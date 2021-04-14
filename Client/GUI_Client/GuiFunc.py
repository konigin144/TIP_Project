import sys, path, os, asyncio, threading, socket

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtGui import QIcon

import client
from stylesheets import *

def initClient(self):
    self.thread = client.Client(parent=self)

def startTh(self):
    print(self.ipInput.text() + "   " + self.portInput.text())
    self.thread.set_params(self.ipInput.text(), self.portInput.text())
    self.thread.start()

def stopTh(self):
    self.updateStatus("Disconnected")
    self.thread.stop()

def updateStatus(self, msg):
    self.statusBar.setText(msg)

def checkInputs(self):
    if self.checkPort(self.portInput.text()) is not True and self.checkIp(self.ipInput.text()) is not True:  
        self.ipInput.setStyleSheet("color: red")
        self.portInput.setStyleSheet("color: red")      
        self.portInput.setText("Wrong port number!")
        self.ipInput.setText("Wrong IP address!")     
        return False
    elif self.checkIp(self.ipInput.text()) is not True: 
        self.ipInput.setStyleSheet("color: red")   
        self.ipInput.setText("Wrong IP address!")  
        return False
    elif self.checkPort(self.portInput.text()) is not True:
        self.portInput.setStyleSheet("color: red")     
        self.portInput.setText("Wrong port number!")
        return False
    return True

def checkIp(self, ip_addr):
    def partCheck(ip_addr):
        try: return str(int(ip_addr)) == ip_addr and 0 <= int(ip_addr) <= 255
        except: return False
    if ip_addr.count(".") == 3 and all(partCheck(i) for i in ip_addr.split(".")):
        return True

def checkPort(self, port):
    if port == "":
        return False
    if all(d.isdigit() for d in port) and (int(port) >= 1 and int(port) <= 65000):
        return True
    return False

def checkSocket(self, ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, int(port)))
        return True
    except:
        self.updateStatus("Couldn't connect to server: " + ip + " - " + port)
        return False
    finally:
        s.close()
           
def handleClickStartBtn(self):
    if self.isActive == False and self.checkInputs():
        if self.checkSocket(self.ipInput.text(), self.portInput.text()) == True:
            self.startTh()
            self.isActive = True
            self.startBtn.setText("DISCONNECT")
            self.startBtn.setStyleSheet(startBtnStopStyle)
    elif self.checkInputs():
        self.stopTh()
        self.isActive = False
        self.startBtn.setText("CONNECT")
        self.startBtn.setStyleSheet(startBtnStartStyle)

def handleMicroBtn(self):
    if self.thread.send_flag == True:
        self.thread.send_flag = False
        self.micBtn.setIcon(QIcon(self.imgPath + "mic_off.png"))
        self.micBtn.setStyleSheet(micBtnStyle)
    else:
        self.thread.send_flag = True
        self.micBtn.setIcon(QIcon(self.imgPath + "mic_on.png"))
        self.micBtn.setStyleSheet(micBtnStyle)
    
def handleSpeakerBtn(self):
    if self.thread.recive_flag == True:
        self.thread.recive_flag = False
        self.spkBtn.setIcon(QIcon(self.imgPath + "speaker_off.png"))
        self.spkBtn.setStyleSheet(spkBtnStyle)
    else:
        self.thread.recive_flag = True
        self.spkBtn.setIcon(QIcon(self.imgPath + "speaker_on.png"))
        self.spkBtn.setStyleSheet(spkBtnStyle)