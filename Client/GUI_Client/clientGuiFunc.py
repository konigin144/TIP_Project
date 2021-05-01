import sys, path, os, asyncio, threading, socket, time
from usernames import is_safe_username

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtGui import QIcon

import client
from clientStylesheets import *

def initClient(self):
    self.thread = client.Client(parent=self)

def startTh(self):
    self.initClient()
    self.thread.setParams(self.ipInput.text(), self.portInput.text())
    self.thread.start()

def stopTh(self):
    self.updateStatus("Disconnected")
    self.thread.stop()

def updateStatus(self, msg):
    self.usersList[0] = msg
    self.statusBar.clear()
    self.statusBar.addItems(self.usersList)

def checkInputs(self):
    if self.checkPort(self.portInput.text()) is not True and self.checkIp(self.ipInput.text()) is not True and self.checkNickname(self.nickInput.text()) is not True:    
        self.portInput.setText("Wrong port number!")
        self.ipInput.setText("Wrong IP address!")
        self.nickInput.setText("Wrong nickname!")     
        return False
    elif self.checkIp(self.ipInput.text()) is not True: 
        self.ipInput.setText("Wrong IP address!")  
        return False
    elif self.checkPort(self.portInput.text()) is not True:  
        self.portInput.setText("Wrong port number!")
        return False
    elif self.checkNickname(self.nickInput.text()) is not True:
        self.nickInput.setText("Wrong nickname!")     
        return False
    return True

def checkIp(self, ipAddr):
    def partCheck(ipAddr):
        try: return str(int(ipAddr)) == ipAddr and 0 <= int(ipAddr) <= 255
        except: return False
    if ipAddr.count(".") == 3 and all(partCheck(i) for i in ipAddr.split(".")):
        return True

def checkPort(self, port):
    if port == "":
        return False
    if all(d.isdigit() for d in port) and (int(port) >= 29200 and int(port) <= 65000):
        return True
    return False

def checkNickname(self, nickname):
    return is_safe_username(nickname)

def checkSocket(self, ip, port):
    connectionFlag = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((ip, int(port)))
        self.updateStatus("Couldn't connect to server: " + ip + " - " + port)
        connectionFlag = False
    except:
        connectionFlag = True
    finally:
        s.close()
        return connectionFlag
           
def handleClickStartBtn(self):
    if self.isActive == False and self.checkInputs():
        if self.checkSocket(self.ipInput.text(), self.portInput.text()) == True:
            self.startTh()
            if self.muteMic_flag:
                self.thread.sendFlag = False
            if self.muteSpk_flag:
                self.thread.receiveFlag = False
    elif self.checkInputs():
        self.stopTh()
        self.startBtnChangeStatus(False)

def startBtnChangeStatus(self, status): # Status TRUE - change to disconnect, Status FALSE - change to connect
    if status:
        self.isActive = True
        self.startBtn.setText("DISCONNECT")
        self.startBtn.setStyleSheet(startBtnStopStyle)
    else:
        self.isActive = False
        self.startBtn.setText("CONNECT")
        self.startBtn.setStyleSheet(startBtnStartStyle)

def handleMicroBtn(self):
    if self.thread.sendFlag == True:
        self.thread.sendFlag = False
        self.muteMic_flag = True
        self.micBtn.setIcon(QIcon(self.imgPath + "mic_off.png"))
        self.micBtn.setStyleSheet(micBtnStyle)
    else:
        self.thread.sendFlag = True
        self.muteMic_flag = False
        self.micBtn.setIcon(QIcon(self.imgPath + "mic_on.png"))
        self.micBtn.setStyleSheet(micBtnStyle)
    
def handleSpeakerBtn(self):
    if self.thread.receiveFlag == True:
        self.thread.receiveFlag = False
        self.muteSpk_flag = True
        self.spkBtn.setIcon(QIcon(self.imgPath + "speaker_off.png"))
        self.spkBtn.setStyleSheet(spkBtnStyle)
    else:
        self.thread.receiveFlag = True
        self.muteSpk_flag = False
        self.spkBtn.setIcon(QIcon(self.imgPath + "speaker_on.png"))
        self.spkBtn.setStyleSheet(spkBtnStyle)

def fillDropdown(self, usersString):
    usersList = usersString[6:].split(" ")
    firstElem = self.usersList[0]
    self.usersList.clear()
    self.statusBar.clear()
    self.usersList.append(firstElem)
    if usersList[0] != "":
        self.usersList += usersList
    self.statusBar.addItems(self.usersList)

def preventDropdownChange(self):
    self.statusBar.setCurrentIndex(0)