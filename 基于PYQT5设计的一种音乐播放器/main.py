import hashlib
import os
import random
import shutil

import eyed3
import pygame
import pymysql
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, QDateTime, Qt
from PyQt5.QtGui import QPainter, QPen, QFont, QTransform
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QColorDialog, QDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem

from login import Ui_Form
from register import Ui_userRegister
from theme import Ui_theme
from window import Ui_MainWindow

#   定义全局变量 表示当前用户和登录状态
CurructUser = None
State = False
bkdChange = False
# 数据库连接信息
myhost = "localhost"
myuser = "root"
mypassword = "222416"
mydatabase = "msy"


class MusicPlayer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # 初始化音乐总时间和当前播放时间的变量
        pygame.init()
        pygame.mixer.init()
        self.login_window = None
        self.total_time = 0
        self.current_time = 0
        self.current_music_path = None
        self.isPlay = False
        self.setupUi(self)
        self.bnt_Music.clicked.connect(self.show_music)
        self.bnt_importMusic.clicked.connect(self.import_music)
        self.bnt_LoveMusic.clicked.connect(self.show_love_music)
        self.bnt_theme.clicked.connect(self.show_theme_settings)
        self.bnt_login.clicked.connect(self.show_login_window)
        self.bnt_previous.clicked.connect(self.play_previous)
        self.bnt_play.clicked.connect(self.play_pause)
        self.bnt_next.clicked.connect(self.play_next)
        self.bnt_addToMyLove.clicked.connect(self.add_to_love)
        self.bnt_logout.clicked.connect(self.logout)
        self.mylist.itemClicked.connect(self.play_selected_music)
        self.bnt_serch.clicked.connect(self.search_music)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_time2)
        self.timer2.start(1000)  # 设置定时器间隔为1000毫秒（1秒）

    def search_music(self):
        # 获取搜索关键字
        search_keyword = self.serchEdit.text()
        if search_keyword:
            # 执行搜索操作
            self.perform_search(search_keyword)
        else:
            QMessageBox.warning(self, "提示", "请输入搜索关键字")

    def perform_search(self, keyword):
        global myhost, myuser, mypassword, mydatabase
        connection = pymysql.connect(
            host=myhost,
            user=myuser,
            password=mypassword,
            database=mydatabase,
        )
        try:
            with connection.cursor() as cursor:
                # 查询包含搜索关键字的音乐信息
                sql_select = "SELECT * FROM music WHERE name LIKE %s OR artist LIKE %s"
                cursor.execute(sql_select, (f"%{keyword}%", f"%{keyword}%"))
                result = cursor.fetchall()

                if result:
                    # 清空mylist
                    self.mylist.setRowCount(0)

                    # 遍历喜欢的音乐地址，获取音乐信息并输出到mylist
                    for row, record in enumerate(result):

                        # music_dir = record[0]  # 使用索引而不是键
                        print(record[3])
                        music_info = self.get_music_info(record[3])

                        if music_info:
                            self.mylist.insertRow(row)
                            for col, info in enumerate(music_info):
                                item = QTableWidgetItem(str(info))
                                self.mylist.setItem(row, col, item)
                                item.setTextAlignment(0x0004 | 0x0080)  # 居中对齐
                    listcnt = self.mylist.rowCount()
                    self.mylist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    self.cnt.setText(f"总计个数:{listcnt}")

                else:
                    QMessageBox.warning(self, "提示", "未找到符合条件的音乐")

        except Exception as e:
            print("Error performing search:", e)
        finally:
            # 关闭数据库连接
            connection.close()

    def show_theme_settings(self):
        theme_settings = ThemeSettings(self)
        theme_settings.set_main_window(self)
        theme_settings.exec_()

    def show_login_window(self):
        global CurructUser, State
        if State:
            QMessageBox.information(self, "提示", f"{CurructUser} 您已经登录了，如果想切换账户请先退出登录")
        else:
            self.login_window = LoginWindow()
            self.login_window.show()

    def get_music_info(self, path):
        try:

            audiofile = eyed3.load(path)

            if audiofile.tag:
                # 获取歌曲名
                title = audiofile.tag.title

                # 获取艺术家
                artist = audiofile.tag.artist if audiofile.tag.artist else "未知艺术家"

                # 获取时长（以秒为单位）

                duration = self.seconds_to_hh_mm_ss(audiofile.info.time_secs)

                # 返回包含音乐信息的列表
                return [title, artist, duration, path]

        except Exception as e:
            print(f"文件位置错误 {path}: {e}")

        # 如果出现错误或者没有元数据，返回 None
        return None

    def show_love_music(self):

        global CurructUser, State
        if not State:
            QMessageBox.warning(self, "提示", "请先登录！")
            return
        self.mylist.setColumnCount(4)  # 列数为4，分别是标题、艺术家、时长和文件地址

        # 设置列标签
        header_labels = ["歌曲名", "艺术家", "时长", "文件地址"]
        self.mylist.setHorizontalHeaderLabels(header_labels)
        global myhost, myuser, mypassword, mydatabase
        connection = pymysql.connect(
            host=myhost,
            user=myuser,
            password=mypassword,
            database=mydatabase,
        )
        try:
            with connection.cursor() as cursor:
                # 查询当前用户的喜欢音乐地址
                sql_select = "SELECT music_dir FROM favorite WHERE user_name = %s"
                cursor.execute(sql_select, (CurructUser,))
                result = cursor.fetchall()

                if result:
                    # 清空mylist
                    self.mylist.setRowCount(0)

                    # 遍历喜欢的音乐地址，获取音乐信息并输出到mylist
                    for row, record in enumerate(result):

                        music_dir = record[0]  # 使用索引而不是键
                        music_info = self.get_music_info(music_dir)

                        if music_info:
                            self.mylist.insertRow(row)
                            for col, info in enumerate(music_info):
                                item = QTableWidgetItem(str(info))
                                self.mylist.setItem(row, col, item)
                                item.setTextAlignment(0x0004 | 0x0080)  # 居中对齐
                    listcnt = self.mylist.rowCount()
                    self.mylist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    self.cnt.setText(f"总计个数:{listcnt}")
                else:
                    QMessageBox.warning(self, "提示", "当前用户没有喜欢的音乐！")

        except Exception as e:
            print("Error fetching love music:", e)
        finally:
            # 关闭数据库连接
            connection.close()

    def logout(self):
        global CurructUser
        global State
        CurructUser = None
        State = False
        QMessageBox.information(self, "提示", f"退出成功")
        pass

    def add_to_love(self):
        global CurructUser, State
        if State:

            # 获取当前用户名和歌曲地址
            current_user = CurructUser
            current_music_path = self.current_music_path

            # 将用户名和歌曲地址插入到数据库中
            if current_user and current_music_path:
                # 建立数据库连接

                global myhost, myuser, mypassword, mydatabase
                connection = pymysql.connect(
                    host=myhost,
                    user=myuser,
                    password=mypassword,
                    database=mydatabase,
                )

                try:
                    with connection.cursor() as cursor:
                        # 查询是否已存在
                        sql_check = "SELECT * FROM favorite WHERE user_name = %s AND music_dir = %s"
                        cursor.execute(sql_check, (current_user, current_music_path))
                        result = cursor.fetchone()

                        if not result:  # 如果记录不存在，则执行插入操作
                            # 执行插入 SQL
                            sql_insert = "INSERT INTO favorite (user_name, music_dir) VALUES (%s, %s)"
                            cursor.execute(sql_insert, (current_user, current_music_path))
                            # 提交到数据库
                            connection.commit()
                            print("Song added to favorites successfully.")
                            QMessageBox.information(self, "提示", f"用户 {current_user} ,添加成功！")
                        else:
                            print("Song already exists in favorites.")
                            QMessageBox.warning(self, "提示", f"用户 {current_user} ,已经添加过该歌曲！")

                except Exception as e:
                    print("Error adding song to favorites:", e)
                finally:
                    # 关闭数据库连接
                    connection.close()
        else:
            QMessageBox.warning(self, "错误", "未登录")

        pass

    def show_music(self):
        print("Show My Music begin")
        # 获取音乐文件夹中的文件列表
        music_folder = 'music'  # 替换为实际的音乐文件夹路径
        music_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
        # 清空数据库表单
        self.clear_database_table()
        # 在 QTableWidget 中设置行和列的数量
        self.mylist.setRowCount(len(music_files))
        self.mylist.setColumnCount(4)  # 列数为4，分别是标题、艺术家、时长和文件地址
        # 设置列标签
        header_labels = ["歌曲名", "艺术家", "时长", "文件地址"]
        self.mylist.setHorizontalHeaderLabels(header_labels)
        # 使用 eyed3 获取 MP3 文件的元数据信息并填充 QTableWidget
        for row_idx, file_name in enumerate(music_files):
            file_path = os.path.join(music_folder, file_name)
            audiofile = eyed3.load(file_path)
            # 获取标题、艺术家和时长信息
            title = audiofile.tag.title
            artist = audiofile.tag.artist
            duration = self.seconds_to_hh_mm_ss(audiofile.info.time_secs)
            # 在 QTableWidget 中填充信息
            self.mylist.setItem(row_idx, 0, QTableWidgetItem(title))
            self.mylist.setItem(row_idx, 1, QTableWidgetItem(artist))
            self.mylist.setItem(row_idx, 2, QTableWidgetItem(duration))
            self.mylist.setItem(row_idx, 3, QTableWidgetItem(file_path))  # 新增一列显示文件地址
            # 设置单元格文本居中对齐
            for col_idx in range(self.mylist.columnCount()):
                item = self.mylist.item(row_idx, col_idx)
                item.setTextAlignment(0x0004 | 0x0080)  # 居中对齐
            # 将音乐信息插入数据库
            self.insert_music_to_database(title, artist, duration, file_path)
        # 设置列宽度自动填充整个表格
        self.mylist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        listcnt = self.mylist.rowCount()
        self.cnt.setText(f"总计个数:{listcnt}")
        print("Show My Music end")

    def clear_database_table(self):
        # 清空数据库表单
        global myhost, myuser, mypassword, mydatabase
        connection = pymysql.connect(
            host=myhost,
            user=myuser,
            password=mypassword,
            database=mydatabase,
        )
        try:
            with connection.cursor() as cursor:
                sql_delete = "DELETE FROM music"
                cursor.execute(sql_delete)
            connection.commit()
        except Exception as e:
            print("Error clearing database table:", e)
        finally:
            connection.close()
        pass

    def seconds_to_hh_mm_ss(self, seconds):
        # 将秒数转换为hh:mm:ss的格式
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    def insert_music_to_database(self, title, artist, duration, file_path):
        # 将音乐信息插入数据库
        global myhost, myuser, mypassword, mydatabase
        connection = pymysql.connect(
            host=myhost,
            user=myuser,
            password=mypassword,
            database=mydatabase,
        )
        try:
            with connection.cursor() as cursor:
                sql_insert = "INSERT INTO music (name, artist, time, dir) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_insert, (title, artist, duration, file_path))
            connection.commit()
        except Exception as e:
            print("Error inserting music to database:", e)
        finally:
            connection.close()

    def import_music(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(self, "导入本地音乐", "",
                                                     "Music Files (*.mp3)", options=options)

        for file_name in file_names:
            # 实现逻辑来导入音乐，例如将文件复制到音乐文件夹
            destination_folder = 'music'  # 替换为实际的音乐文件夹路径
            destination_path = os.path.join(destination_folder, os.path.basename(file_name))

            # 检查目标路径是否已存在，如果存在，可以进行重命名等操作
            if os.path.exists(destination_path):
                # 在文件名后面添加数字以确保唯一性
                base, extension = os.path.splitext(os.path.basename(file_name))
                counter = 1
                while os.path.exists(os.path.join(destination_folder, f"{base}_{counter}{extension}")):
                    counter += 1
                destination_path = os.path.join(destination_folder, f"{base}_{counter}{extension}")

            # 复制文件到目标路径
            shutil.copy2(file_name, destination_path)

            # 在音乐列表中显示新导入的音乐
            self.show_music()

            print(f"Importing Music: {file_name} to {destination_path}")

    def play_selected_music(self, item):
        # 获取选中行的行号
        row = self.mylist.row(item)

        # 获取选中行的文件地址
        file_path_item = self.mylist.item(row, 3)
        file_path = file_path_item.text()

        # 播放选中音乐的逻辑
        self.play_music(file_path)
        self.musicInfo.setText(f"{self.mylist.item(row, 0).text()}--{self.mylist.item(row, 1).text()} ")
        pygame.mixer.music.pause()
        icon = QtGui.QIcon(":/image/播放.png")
        self.bnt_play.setIcon(icon)

    def play_music(self, file_path):
        if self.mylist.currentRow() >= 0:
            icon = QtGui.QIcon(":/image/暂停.png")
            self.bnt_play.setIcon(icon)
            # 如果当前正在播放，停止音乐
            pygame.mixer.music.stop()
            pygame.mixer.music.load(file_path)

            # 加载新的音乐文件
            pygame.mixer.music.play()
            self.isPlay = True

            # 更新当前音乐文件路径
            self.current_music_path = file_path
            self.total_time = pygame.mixer.Sound(file_path).get_length()
            self.update_time()
            self.timer.start(1000)

    def play_pause(self):
        if self.mylist.currentRow() >= 0:
            # 实现播放或暂停音乐的逻辑
            if pygame.mixer.music.get_busy():
                self.timer.stop()
                pygame.mixer.music.pause()
                # 更换图标
                icon = QtGui.QIcon(":/image/播放.png")
                self.bnt_play.setIcon(icon)
                self.isPlay = False
            else:
                self.timer.start(1000)
                pygame.mixer.music.unpause()
                # 更换图标
                icon = QtGui.QIcon(":/image/暂停.png")
                self.bnt_play.setIcon(icon)
                self.isPlay = True

    def play_previous(self):
        if self.mylist.currentRow() >= 0:
            # 实现播放上一首音乐的逻辑

            # 获取当前选中的行
            current_row = self.mylist.currentRow()

            # 获取音乐文件的总数
            total_music = self.mylist.rowCount()

            if current_row > 0:
                # 如果不是第一首歌曲，播放上一首
                previous_row = current_row - 1
            else:
                # 如果是第一首歌曲，切换到最后一首
                previous_row = total_music - 1

            # 获取上一首歌曲的文件地址
            file_path_item = self.mylist.item(previous_row, 3)
            file_path = file_path_item.text()

            # 播放上一首音乐的逻辑
            self.play_music(file_path)

            # 更新标签显示当前播放音乐信息
            self.musicInfo.setText(
                f"{self.mylist.item(previous_row, 0).text()}--{self.mylist.item(previous_row, 1).text()} ")

            # 设置当前选择的行列到上一行的第一列
            self.mylist.setCurrentCell(previous_row, 0)

            # 停止计时器
            # self.timer.stop()

    def play_next(self):
        # 获取当前选中的行
        current_row = self.mylist.currentRow()
        # 获取音乐文件的总数
        total_music = self.mylist.rowCount()
        if current_row < total_music - 1:
            # 如果不是最后一首歌曲，播放下一首
            next_row = current_row + 1
        else:
            # 如果是最后一首歌曲，切换到第一首
            next_row = 0
        # 获取下一首歌曲的文件地址
        file_path_item = self.mylist.item(next_row, 3)
        file_path = file_path_item.text()
        # 播放下一首音乐的逻辑
        self.play_music(file_path)
        self.musicInfo.setText(f"{self.mylist.item(next_row, 0).text()}--{self.mylist.item(next_row, 1).text()} ")
        # 更新标签显示当前播放音乐信息
        self.mylist.setCurrentCell(next_row, 0)
        self.update_time()
        print(total_music, current_row)
        print("Play Next Song")

        # .timer.stop()
        pass

    def update_time(self):
        print("正在更新时间...")
        self.current_time = pygame.mixer.music.get_pos() / 1000
        print("总时间：", self.total_time)
        print("当前时间：", self.current_time)

        self.musicTime.setText(
            self.seconds_to_hh_mm_ss(self.current_time) + "/" + self.seconds_to_hh_mm_ss(self.total_time))
        progress_value = int((self.current_time / self.total_time) * 100)
        print("进度值：", progress_value)
        self.musicprogressBar.setValue(progress_value)

    def update_time2(self):
        # 获取当前系统时间
        current_time = QDateTime.currentDateTime()
        global CurructUser, bkdChange
        if State:
            self.Title.setText(f"{CurructUser}已登录")
        else:
            self.Title.setText(f"2023-2024学年度 可视化程序设计期末大作业")
        if bkdChange:
            self.background_bar.setStyleSheet(f"background-color: rgb(205, 205, 205);")
            self.serchEdit.setStyleSheet(f"background-color: rgb(255, 255, 255);")
            self.bnt_serch.setStyleSheet(f"background-color: rgb(205, 205, 205);")
        # 格式化时间为字符串
        time_str = current_time.toString("yyyy/MM/dd hh:mm:ss")
        # 在标签上显示时间
        self.nowDateTime.setText(f" {time_str}")


class LoginWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.register_window = Ui_userRegister()
        self.setupUi(self)

        self.bnt_login.clicked.connect(self.login)
        self.bnt_register.clicked.connect(self.register)
        self.changeCheakCode.clicked.connect(self.update_captcha)
        self.code = ''
        self.string = ''
        self.char = []
        for i in range(48, 58):
            self.char.append(chr(i))
        for i in range(65, 91):
            self.char.append(chr(i))
        for i in range(97, 123):
            self.char.append(chr(i))
        self.should_draw_captcha = False

    def update_captcha(self):
        self.should_draw_captcha = True
        self.repaint()

    # 验证码
    def paintEvent(self, event):
        if self.should_draw_captcha:
            painter = QPainter(self)
            painter.drawRect(300, 380, 480, 150)

            # ###############   绘制直线      ###############################
            line_pen = QPen(Qt.red)
            line_pen.setWidth(2)
            painter.setPen(line_pen)
            for i in range(60):
                x1 = random.randint(300, 300 + 480)
                y1 = random.randint(380, 380 + 150)
                x2 = random.randint(300, 300 + 480)
                y2 = random.randint(380, 380 + 150)
                painter.drawLine(x1, y1, x2, y2)

            # ###############   绘制噪点      ###############################
            painter.setPen(Qt.green)
            point_pen = QPen(Qt.green)
            point_pen.setWidth(3)
            painter.setPen(point_pen)
            for i in range(800):
                x = random.randint(300, 300 + 480)
                y = random.randint(380, 380 + 150)
                painter.drawPoint(x, y)

            painter.setPen(Qt.black)
            font = QFont()
            font.setFamily("consolas")
            font.setPointSize(40)
            font.setBold(True)
            font.setUnderline(True)
            painter.setFont(font)

            self.string = ''
            for i in range(4):
                c = self.char[random.randint(0, len(self.char) - 1)]
                self.string += c
                rotation_angle = random.uniform(-5, 5)
                transform = QTransform()
                transform.rotate(rotation_angle)
                painter.save()
                painter.setWorldTransform(transform)
                painter.drawText(50 + 50 * i + 380, 380 + 100, c)
                painter.restore()

            print(self.string)
            self.should_draw_captcha = False

    def login(self):
        global CurructUser, State
        # if State:
        #     QMessageBox.warning(self, "Tips", "已经登录了，切换账户先退出登录")

        import hashlib
        user_name = self.userlineEdit.text()
        password = self.psdlineEdit_2.text()
        checkCode = self.cheaklineEdit.text()

        # MD5加密
        md5Psd = hashlib.md5(password.encode()).hexdigest()
        print(md5Psd)

        if self.string == checkCode:
            global myhost, myuser, mypassword, mydatabase
            connection = pymysql.connect(
                host=myhost,
                user=myuser,
                password=mypassword,
                database=mydatabase,
            )
            try:
                with connection.cursor() as cursor:
                    # Check if the username and password match a record in the database
                    sql = "SELECT * FROM `user` WHERE `user_name`=%s AND `password`=%s"
                    cursor.execute(sql, (user_name, md5Psd))

                    result = cursor.fetchone()
                    print(result)
                    if result:
                        # User is authenticated, add your logic for successful login

                        QMessageBox.information(self, '成功', f'登录成功\n你好 {user_name}')
                        CurructUser = user_name
                        State = True
                        self.userlineEdit.clear()
                        self.psdlineEdit_2.clear()
                        self.cheaklineEdit.clear()
                        self.close()
                    else:
                        # Incorrect username or password
                        QMessageBox.warning(self, '错误', '用户名或密码错误')
            finally:
                connection.close()
        else:
            QMessageBox.warning(self, '错误', '验证码错误.')

        # print(user_name, password, checkCode)

    def register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()


class RegisterWindow(QWidget, Ui_userRegister):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bnt_register.clicked.connect(self.Register)
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="222416",
            database="msy")
        self.cursor = self.db.cursor()

    def validate_password(self, password):
        requirements = [any(c.islower() for c in password),
                        any(c.isupper() for c in password),
                        any(c.isdigit() for c in password),
                        any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for c in password)]
        return sum(requirements) >= 2 and 4 <= len(password) <= 24

    def check_existing_username(self, username):
        query = f"SELECT * FROM user WHERE user_name = '{username}'"
        self.cursor.execute(query)
        return self.cursor.fetchone() is not None

    def Register(self):
        inputUsername = self.userlineEdit.text()
        inputPassword1 = self.psdlineEdit1.text()
        inputPassword2 = self.psdlineEdit2.text()

        if inputPassword1 != inputPassword2:
            QMessageBox.warning(self, "错误", "两次输入的密码不一样")
            self.psdlineEdit1.clear()
            self.psdlineEdit2.clear()
        elif not self.validate_password(inputPassword1):
            QMessageBox.warning(self, "错误", "密码不符合要求")
            self.psdlineEdit1.clear()
            self.psdlineEdit2.clear()
        elif self.check_existing_username(inputUsername):
            QMessageBox.warning(self, "错误", "用户名已存在")
            self.userlineEdit.clear()
        elif not inputUsername.strip():
            QMessageBox.warning(self, "Error", "用户名不能为空")
            self.userlineEdit.clear()
        else:
            password = hashlib.md5(inputPassword1.encode()).hexdigest()
            insert_query = f"INSERT INTO `user` (user_name, password) VALUES ('{inputUsername}', '{password}')"
            self.cursor.execute(insert_query)
            self.db.commit()
            QMessageBox.information(self, "成功", "注册成功")
            print("注册成功")
            self.close()


