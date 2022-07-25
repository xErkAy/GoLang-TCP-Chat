from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, WindowTitle):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(360, 220)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(360, 220))
        MainWindow.setMaximumSize(QtCore.QSize(360, 220))
        MainWindow.setStyleSheet("background-color: #edeef0;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.messages = QtWidgets.QTextBrowser(self.centralwidget)
        self.messages.setGeometry(QtCore.QRect(5, 10, 350, 150))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.messages.setFont(font)
        self.messages.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.messages.setAcceptDrops(False)
        self.messages.setStyleSheet("background-color: #ffffff;\nborder: 0;")
        self.messages.setOpenLinks(False)
        self.messages.setObjectName("messages")
        self.record = QtWidgets.QPushButton(self.centralwidget)
        self.record.setGeometry(QtCore.QRect(50, 175, 81, 31))
        self.record.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.record.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.record.setStyleSheet("QPushButton {\n"
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
        self.record.setObjectName("record")
        self.listen = QtWidgets.QPushButton(self.centralwidget)
        self.listen.setGeometry(QtCore.QRect(140, 175, 81, 31))
        self.listen.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.listen.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.listen.setStyleSheet("QPushButton {\n"
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
        self.listen.setObjectName("listen")
        self.send = QtWidgets.QPushButton(self.centralwidget)
        self.send.setGeometry(QtCore.QRect(230, 175, 81, 31))
        self.send.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.send.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.send.setStyleSheet("QPushButton {\n"
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
        self.send.setObjectName("send")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow, WindowTitle)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow, WindowTitle):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", WindowTitle))
        self.record.setText(_translate("MainWindow", "Record"))
        self.listen.setText(_translate("MainWindow", "Listen"))
        self.send.setText(_translate("MainWindow", "Send"))
