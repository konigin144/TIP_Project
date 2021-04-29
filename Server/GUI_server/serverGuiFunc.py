import sys, path, os, asyncio, threading, socket, time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import server
from serverStylesheets import startBtnStartStyle, startBtnStopStyle
from PyQt5 import QtCore, QtGui, QtWidgets

def startTh(self):
    self.logsArea.clear()
    numOfRooms = self.portInput.text()
    port = 29199
    self.clearDropdown()
    for i in range(int(numOfRooms)):
        port += 1
        if self.checkSocket(self.ipInput.text(), port):
            thread = server.Server(parent=self)
            thread.set_params(self.ipInput.text(), port)
            thread.update.connect(self.updateLogs)
            thread.start()
            thread.roomNumber =  i + 1
            self.logsDict[str(i + 1)] = []
            self.threadList.append(thread)
            self.roomsList.append("ROOM " + str((i + 1)) + " - IP: " + self.ipInput.text() + " - PORT: " + str(port))             
    time.sleep(0.1)
    self.fillDropdown(self.roomsList)
    self.updateLogs()

def stopTh(self):
    for t in self.threadList:
        t.stop()
    self.threadList.clear()
    self.clearDropdown()
    tmp = {}
    tmp['general'] = self.logsDict.get('general')
    self.logsDict.clear()
    self.logsArea.clear()
    self.logsDict = tmp
    self.currentLog = 'general'
    self.roomsDropDown.addItem("General info")
    self.updateLogs()

def updateLogs(self):
    tmpList = self.logsDict.get(self.currentLog)
    print("wywolanie logs")
    print(self.logsDict)
    if tmpList != None:
        self.logsArea.clear()
        tmpStr = "\n".join(tmpList)
        self.logsArea.append(tmpStr)

def addLogs(self, key, value):
    self.logsDict.get(key).append(value)

def checkInputs(self):
    if self.checkNumOfRooms(self.portInput.text()) is not True and self.checkIp(self.ipInput.text()) is not True:       
        self.portInput.setText("Wrong number of ports!")
        self.ipInput.setText("Wrong IP address!")     
        return False
    elif self.checkIp(self.ipInput.text()) is not True: 
        self.ipInput.setText("Wrong IP address!")  
        return False
    elif self.checkNumOfRooms(self.portInput.text()) is not True: 
        self.portInput.setText("Wrong number of ports!")
        return False
    return True

def checkIp(self, ip_addr):
    def partCheck(ip_addr):
        try: return str(int(ip_addr)) == ip_addr and 0 <= int(ip_addr) <= 255
        except: return False
    if ip_addr.count(".") == 3 and all(partCheck(i) for i in ip_addr.split(".")):
        return True

def checkNumOfRooms(self, numOfRooms):
    if numOfRooms == "":
        return False
    if all(d.isdigit() for d in numOfRooms) and (int(numOfRooms) >= 1 and int(numOfRooms) <= 10):
        return True
    return False

def checkPort(self, port):
    if port == "":
        return False
    if all(d.isdigit() for d in port) and (int(port) >= 29200 and int(port) <= 65000):
        return True
    return False

def checkSocket(self, ip, port=29200):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, int(port)))
        return True
    except:
        self.addLogs('general', "[Server] Couldn't create socket for given parameters.")
        self.updateLogs()
        return False
    finally:
        s.close()
           
def handleClick(self):
    self.roomsList.clear()
    if self.isActive == False and self.checkInputs():
        if self.checkSocket(self.ipInput.text()):
            self.startTh()
            self.isActive = True
            self.startBtn.setText("STOP")
            self.startBtn.setStyleSheet(startBtnStopStyle)
    elif self.checkInputs():
        self.stopTh()
        self.isActive = False
        self.startBtn.setText("START")
        self.startBtn.setStyleSheet(startBtnStartStyle)

def fillDropdown(self, roomsList):
    self.roomsDropDown.addItems(roomsList)

def clearDropdown(self):
    self.roomsList.clear()
    self.roomsDropDown.clear()
    self.roomsList.append("General info")

def handleItemDropdown(self, txt):
    if txt in self.roomsList:
        key = str((self.roomsList.index(txt)))
        if key == "0":
            self.currentLog = 'general'
            self.updateLogs()
        else:
            self.currentLog = key
            self.updateLogs()
    else:
        self.currentLog = 'general'
        self.updateLogs()
        