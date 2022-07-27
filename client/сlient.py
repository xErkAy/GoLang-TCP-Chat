import sys
import random
import socket
import time
import configparser
import os.path
import os
import json
import re
import main_gui
import auth_gui
import audio_message
import settings
import pms
import hashlib
import wave
from pathlib import Path
from threading import Thread
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import *
from cryptography.fernet import Fernet
from PyQt6.QtGui import QIcon, QDesktopServices
from PyQt6.QtCore import QThread, QObject

users_response = []


class Authentication(QtWidgets.QMainWindow, auth_gui.Ui_MainWindow):
    def __init__(self):
        super(Authentication, self).__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setupUi(self)
        self.key = "nLsAq81xXqmU7hF"
        self.init_ui()

    def init_ui(self):
        try:
            config = configparser.ConfigParser()
            config.read("settings.ini")
            last_used_name = config.get("settings", "last_used_name")
            if last_used_name != "0":
                self.name.setText(last_used_name)
        except:
            pass
        self.log_in.clicked.connect(self.log_in_func)
        self.name.returnPressed.connect(self.log_in_func)
        self.password.returnPressed.connect(self.log_in_func)
        self.sign_up.clicked.connect(self.sign_up_func)

    def generate_hash_password(self):
        alphabet = "ab7cdefg!h4ijklmn-opqrstuvwxy_235zABC?DEFGHI.JKLMNOPQRSTUVWXYZ16890"
        result = ""
        for i in range(40):
            result += alphabet[random.randint(0, 65)]
        return hashlib.md5(result.encode()).hexdigest()

    def log_in_func(self):
        try:
            config = configparser.ConfigParser()
            config.read("settings.ini")
            self.pass_encrypt_key = config.get("settings", "user_password_encrypt_key")
        except:
            QMessageBox.warning(self, "Error", "Contact your administrator to solve this problem.")
            return

        if self.pass_encrypt_key == "0":
            file = open("settings.ini", "wt")
            config.set("settings", "user_password_encrypt_key", self.generate_hash_password())
            config.write(file)
            file.close()

        if not re.search("(\w+)", self.name.text()) or not re.search("(\w+)", self.password.text()):
            QMessageBox.warning(self, "Error", "Enter your username and password.")
            return

        file = open("settings.ini", "wt")
        config.set("settings", "last_used_name", self.name.text())
        config.write(file)
        file.close()

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 8080))
        except:
            QMessageBox.warning(self, "Error", "The connection has been failed.")
            return

        message = {
            "type": "authorization",
            "username": nick_encrypt(self.name.text()),
            "password": pass_encrypt(self.password.text(), self.pass_encrypt_key)
        }
        client.send(json.dumps(message).encode("utf-8"))

        try:
            data = client.recv(1024)
            if data == b'0':
                QMessageBox.warning(self, "Error", "The connection has been failed."
                                                   "\nError username or password.")
                client.close()
                return
        except:
            QMessageBox.warning(self, "Error", "The connection has been failed.")
            client.close()
            return

        self.chat_app = Chat(self.name.text(), client)
        self.close()
        self.chat_app.show()

    def sign_up_func(self):
        try:
            config = configparser.ConfigParser()
            config.read("settings.ini")
            pass_encrypt_key = config.get("settings", "user_password_encrypt_key")
        except:
            QMessageBox.warning(self, "Error", "Contact your administrator to solve this problem.")
            return

        if not re.search("(\w+)", self.name.text()) or not re.search("(\w+)", self.password.text()):
            QMessageBox.warning(self, "Error", "Enter your name and password.")
            return

        if pass_encrypt_key == "0":
            self.pass_encrypt_key = self.generate_hash_password()
            file = open("settings.ini", "wt")
            config.set("settings", "user_password_encrypt_key", self.pass_encrypt_key)
            config.write(file)
            file.close()

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 8080))
        except:
            QMessageBox.warning(self, "Error", "The connection has been failed.")
            return

        message = {
            "type": "registration",
            "username": nick_encrypt(self.name.text()),
            "password": pass_encrypt(self.password.text(), self.pass_encrypt_key)
        }
        client.send(json.dumps(message).encode("utf-8"))
        try:
            data = client.recv(1024)
            if data == b'1':
                QMessageBox.information(self, "Success", "The user has been created.")
            elif data == b'0':
                QMessageBox.warning(self, "Error", "This user already exists."
                                                   "\nTry to use a different name.")
        except:
            QMessageBox.warning(self, "Error", "The connection has been failed.")
        client.close()


