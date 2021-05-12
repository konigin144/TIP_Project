import socket, threading, pyaudio, ssl
from multiprocessing import Process
from PyQt5.QtCore import QThread, QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal, QMutex

class Client(QThread):
    def __init__(self, parent=None):
        super(Client, self).__init__()       
        self.parent = parent

        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.check_hostname = False
        self.context.verify_mode=ssl.CERT_NONE
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.receiveFlag = True
        self.sendFlag   = True
        
        chunkSize = 1024
        audioFormat = pyaudio.paInt16
        channels = 1
        rate = 20000

        self.p = pyaudio.PyAudio()
        self.playingStream = self.p.open(format=audioFormat, channels=channels, rate=rate, output=True, frames_per_buffer=chunkSize)
        self.recordingStream = self.p.open(format=audioFormat, channels=channels, rate=rate, input=True, frames_per_buffer=chunkSize)

    def run(self):
        self.startButton()
    
    def stop(self):
        self.s.close()
        self.terminate()   
       
    def startButton(self):
        try:  
            self.parent.updateStatus("Trying to connect...")
            self.s = self.context.wrap_socket(self.sock, server_hostname=self.ipAddr)
            self.s.connect((self.ipAddr, self.portNumber))
        except Exception as e:
            self.parent.updateStatus("Couldn't connect to server: " + self.ipAddr + ":" + str(self.portNumber))
       
        resultNick = self.handleNick()
        if resultNick == True:
            self.parent.startBtnChangeStatus(True)
            self.parent.updateStatus("Connected to server: " + self.ipAddr + ":" + str(self.portNumber))
            receiveThread = threading.Thread(target=self.receiveServerData)
            receiveThread.start()
            self.sendDataToServer()
        elif resultNick == False:
            self.parent.updateStatus("Couldn't connect to server: " + self.ipAddr + ":" + str(self.portNumber))
            self.parent.nickInput.setText("This nick exist!")
            self.parent.startBtnChangeStatus(False)
        else:
            self.parent.updateStatus("Couldn't connect to server: " + self.ipAddr + ":" + str(self.portNumber))
            self.parent.startBtnChangeStatus(False)

    def receiveServerData(self):
        while True:
            try:
                data = self.s.recv(1024)
                if bytes("LIST:".encode('utf-8')) in data:
                    self.parent.fillDropdown(data.decode('utf-8'), True)
                else:
                    if self.receiveFlag:
                        self.playingStream.write(data)
            except Exception as e:
                self.handleServerDis()
                break

    def sendDataToServer(self):
        while True:
            try:
                if self.sendFlag:
                    data = self.recordingStream.read(1024)
                    self.s.sendall(data)
            except:
                self.handleServerDis()
                break
    
    def setParams(self, ipAddr, portNumber):
        self.ipAddr = socket.gethostbyname(ipAddr)
        self.portNumber = int(portNumber)

    def handleServerDis(self):
        self.parent.updateStatus("Disconnected - start port is 29200.")
        self.parent.fillDropdown("", False)
        self.parent.startBtnChangeStatus(False)
        self.stop()

    def handleNick(self):
        data = None
        try:
            msg = "CHECKNICK: " + self.parent.nickInput.text()
            self.s.send(bytes(msg.encode('utf-8')))
            data = self.s.recv(1024).decode('utf-8')
        except:
            self.parent.updateStatus("Couldn't connect to server: " + self.ipAddr + ":" + str(self.portNumber))
            return
        finally:
            if data == None:
                return None
            elif "ACK" in data:
                self.parent.fillDropdown(data, False)
                return True
            elif "NAK" in data:
                return False
       