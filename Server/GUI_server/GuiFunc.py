import sys, path, os, asyncio, threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import server

def startTh(self):
    self.thread = server.Server(parent=self)
    self.thread.set_params(self.ipInput.text(), self.portInput.text())
    self.thread.start()

def stopTh(self):
    self.thread.stop()

def updateLogs(self, msg):
        self.logsArea.append(msg)

def checkInputs(self):
    print("przed warunkiem")
    if self.checkPort(self.portInput.text()) is not True and self.checkIp(self.ipInput.text()) is not True:   
            self.portInput.setText("Wrong port number!")
            self.ipInput.setText("Wrong IP address!")      
            return False
    elif self.checkIp(self.ipInput.text()) is not True:           
            self.ipInput.setText("Wrong IP address!")  
            return False
    elif self.checkPort(self.portInput.text()) is not True:
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
    if port is "":
            return False
    if all(d.isdigit() for d in port) and (int(port) >= 1 and int(port) <= 65000):
            return True
    return False