class Chat(QtWidgets.QMainWindow, main_gui.Ui_MainWindow, QObject):
    def __init__(self, username, client):
        super(Chat, self).__init__()
        self.username = username
        self.client = client
        self.setWindowIcon(QIcon("icon.ico"))
        self.setupUi(self, "Chat [" + username + "]")
        self.init_ui()

    def init_ui(self):
        self.sendbutton.clicked.connect(self.send_text)
        self.sendbutton_1.clicked.connect(self.send_file)
        self.audio_message.clicked.connect(self.audio_message_window)
        self.users_online.clicked.connect(self.send_pm_message)
        self.sendText.returnPressed.connect(self.send_text)
        self.settings.clicked.connect(self.settings_window)
        self.messages.anchorClicked.connect(QDesktopServices.openUrl)

        message = {
            "type": "login",
            "message": {
                "text": self.username + " connected to the server!",
            }
        }
        self.client.send(json.dumps(message).encode("utf-8"))
        self.messages.append("<html>You connected to the server.</html>")
        self.messages.repaint()

        self.thread = ChatUpdating(messages=self.messages, client=self.client)
        self.thread.start()

    def audio_message_window(self):
        self.audio_message_app = AudioMessage("")
        self.audio_message_app.show()

    def settings_window(self):
        self.settings_app = Settings()
        self.settings_app.show()

    def closeEvent(self, event):
        try:
            message = {
                "type": "logout",
                "message": {
                    "text": self.username + " disconnected from the server!",
                }
            }
            self.client.send(json.dumps(message).encode("utf-8"))
            self.client.close()
        except:
            pass
        event.accept()
        exit(0)

    def send_pm_message(self):
        nick_sendto = self.users_online.selectedIndexes()[0].data()
        if nick_sendto == "Users online:" or nick_sendto == self.username:
            return

        self.pm_message_app = PMMessages(self.client, nick_sendto)
        self.pm_message_app.show()

    def send_text(self):
        if not re.search("(\w+)", self.sendText.text()):
            self.sendText.clear()
            return
        if len(self.sendText.text()) > 100:
            self.sendText.clear()
            QMessageBox.warning(self, "Error", "Your message is too long.")
            return
        try:
            self.messages.append("<html>[" + time.strftime("%H:%M:%S") + "] You: " + self.sendText.text() + "</html>")
            message = {
                "username": self.username,
                "type": "message",
                "message": {
                    "text": str(crypt.encrypt(bytes(self.sendText.text(), encoding="utf-8")), encoding="utf-8"),
                    "time": str(crypt.encrypt(bytes(time.strftime("%H:%M:%S"), encoding="utf-8")), encoding="utf-8")
                }
            }
            self.client.send(json.dumps(message).encode("utf-8"))
        except:
            pass
        self.sendText.clear()

    def send_file(self):
        selectedfile = QFileDialog.getOpenFileName(self, "Open file", "C:\\", "Any file (*)")
        if selectedfile[0] == "":
            return

        if os.path.getsize(selectedfile[0]) > 1073741824:
            QMessageBox.warning(self, "Error", "Your file is too big. (max = 1 gb)")
            return

        file_path = selectedfile[0]
        file_name = os.path.split(selectedfile[0])[1]

        self.messages.append(f'<html>[{time.strftime("%H:%M:%S")}] You sent a file - {file_name}.</html>')

        file_name = str(crypt.encrypt(file_name.encode()), encoding="utf-8")

        self.send_file_thread = SendFileLoop(username=self.username, file_name=file_name, file_path=file_path, client=self.client)
        self.send_file_thread.start()

