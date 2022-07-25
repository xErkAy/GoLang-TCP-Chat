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
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(60, 105, 81, 31))
        self.save.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.save.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.save.setStyleSheet("QPushButton {\n"
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
        self.save.setObjectName("save")
        self.clear_cache = QtWidgets.QPushButton(self.centralwidget)
        self.clear_cache.setGeometry(QtCore.QRect(160, 105, 81, 31))
        self.clear_cache.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.clear_cache.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.clear_cache.setStyleSheet("QPushButton {\n"
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
        self.clear_cache.setObjectName("clear_cache")
        self.old_password = QtWidgets.QLineEdit(self.centralwidget)
        self.old_password.setGeometry(QtCore.QRect(20, 20, 270, 31))
        self.old_password.setStyleSheet("border-radius: 3px;\n"
"border: 1px solid #d3d9de;\n"
"padding-left: 3px;\n"
"background-color: #ffffff;")
        self.old_password.setPlaceholderText("Old password")
        self.old_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.old_password.setObjectName("old_password")
        self.new_password = QtWidgets.QLineEdit(self.centralwidget)
        self.new_password.setGeometry(QtCore.QRect(20, 60, 270, 31))
        self.new_password.setStyleSheet("border-radius: 3px;\n"
"border: 1px solid #d3d9de;\n"
"padding-left: 3px;\n"
"background-color: #ffffff;")
        self.new_password.setPlaceholderText("New password")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setObjectName("new_password")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Settings"))
        self.save.setText(_translate("MainWindow", "Save"))
        self.clear_cache.setText(_translate("MainWindow", "Clear cache"))
