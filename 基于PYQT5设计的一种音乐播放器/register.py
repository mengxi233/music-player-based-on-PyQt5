# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_userRegister(object):
    def setupUi(self, userRegister):
        userRegister.setObjectName("userRegister")
        userRegister.resize(1259, 644)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/心-音符.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        userRegister.setWindowIcon(icon)
        self.userlineEdit = QtWidgets.QLineEdit(userRegister)
        self.userlineEdit.setGeometry(QtCore.QRect(470, 139, 481, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self.userlineEdit.setFont(font)
        self.userlineEdit.setObjectName("userlineEdit")
        self.user = QtWidgets.QGraphicsView(userRegister)
        self.user.setGeometry(QtCore.QRect(300, 139, 48, 48))
        self.user.setStyleSheet("border-image: url(:/image/用户名-登录页.png);")
        self.user.setObjectName("user")
        self.psdlineEdit1 = QtWidgets.QLineEdit(userRegister)
        self.psdlineEdit1.setGeometry(QtCore.QRect(470, 220, 481, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self.psdlineEdit1.setFont(font)
        self.psdlineEdit1.setInputMethodHints(QtCore.Qt.ImhDialableCharactersOnly|QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhEmailCharactersOnly|QtCore.Qt.ImhExclusiveInputMask|QtCore.Qt.ImhFormattedNumbersOnly|QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhLatinOnly|QtCore.Qt.ImhLowercaseOnly|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData|QtCore.Qt.ImhUppercaseOnly|QtCore.Qt.ImhUrlCharactersOnly)
        self.psdlineEdit1.setInputMask("")
        self.psdlineEdit1.setMaxLength(255)
        self.psdlineEdit1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.psdlineEdit1.setDragEnabled(False)
        self.psdlineEdit1.setObjectName("psdlineEdit1")
        self.user_lable = QtWidgets.QLabel(userRegister)
        self.user_lable.setGeometry(QtCore.QRect(360, 140, 81, 41))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.user_lable.setFont(font)
        self.user_lable.setObjectName("user_lable")
        self.password_lable = QtWidgets.QLabel(userRegister)
        self.password_lable.setGeometry(QtCore.QRect(360, 220, 81, 41))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.password_lable.setFont(font)
        self.password_lable.setObjectName("password_lable")
        self.password = QtWidgets.QGraphicsView(userRegister)
        self.password.setGeometry(QtCore.QRect(300, 220, 48, 48))
        self.password.setStyleSheet("border-image: url(:/image/密码.png);")
        self.password.setObjectName("password")
        self.title = QtWidgets.QLabel(userRegister)
        self.title.setGeometry(QtCore.QRect(530, 50, 181, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.password_lable_2 = QtWidgets.QLabel(userRegister)
        self.password_lable_2.setGeometry(QtCore.QRect(310, 310, 131, 41))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.password_lable_2.setFont(font)
        self.password_lable_2.setObjectName("password_lable_2")
        self.psdlineEdit2 = QtWidgets.QLineEdit(userRegister)
        self.psdlineEdit2.setGeometry(QtCore.QRect(470, 310, 481, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self.psdlineEdit2.setFont(font)
        self.psdlineEdit2.setInputMethodHints(QtCore.Qt.ImhDialableCharactersOnly|QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhEmailCharactersOnly|QtCore.Qt.ImhExclusiveInputMask|QtCore.Qt.ImhFormattedNumbersOnly|QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhLatinOnly|QtCore.Qt.ImhLowercaseOnly|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData|QtCore.Qt.ImhUppercaseOnly|QtCore.Qt.ImhUrlCharactersOnly)
        self.psdlineEdit2.setInputMask("")
        self.psdlineEdit2.setMaxLength(255)
        self.psdlineEdit2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.psdlineEdit2.setDragEnabled(False)
        self.psdlineEdit2.setObjectName("psdlineEdit2")
        self.tips1 = QtWidgets.QLabel(userRegister)
        self.tips1.setGeometry(QtCore.QRect(980, 170, 221, 130))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.tips1.setFont(font)
        self.tips1.setWordWrap(True)
        self.tips1.setObjectName("tips1")
        self.tips2 = QtWidgets.QLabel(userRegister)
        self.tips2.setGeometry(QtCore.QRect(980, 295, 221, 81))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.tips2.setFont(font)
        self.tips2.setWordWrap(True)
        self.tips2.setObjectName("tips2")
        self.bnt_register = QtWidgets.QPushButton(userRegister)
        self.bnt_register.setGeometry(QtCore.QRect(770, 410, 181, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self.bnt_register.setFont(font)
        self.bnt_register.setObjectName("bnt_register")
        self.logo1 = QtWidgets.QLabel(userRegister)
        self.logo1.setGeometry(QtCore.QRect(470, 60, 48, 48))
        self.logo1.setStyleSheet("border-image: url(:/image/心-音符.png);")
        self.logo1.setText("")
        self.logo1.setObjectName("logo1")
        self.logo1_2 = QtWidgets.QLabel(userRegister)
        self.logo1_2.setGeometry(QtCore.QRect(710, 60, 48, 48))
        self.logo1_2.setStyleSheet("border-image: url(:/image/心-音符.png);")
        self.logo1_2.setText("")
        self.logo1_2.setObjectName("logo1_2")

        self.retranslateUi(userRegister)
        QtCore.QMetaObject.connectSlotsByName(userRegister)

    def retranslateUi(self, userRegister):
        _translate = QtCore.QCoreApplication.translate
        userRegister.setWindowTitle(_translate("userRegister", "注册"))
        self.user_lable.setText(_translate("userRegister", "用户名："))
        self.password_lable.setText(_translate("userRegister", "密  码："))
        self.title.setText(_translate("userRegister", "用  户  注 册"))
        self.password_lable_2.setText(_translate("userRegister", "确 认 密 码："))
        self.tips1.setText(_translate("userRegister", "至少包含，小写字母，大写字母，数字，特殊字符其中的两种，密码长度在4到24位之间"))
        self.tips2.setText(_translate("userRegister", "再一次确认密码，与上一栏密码内容一致。"))
        self.bnt_register.setText(_translate("userRegister", "注册"))
import Picture_rc
