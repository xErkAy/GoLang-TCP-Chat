from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QLineEdit


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(310, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(310, 150))
        MainWindow.setMaximumSize(QtCore.QSize(310, 150))
        MainWindow.setStyleSheet("background-color: #edeef0;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.name = QtWidgets.QLineEdit(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(20, 20, 270, 31))
        self.name.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.name.setStyleSheet("border-radius: 3px;\n"
"border: 1px solid #d3d9de;\n"
"outline: none;\n"
"padding-left: 3px;\n"
"background-color: #ffffff;")
        self.name.setPlaceholderText("Name")
        self.name.setObjectName("name")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(20, 60, 270, 31))
        self.password.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.password.setStyleSheet("border-radius: 3px;\n"
"border: 1px solid #d3d9de;\n"
"outline: none;\n"
"padding-left: 3px;\n"
"background-color: #ffffff;")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText("Password")
        self.password.setObjectName("password")
        self.log_in = QtWidgets.QPushButton(self.centralwidget)
        self.log_in.setGeometry(QtCore.QRect(60, 105, 81, 31))
        self.log_in.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.log_in.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.log_in.setStyleSheet("QPushButton {\n"
" border-radius: 7px;\n"
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
        self.log_in.setObjectName("log_in")
        self.sign_up = QtWidgets.QPushButton(self.centralwidget)
        self.sign_up.setGeometry(QtCore.QRect(150, 105, 81, 31))
        self.sign_up.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.sign_up.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.sign_up.setStyleSheet("QPushButton {\n"
" border-radius: 7px;\n"
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
        self.sign_up.setObjectName("sign_up")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Authorization"))
        self.log_in.setText(_translate("MainWindow", "Log in"))
        self.sign_up.setText(_translate("MainWindow", "Sign up"))
