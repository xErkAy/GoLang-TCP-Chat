import sys
import random
import socket
import time
import configparser
import os.path
import os
import json
import base64
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
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from PyQt6.QtGui import QIcon, QDesktopServices

users_response = []


class Auth(QtWidgets.QMainWindow, auth_gui.Ui_MainWindow):
    def __init__(self):
        super(Auth, self).__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setupUi(self)
        self.init_UI()

    def init_UI(self):
        global auth_key, key, crypt, lastUsedName
        try:
            config = configparser.ConfigParser()
            config.read("settings.ini")
            lastUsedName = config.get("settings", "last_used_name")
            if lastUsedName != "0":
                self.name.setText(lastUsedName)
        except:
            pass
        self.log_in.clicked.connect(self.Log_in)
        self.name.returnPressed.connect(self.Log_in)
        self.password.returnPressed.connect(self.Log_in)
        self.sign_up.clicked.connect(self.Sign_up)
        key = "nLsAq81xXqmU7hF"
        crypt = Fernet(bytes("EXEiyCREoeTdtftxw3-scOfs9GbDqAVfT1eIxXFUwnc=", "utf-8"))

    def generateHashPassword(self):
        alphabet = "ab7cdefg!h4ijklmn-opqrstuvwxy_235zABC?DEFGHI.JKLMNOPQRSTUVWXYZ16890"
        result = ""
        for i in range(50):
            result += alphabet[random.randint(0, 65)]
        return hashlib.sha224(
            hashlib.md5(hashlib.sha512(result.encode()).hexdigest().encode()).hexdigest().encode()).hexdigest()

    def Log_in(self):
        global client, nick, passEncryptKey

        try:
            config = configparser.ConfigParser()
            config.read("settings.ini")
            passEncryptKey = config.get("settings", "user_password_encrypt_key")
        except:
            QMessageBox.warning(self, "Error", "Contact your administrator to solve this problem.")
            return

        if passEncryptKey == "0":
            file = open("settings.ini", "wt")
            config.set("settings", "user_password_encrypt_key", self.generateHashPassword())
            config.write(file)
            file.close()

        if not re.search("(\w+)", self.name.text()) or not re.search("(\w+)", self.password.text()):
            QMessageBox.warning(self, "Error", "Enter your username and password.")
            return
        nick = self.name.text()

        file = open("settings.ini", "wt")
        config.set("settings", "last_used_name", nick)
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
            "username": Security.nick_encrypt(self, nick),
            "password": Security.pass_encrypt(self, self.password.text(), passEncryptKey)
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

        self.chat_app = Chat()
        self.close()
        self.chat_app.show()

    def Sign_up(self):
        try:
            config = configparser.ConfigParser()
            config.read("settings.ini")
            passEncryptKey = config.get("settings", "user_password_encrypt_key")
        except:
            QMessageBox.warning(self, "Error", "Contact your administrator to solve this problem.")
            return

        if passEncryptKey == "0":
            file = open("settings.ini", "wt")
            config.set("settings", "user_password_encrypt_key", self.generateHashPassword())
            config.write(file)
            file.close()
            passEncryptKey = config.get("settings", "user_password_encrypt_key")

        if not re.search("(\w+)", self.name.text()) or not re.search("(\w+)", self.password.text()):
            QMessageBox.warning(self, "Error", "Enter your name and password.")
            return

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 8080))
        except:
            QMessageBox.warning(self, "Error", "The connection has been failed.")
            return

        message = {
            "type": "registration",
            "username": Security.nick_encrypt(self, self.name.text()),
            "password": Security.pass_encrypt(self, self.password.text(), passEncryptKey)
        }
        client.send(json.dumps(message).encode("utf-8"))
        try:
            data = client.recv(1024)
            if data == b'1':
                QMessageBox.information(self, "Success", "The user has been created.")
                client.close()
            elif data == b'0':
                QMessageBox.warning(self, "Error", "This user already exists."
                                                   "\nTry to use a different name.")
                client.close()
        except:
            QMessageBox.warning(self, "Error", "The connection has been failed.")
            client.close()