class SendFileLoop(QThread):

    def __init__(self, username, file_name, file_path, client):
        super().__init__()
        self.username = username
        self.file_name = file_name
        self.file_path = file_path
        self.client = client

    def run(self):
        file = open(self.file_path, "rb")
        data = file.read(32768)
        message = {
            "username": self.username,
            "type": "file_message",
            "file": {
                "type": "file_data",
                "file_name": self.file_name,
                "data": str(crypt.encrypt(data), encoding="utf-8")
            }
        }
        while data:
            time.sleep(0.3)
            self.client.send(json.dumps(message).encode("utf-8"))
            data = file.read(32768)
            message = {
                "username": self.username,
                "type": "file_message",
                "file": {
                    "type": "file_data",
                    "file_name": self.file_name,
                    "data": str(crypt.encrypt(data), encoding="utf-8")
                }
            }
        file.close()

        time.sleep(0.3)

        message = {
            "username": self.username,
            "type": "file_message",
            "file": {
                "type": "end_file_sending",
                "file_name": self.file_name,
            }
        }
        self.client.send(json.dumps(message).encode("utf-8"))


class ChatUpdating(QThread):

    def __init__(self, messages, client):
        super().__init__()
        self.messages = messages
        self.client = client

    def run(self):
        while True:
            try:
                data = self.client.recv(32768)
                data = json.loads(data.decode("utf-8"))

                if data.get("type") == "login" or data.get("type") == "logout":
                    self.messages.append(f'<html>{data.get("message").get("text")}</html>')

                elif data.get("type") == "message":
                    time = crypt.decrypt((data.get("message").get("time")).encode()).decode()
                    text = crypt.decrypt((data.get("message").get("text")).encode()).decode()
                    self.messages.append(f'<html>[{time}] {data.get("username")}: {text}</html>')

                elif data.get("type") == "file_data":
                    file_name = crypt.decrypt((data.get("file_name")).encode()).decode()
                    with open("data/" + file_name, "ab") as file:
                        file.write(crypt.decrypt(data.get("data").encode()))

                elif data.get("type") == "end_file_sending":
                    import time
                    file_name = crypt.decrypt((data.get("file_name")).encode()).decode()
                    file_path = os.path.abspath(f"data/{file_name}").replace("\\", "/")
                    link = f"<a href = 'file:///{file_path}'>Open.</a>"
                    self.messages.append(f'<html>[{time.strftime("%H:%M:%S")}] {data.get("username")} sent a file - {file_name}. {link}</html>')

            except:
                pass