class ThemeSettings(QDialog, Ui_theme):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.color.clicked.connect(self.choose_color)
        self.image.clicked.connect(self.choose_image_theme)
        self.parent_window = parent  # 保存主窗口的引用
        self.ok.clicked.connect(self.confirm_theme)
        self.reset.clicked.connect(self.resetTheme)

    def resetTheme(self):
        self.parent_window.setStyleSheet("")
        pass

    def confirm_theme(self):
        ch = self.choose.currentText()
        global bkdChange
        print(ch)
        background = ["background/Anamnisar.jpg", "background/Cool Brown.jpg", "background/Green Beach.jpg",
                      "background/Hazel.jpg", "background/Horizon.jpg"]
        if ch == "彩霞":
            self.parent_window.setStyleSheet(
                f"background-image: url({background[0]}); background-repeat: no-repeat; background-position: center;")

            bkdChange = True
        elif ch == "棕色":
            self.parent_window.setStyleSheet(
                f"background-image: url({background[1]}); background-repeat: no-repeat; background-position: center;")

            bkdChange = True
        elif ch == "绿色海滩":
            self.parent_window.setStyleSheet(
                f"background-image: url({background[2]}); background-repeat: no-repeat; background-position: center;")

            bkdChange = True
        elif ch == "红蓝":
            self.parent_window.setStyleSheet(
                f"background-image: url({background[3]}); background-repeat: no-repeat; background-position: center;")

            bkdChange = True
        elif ch == "地平线":
            self.parent_window.setStyleSheet(
                f"background-image: url({background[4]}); background-repeat: no-repeat; background-position: center;")

            bkdChange = True

    def set_main_window(self, main_window):
        self.parent_window = main_window

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid() and self.parent_window:
            self.parent_window.setStyleSheet(f"background-color: {color.name()};")
            global bkdChange
            bkdChange = True

    def choose_image_theme(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图片主题", "",
                                                   "Images (*.png *.jpg *.bmp);;All Files (*)",
                                                   options=options)
        if file_name and self.parent_window:
            self.parent_window.setStyleSheet("")
            self.parent_window.setStyleSheet(
                f"background-image: url({file_name}); background-repeat: no-repeat; background-position: center;")
            global bkdChange
            bkdChange = True


if __name__ == "__main__":
    app = QApplication([])
    player = MusicPlayer()
    player.show()
    app.exec_()