class Chat(QtWidgets.QMainWindow, main_gui.Ui_MainWindow):
    def __init__(self):
        super(Chat, self).__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setupUi(self, "Chat [" + nick + "]")
        self.init_UI()

    def init_UI(self):
        self.sendbutton.clicked.connect(self.SendText)
        self.sendbutton_1.clicked.connect(self.SendFile)
        self.audio_message.clicked.connect(self.AudioMessageWindow)
        self.users_online.clicked.connect(self.SendPMMessage)
        self.sendText.returnPressed.connect(self.SendText)
        self.settings.clicked.connect(self.SettingsWindow)
        self.messages.anchorClicked.connect(QDesktopServices.openUrl)

        client.send((nick + " connected to the server!").encode("utf-8"))
        self.messages.append("<html>You connected to the server.</html>")
        self.messages.repaint()

        loop = Thread(target=self.chat_updating, daemon=True)
        loop.start()

    def AudioMessageWindow(self):
        self.audio_message_app = AudioMessage("")
        self.audio_message_app.show()

    def SettingsWindow(self):
        self.settings_app = Settings()
        self.settings_app.show()

    def closeEvent(self, event):
        try:
            message = {
                "type": "logout",
                "message": {
                    "text": nick + " disconnected from the server!",
                }
            }
            client.send(json.dumps(message).encode("utf-8"))
            client.close()
        except:
            pass
        event.accept()
        exit(0)

    def SendPMMessage(self):
        global nick_sendto
        nick_sendto = self.users_online.selectedIndexes()[0].data()
        if nick_sendto == "Users online:" or nick_sendto == "admin" or nick_sendto == nick or nick == "admin":
            return
        if nick_sendto in users_response:
            client.send(("/acceptPM " + Security.nick_encrypt(self, nick_sendto) + " " + str(
                crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self, nick))), "utf-8")).encode("utf-8"))
            users_response.remove(nick_sendto)
            AcceptPMStatus = 1
        else:
            client.send(("/startPM " + Security.nick_encrypt(self, nick_sendto) + " " + str(
                crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self, nick))), "utf-8")).encode("utf-8"))
            AcceptPMStatus = 0

        self.pmmessage_app = PMMessages(AcceptPMStatus, nick_sendto)
        self.pmmessage_app.show()

    def SendText(self):
        global kickedORbanned
        if kickedORbanned:
            return
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
                "username": nick,
                "type": "message",
                "message": {
                    "text": str(crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self, "[" +
                                                                                              time.strftime(
                                                                                                  "%H:%M:%S") + "] " + nick + ": " + self.sendText.text()))),
                                "utf-8"),
                }
            }
            client.send(json.dumps(message).encode("utf-8"))
        except:
            pass
        self.sendText.clear()

    def SendFile(self):
        selectedfile = QFileDialog.getOpenFileName(self, "Open file", "C:\\", "Any file (*)")
        if selectedfile[0] == "":
            return

        if os.path.getsize(selectedfile[0]) > 1073741824:
            QMessageBox.warning(self, "Error", "Your file is too big. (max = 1 Gb)")
            return

        file_name = os.path.split(selectedfile[0])[1]
        client.send(("/startfilesending " + file_name).encode("utf-8"))
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
        client.send(("/afterfilemessage " + str(crypt.encrypt(Security.dictTobytes(self, Security.encrypt_AES(self, "["
                                                                                                              + time.strftime(
            "%H:%M:%S") + "] " + nick + " sent a file - " + file_name + "."))), "utf-8")).encode("utf-8"))
        self.messages.append("<html>[" + time.strftime("%H:%M:%S") + "] You sent a file - " + file_name + ".</html>")

    def chat_updating(self):
        global changePassStatus, file_path, nick_sendto, allowPM, newPMMessage, kickedORbanned
        kickedORbanned = 0
        changePassStatus = 0
        allowPM = 0
        newPMMessage = ""
        while True:
            try:
                data = client.recv(32768)
                print(data)
                if "/changepassword" in data.decode("utf-8"):
                    if "/changepassword 1" in data.decode("utf-8"):
                        changePassStatus = 1
                    elif "/changepassword 0" in data.decode("utf-8"):
                        changePassStatus = 0
                elif "/usersOnline" in data.decode("utf-8"):
                    self.users_online.clear()
                    [self.users_online.addItem(i) for i in
                     re.search("/usersOnline (.*)", data.decode("utf-8")).group(1).split("|")]
                elif "/startfilesending" in data.decode("utf-8"):
                    file_path = os.getcwd().replace("\\", "/") + "/data/" + re.search(
                        "/startfilesending (.*)", data.decode("utf-8")).group(1)
                    recievedfile = open(file_path, "wb")
                    while True:
                        data = client.recv(32768)
                        if data == b"/endfilesending":
                            recievedfile.close()
                            break
                        recievedfile.write(data)
                elif "/privatestartfilesending" in data.decode("utf-8"):
                    file_path = os.getcwd().replace("\\", "/") + "/data/" + re.search(
                        "/privatestartfilesending (.*)", data.decode("utf-8")).group(1)
                    recievedfile = open(file_path, "wb")
                    while True:
                        data = client.recv(32768)
                        if data == b"/endfilesending":
                            recievedfile.close()
                            break
                        recievedfile.write(data)
                elif "/myaudiomessage" in data.decode("utf-8"):
                    self.messages.append("<html>" + Security.decrypt_AES(self, Security.bytesTodict(self, bytes(
                        crypt.decrypt(bytes(re.search("/myaudiomessage (.*)", data.decode("utf-8")).group(1),
                                            encoding='utf8'))))) + "</html>")
                elif "/audiomessage" in data.decode("utf-8"):
                    try:
                        self.messages.append("<html>" + Security.decrypt_AES(self, Security.bytesTodict(self, bytes(
                            crypt.decrypt(bytes(re.search("/audiomessage (.*)", data.decode("utf-8")).group(1),
                                                encoding='utf8'))))) + " <a href = 'file:///" + file_path + "'>Listen.</a></html>")
                    except:
                        pass
                elif "/afterfilemessage" in data.decode("utf-8"):
                    try:
                        self.messages.append("<html>" + Security.decrypt_AES(self, Security.bytesTodict(self, bytes(
                            crypt.decrypt(bytes(re.search("/afterfilemessage (.*)", data.decode("utf-8")).group(1),
                                                encoding='utf8'))))) +
                                             " <a href = 'file:///" + file_path + "'>Open.</a></html>")
                    except:
                        pass
                elif "/message" in data.decode("utf-8"):
                    try:
                        self.messages.append("<html>" + Security.decrypt_AES(self, Security.bytesTodict(self,
                                                                                                        bytes(
                                                                                                            crypt.decrypt(
                                                                                                                bytes(
                                                                                                                    re.search(
                                                                                                                        "/message (.*)",
                                                                                                                        data.decode(
                                                                                                                            "utf-8")).group(
                                                                                                                        1),
                                                                                                                    encoding='utf8'))))) + "</html>")
                    except:
                        pass
                elif "/startPM" in data.decode("utf-8"):
                    try:
                        users_response.append(Security.decrypt_AES(self, Security.bytesTodict(self,
                                                                                              bytes(crypt.decrypt(bytes(
                                                                                                  re.search(
                                                                                                      "/startPM (.*)",
                                                                                                      data.decode(
                                                                                                          "utf-8")).group(
                                                                                                      1),
                                                                                                  encoding='utf8'))))))
                        self.messages.append("<html>" + Security.decrypt_AES(self, Security.bytesTodict(self,
                                                                                                        bytes(
                                                                                                            crypt.decrypt(
                                                                                                                bytes(
                                                                                                                    re.search(
                                                                                                                        "/startPM (.*)",
                                                                                                                        data.decode(
                                                                                                                            "utf-8")).group(
                                                                                                                        1),
                                                                                                                    encoding='utf8'))))) + " wants to send you a message.</html>")
                    except:
                        pass
                elif "/acceptPM" in data.decode("utf-8"):
                    try:
                        if nick_sendto == Security.decrypt_AES(self, Security.bytesTodict(self, bytes(crypt.decrypt(
                                bytes(re.search("/acceptPM (.*)", data.decode("utf-8")).group(1), encoding='utf8'))))):
                            allowPM = 1
                    except:
                        pass
                elif "/cancelPM" in data.decode("utf-8"):
                    try:
                        users_response.remove(Security.decrypt_AES(self, Security.bytesTodict(self, bytes(crypt.decrypt(
                            bytes(re.search("/cancelPM (.*)", data.decode("utf-8")).group(1), encoding='utf8'))))))
                    except:
                        pass
                elif "/pm" in data.decode("utf-8") or "/endPM" in data.decode(
                        "utf-8") or "/privateafterfilemessage" in data.decode(
                        "utf-8") or "/privateaudiomessage" in data.decode(
                        "utf-8") or "/privatemyaudiomessage" in data.decode("utf-8"):
                    newPMMessage = data.decode("utf-8")
                elif "/kick" in data.decode("utf-8") or "/ban" in data.decode("utf-8"):
                    kickedORbanned = 1
                    self.sendbutton.setEnabled(0)
                    self.sendbutton_1.setEnabled(0)
                    self.audio_message.setEnabled(0)
                    self.users_online.setEnabled(0)
                    client.send((nick + " disconnected from the server!").encode("utf-8"))
                    client.close()
                    self.messages.append(
                        "<html>[" + time.strftime("%H:%M:%S") + "] You have been kicked by admin.</html>")
                    break
            except:
                pass