class PMMessages(QtWidgets.QMainWindow, pms.Ui_MainWindow):
    def __init__(self, client, nick_sendto):
        super(PMMessages, self).__init__()
        self.client = client
        self.nick_sendto = nick_sendto
        self.setWindowIcon(QIcon("icon.ico"))
        self.setupUi(self, "Chat with [" + nick_sendto + "]")
        self.init_ui()

    def init_ui(self):
        self.sendbutton.setEnabled(0)
        self.sendbutton_1.setEnabled(0)
        self.sendbutton.clicked.connect(self.Send)
        self.sendbutton_1.clicked.connect(self.SendFile)
        self.audio_message.clicked.connect(self.AudioMessageWindow)
        self.messages.anchorClicked.connect(QDesktopServices.openUrl)
        loop = Thread(target=self.chat_updating, daemon=True)
        loop.start()

    def closeEvent(self, event):
        if self.status:
            try:
                client.send(("/endPM " + Security.nick_encrypt(self, self.nick_sendto) + " " + str(
                    crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self, nick))), "utf-8")).encode(
                    "utf-8"))
            except:
                pass
        else:
            try:
                client.send(("/cancelPM " + Security.nick_encrypt(self, self.nick_sendto) + " " + str(
                    crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self, nick))), "utf-8")).encode(
                    "utf-8"))
            except:
                pass
        event.accept()
        self.close()

    def AudioMessageWindow(self):
        self.audio_message_app = AudioMessage(self.nick_sendto)
        self.audio_message_app.show()

    def Send(self):
        if not re.search("(\w+)", self.sendText.text()) or not self.status:
            self.sendText.clear()
            return
        if len(self.sendText.text()) > 100:
            self.sendText.clear()
            QMessageBox.warning(self, "Error", "Your message is too long.")
            return
        try:
            self.messages.append("<html>[" + time.strftime("%H:%M:%S") + "] You: " + self.sendText.text() + "</html>")
            client.send(("/pm " + Security.nick_encrypt(self, self.nick_sendto) + " " + str(
                crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self, nick))), "utf-8") + " " + str(
                crypt.encrypt(Security.dictTobytes(
                    self, Security.encrypt_AES(self, "[" + time.strftime(
                        "%H:%M:%S") + "] " + nick + ": " + self.sendText.text()))), "utf-8")).encode("utf-8"))
        except:
            pass
        self.sendText.clear()

    def send_file(self):
        selectedfile = QFileDialog.getOpenFileName(self, "Open file", "C:\\", "Any file (*)")
        if selectedfile[0] == "":
            return

        file_name = os.path.split(selectedfile[0])[1]
        client.send(
            ("/privatestartfilesending " + Security.nick_encrypt(self, self.nick_sendto) + " " + file_name).encode(
                "utf-8"))
        time.sleep(0.5)

        fileData = open(selectedfile[0], "rb")
        data = fileData.read(32768)
        while data:
            client.send(data)
            data = fileData.read(32768)
        fileData.close()

        time.sleep(0.2)
        client.send(b"/endfilesending")

        time.sleep(0.5)
        client.send(("/privateafterfilemessage " + Security.nick_encrypt(self, self.nick_sendto) + " " + str(
            crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self, nick))), "utf-8") + " " + str(
            crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self, "[" + time.strftime(
                "%H:%M:%S") + "] " + nick + " sent a file - " + file_name + "."))), "utf-8")).encode("utf-8"))
        self.messages.append("<html>[" + time.strftime("%H:%M:%S") + "] You sent a file - " + file_name + ".</html>")

    def send_file_loop(self):
        pass

    def chat_updating(self):
        global allowPM, newPMMessage
        newPMMessage = ""
        oldPMMessage = ""
        if not self.AcceptPMStatus:
            self.messages.append("<html>Connecting...<html>")
            while not allowPM:
                pass
        allowPM = 0
        self.status = 1
        self.messages.append("<html>Connected.<html>")
        self.sendbutton.setEnabled(1)
        self.sendbutton_1.setEnabled(1)
        self.sendText.returnPressed.connect(self.Send)
        while True:
            if not (oldPMMessage == newPMMessage):
                try:
                    if "/privatemyaudiomessage" in newPMMessage:
                        if Security.decrypt_AES(self, Security.bytesTodict(self, bytes(crypt.decrypt(
                                bytes(re.search("/privatemyaudiomessage (.*) (.*)", newPMMessage).group(1),
                                      encoding='utf8'))))) == self.nick_sendto:
                            self.messages.append("<html>" + Security.decrypt_AES(self, Security.bytesTodict(self, bytes(
                                crypt.decrypt(
                                    bytes(re.search("/privatemyaudiomessage (.*) (.*)", newPMMessage).group(2),
                                          encoding='utf8'))))) + "</html>")
                            oldPMMessage = newPMMessage
                    elif "/privateaudiomessage" in newPMMessage:
                        if Security.decrypt_AES(self, Security.bytesTodict(self, bytes(crypt.decrypt(
                                bytes(re.search("/privateaudiomessage (.*) (.*)", newPMMessage).group(1),
                                      encoding='utf8'))))) == self.nick_sendto:
                            self.messages.append("<html>" + Security.decrypt_AES(self, Security.bytesTodict(self, bytes(
                                crypt.decrypt(bytes(re.search("/privateaudiomessage (.*) (.*)", newPMMessage).group(2),
                                                    encoding='utf8'))))) + " <a href = 'file:///" + file_path + "'>Listen.</a></html>")
                            oldPMMessage = newPMMessage
                    elif "/privateafterfilemessage" in newPMMessage:
                        if Security.decrypt_AES(self, Security.bytesTodict(self, bytes(crypt.decrypt(
                                bytes(re.search("/privateafterfilemessage (.*) (.*)", newPMMessage).group(1),
                                      encoding='utf8'))))) == self.nick_sendto:
                            self.messages.append("<html>" + Security.decrypt_AES(self, Security.bytesTodict(self, bytes(
                                crypt.decrypt(
                                    bytes(re.search("/privateafterfilemessage (.*) (.*)", newPMMessage).group(2),
                                          encoding='utf8'))))) + " <a href = 'file:///" + file_path + "'>Open.</a></html>")
                            oldPMMessage = newPMMessage
                    elif "/endPM" in newPMMessage:
                        if Security.decrypt_AES(self, Security.bytesTodict(self, bytes(crypt.decrypt(
                                bytes(re.search("/endPM (.*)", newPMMessage).group(1),
                                      encoding='utf8'))))) == self.nick_sendto:
                            self.messages.append(self.nick_sendto + " has left.")
                            self.sendbutton.setEnabled(0)
                            self.sendbutton_1.setEnabled(0)
                            self.status = 0
                            break
                    elif "/pm" in newPMMessage:
                        if Security.decrypt_AES(self, Security.bytesTodict(self, bytes(crypt.decrypt(
                                bytes(re.search("/pm (.*) (.*)", newPMMessage).group(1),
                                      encoding='utf8'))))) == self.nick_sendto:
                            self.messages.append("<html>" + Security.decrypt_AES(self, Security.bytesTodict(self, bytes(
                                crypt.decrypt(bytes(re.search("/pm (.*) (.*)", newPMMessage).group(2),
                                                    encoding='utf8'))))) + "</html>")
                            oldPMMessage = newPMMessage
                except:
                    pass


