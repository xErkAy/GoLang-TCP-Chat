from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, WindowTitle):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 560)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(850, 560))
        MainWindow.setMaximumSize(QtCore.QSize(850, 560))
        MainWindow.setStyleSheet("background-color: #edeef0;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sendText = QtWidgets.QLineEdit(self.centralwidget)
        self.sendText.setGeometry(QtCore.QRect(10, 480, 440, 31))
        self.sendText.setStyleSheet("border-radius: 3px;\n"
"border: 1px solid #d3d9de;\n"
"padding-left: 3px;\n"
"background-color: #ffffff;")
        self.sendText.setObjectName("sendText")
        self.sendbutton = QtWidgets.QPushButton(self.centralwidget)
        self.sendbutton.setGeometry(QtCore.QRect(492, 480, 81, 31))
        self.sendbutton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.sendbutton.setStyleSheet("QPushButton {\n"
"border-radius: 5px;\n"
"text-align: center;\n"
"background-color: #5181b8;\n"
"border: 0;\n"
"display: inline-block;\n"
"vertical-align: top;\n"
"color: #ffffff;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: #6690c1;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: #5181c2;\n"
"}")
        self.sendbutton.setObjectName("sendbutton")
        self.sendbutton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.sendbutton_1.setGeometry(QtCore.QRect(580, 480, 81, 31))
        self.sendbutton_1.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.sendbutton_1.setStyleSheet("QPushButton {\n"
"border-radius: 5px;\n"
"text-align: center;\n"
"background-color: #5181b8;\n"
"border: 0;\n"
"display: inline-block;\n"
"vertical-align: top;\n"
"color: #ffffff;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: #6690c1;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: #5181c2;\n"
"}")
        self.sendbutton_1.setObjectName("sendbutton_1")
        self.audio_message = QtWidgets.QPushButton(self.centralwidget)
        self.audio_message.setGeometry(QtCore.QRect(448, 475, 40, 40))
        self.audio_message.setStyleSheet("outline: none;\n"
"border: 0;\n"
"background: transparent;")
        self.audio_message.setText("")
        self.audio_message.setObjectName("audio_message")
        self.settings = QtWidgets.QPushButton(self.centralwidget)
        self.settings.setGeometry(QtCore.QRect(580, 520, 81, 31))
        self.audio_message.setIcon(QIcon("microphone.ico"))
        self.settings.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.settings.setStyleSheet("QPushButton {\n"
"border-radius: 5px;\n"
"text-align: center;\n"
"background-color: #5181b8;\n"
"border: 0;\n"
"display: inline-block;\n"
"vertical-align: top;\n"
"color: #ffffff;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color: #6690c1;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: #5181c2;\n"
"}")
        self.settings.setObjectName("settings")
        self.messages = QtWidgets.QTextBrowser(self.centralwidget)
        self.messages.setGeometry(QtCore.QRect(5, 10, 661, 461))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.messages.setFont(font)
        self.messages.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.messages.setAcceptDrops(False)
        self.messages.setStyleSheet("background-color: #ffffff;\nborder: 0;")
        self.messages.setOpenLinks(False)
        self.messages.setObjectName("messages")
        self.users_online = QtWidgets.QListWidget(self.centralwidget)
        self.users_online.setGeometry(QtCore.QRect(680, 10, 160, 540))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.users_online.setFont(font)
        self.users_online.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.users_online.setStyleSheet("background-color: #ffffff;\n"
"border-radius: 3px;")
        self.users_online.setObjectName("users_online")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow, WindowTitle)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow, WindowTitle):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", WindowTitle))
        self.sendbutton.setText(_translate("MainWindow", "Send"))
        self.sendbutton_1.setText(_translate("MainWindow", "Send file"))
        self.settings.setText(_translate("MainWindow", "Settings"))