class PMMessages(QtWidgets.QMainWindow, pms.Ui_MainWindow):
    def __init__(self, AcceptPMStatus, nick_sendto):
        super(PMMessages, self).__init__()
        self.nick_sendto = nick_sendto
        self.AcceptPMStatus = AcceptPMStatus
        self.status = 0
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

    def SendFile(self):
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


class Security:
    def dictTobytes(self, text):
        return base64.b64encode(str(text).encode('ascii'))

    def bytesTodict(self, text):
        ascii_msg = base64.b64decode(text).decode('ascii')
        ascii_msg = ascii_msg.replace("'", "\"")
        return json.loads(ascii_msg)

    def encrypt_AES(self, text):
        salt = get_random_bytes(AES.block_size)
        private_key = hashlib.scrypt(
            key.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
        cipher_config = AES.new(private_key, AES.MODE_GCM)
        cipher_text, tag = cipher_config.encrypt_and_digest(bytes(text, 'utf-8'))
        return {
            'cipher_text': b64encode(cipher_text).decode('utf-8'),
            'salt': b64encode(salt).decode('utf-8'),
            'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
            'tag': b64encode(tag).decode('utf-8')
        }

    def decrypt_AES(self, text):
        salt = b64decode(text['salt'])
        cipher_text = b64decode(text['cipher_text'])
        nonce = b64decode(text['nonce'])
        tag = b64decode(text['tag'])
        private_key = hashlib.scrypt(
            key.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(cipher_text, tag)
        return bytes.decode(decrypted)

    def nick_encrypt(self, text):
        return hashlib.md5(hashlib.sha256(hashlib.sha1(hashlib.sha384(hashlib.md5(hashlib.sha512(
            text.encode()).hexdigest().encode()).hexdigest().encode()).hexdigest().encode()).hexdigest().encode()).
                           hexdigest().encode()).hexdigest()

    def pass_encrypt(self, text, text1):
        return hashlib.sha1(hashlib.md5(hashlib.sha224(
            hashlib.md5(hashlib.sha1(hashlib.sha256(hashlib.md5(hashlib.sha512(hashlib.md5(text.encode()).
                                                                               hexdigest().encode()).hexdigest().encode()).hexdigest().encode()).hexdigest().encode()).hexdigest().
                        encode()).hexdigest().encode() + text1.encode()).hexdigest().encode()).hexdigest().encode()).hexdigest()

    def admin_encrypt(self, text, text1):
        return hashlib.md5(hashlib.sha1(hashlib.sha224(
            hashlib.sha512(hashlib.md5(hashlib.sha256(hashlib.sha224(hashlib.sha512(hashlib.md5(text.encode()).
                                                                                    hexdigest().encode()).hexdigest().encode()).hexdigest().encode()).hexdigest().encode()).hexdigest().
                           encode()).hexdigest().encode() + text1.encode()).hexdigest().encode()).hexdigest().encode()).hexdigest()


app = QtWidgets.QApplication([])
auth_app = Auth()
auth_app.show()
sys.exit(app.exec())