class AudioMessage(QtWidgets.QMainWindow, audio_message.Ui_MainWindow):
    def __init__(self, nick_sendto):
        super(AudioMessage, self).__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        if nick_sendto == "":
            self.privateStatus = 0
            self.setupUi(self, "Audio")
        else:
            self.nick_sendto = nick_sendto
            self.privateStatus = 1
            self.setupUi(self, "Audio to [" + nick_sendto + "]")
        self.init_ui()

    def init_ui(self):
        self.listen.setEnabled(0)
        self.send.setEnabled(0)
        self.record.clicked.connect(self.Record)
        self.listen.clicked.connect(self.Listen)
        self.send.clicked.connect(self.Send)
        self.status = 0

    def closeEvent(self, event):
        event.accept()
        self.close()

    def Record(self):
        self.status = not self.status
        if self.status:
            self.listen.setEnabled(0)
            self.send.setEnabled(0)
            self.record.setText("Stop")
            loop = Thread(target=self.AudioRecording, daemon=True)
            loop.start()
        else:
            self.listen.setEnabled(1)
            self.send.setEnabled(1)
            self.record.setText("Record")

    def AudioRecording(self):
        global file_path, file_name
        file_name = "audio_message_" + str(
            int(time.strftime("%H")) + int(time.strftime("%M")) + int(time.strftime("%j")) + int(
                time.strftime("%S")) + int(time.strftime("%m")) + int(time.strftime("%d"))) + ".wav"
        file_path = os.getcwd().replace("\\", "/") + "/data/" + file_name
        self.messages.append("Recording " + file_name)
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        output=True,
                        frames_per_buffer=1024)
        frames = []
        while self.status:
            data = stream.read(1024)
            frames.append(data)
        self.messages.append("Done.")
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(file_path, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b"".join(frames))
        wf.close()

    def Listen(self):
        global file_path
        os.system('"' + file_path + '"')

    def Send(self):
        global file_path, file_name

        if self.privateStatus:
            client.send(
                ("/privatestartfilesending " + Security.nick_encrypt(self, self.nick_sendto) + " " + file_name).encode(
                    "utf-8"))
        else:
            client.send(("/startfilesending " + file_name).encode("utf-8"))
        time.sleep(0.5)

        fileData = open(file_path, "rb")
        data = fileData.read(32768)
        while data:
            client.send(data)
            data = fileData.read(32768)
        fileData.close()

        time.sleep(0.2)
        client.send(b"/endfilesending")

        time.sleep(0.5)
        if self.privateStatus:
            client.send(("/privatemyaudiomessage " + str(
                crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self, self.nick_sendto))),
                "utf-8") + " " + str(crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self,
                                                                                                   "[" + time.strftime(
                                                                                                       "%H:%M:%S") + "] You sent an audio message - " + file_name + "."))),
                                     "utf-8")).encode("utf-8"))
            client.send(("/privateaudiomessage " + Security.nick_encrypt(self, self.nick_sendto) + " " + str(
                crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self, nick))), "utf-8") + " " + str(
                crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self, "[" + time.strftime(
                    "%H:%M:%S") + "] " + nick + " sent an audio message - " + file_name + "."))), "utf-8")).encode(
                "utf-8"))
        else:
            client.send(("/myaudiomessage " + str(crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self,
                                                                                                                "[" + time.strftime(
                                                                                                                    "%H:%M:%S") + "] You sent an audio message - " + file_name + "."))),
                                                  "utf-8")).encode("utf-8"))
            client.send(("/audiomessage " + str(crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self,
                                                                                                              "[" + time.strftime(
                                                                                                                  "%H:%M:%S") + "] " + nick + " sent an audio message - " + file_name + "."))),
                                                "utf-8")).encode("utf-8"))
        self.close()


class Settings(QtWidgets.QMainWindow, settings.Ui_MainWindow):
    def __init__(self):
        super(Settings, self).__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        global kickedORbanned
        self.save.clicked.connect(self.Save)
        self.clear_cache.clicked.connect(self.Clear_Cache)
        self.old_password.returnPressed.connect(self.Save)
        self.new_password.returnPressed.connect(self.Save)
        if kickedORbanned:
            self.save.setEnabled(0)

    def closeEvent(self, event):
        event.accept()
        self.close()

    def Save(self):
        if self.old_password.text() == self.new_password.text():
            QMessageBox.warning(self, "Error", "The passwords are the same.")
            return
        if nick == "admin":
            client.send(("/changepassword " + Security.admin_encrypt(self, self.old_password.text(),
                                                                     passEncryptKey) + " " + Security.admin_encrypt(
                self, self.new_password.text(), passEncryptKey)).encode("utf-8"))
        else:
            client.send(("/changepassword " + Security.nick_encrypt(self, nick) + " " + Security.pass_encrypt(self,
                                                                                                              self.old_password.text(),
                                                                                                              passEncryptKey) + " " + Security.pass_encrypt(
                self, self.new_password.text(), passEncryptKey)).encode("utf-8"))
        time.sleep(1)
        if changePassStatus == 0:
            QMessageBox.warning(self, "Error", "Check if your old password is correct.")
        else:
            QMessageBox.information(self, "Success", "Your password has been changed.")

    def Clear_Cache(self):
        [f.unlink() for f in Path(os.getcwd().replace("\\", "/") + "/data").glob("*") if f.is_file()]
        QMessageBox.information(self, "Success", "Cache cleared.")


def nick_encrypt(text):
    return hashlib.sha512(text.encode()).hexdigest()


def pass_encrypt(text, text1):
    return hashlib.md5(text.encode()).hexdigest() + hashlib.sha224(text1.encode()).hexdigest()


crypt = Fernet(bytes("EXEiyCREoeTdtftxw3-scOfs9GbDqAVfT1eIxXFUwnc=", "utf-8"))
app = QtWidgets.QApplication([])
auth_app = Authentication()
auth_app.show()
sys.exit(app.exec())
