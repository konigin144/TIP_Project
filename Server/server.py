import socket, threading, asyncio, sys, traceback, os, ssl
from multiprocessing import Process
from PyQt5.QtCore import QThread, QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal, QMutex

class Server(QThread):
    update = pyqtSignal()
    def __init__(self, parent=None):
        super(Server, self).__init__()
        self.parent = parent

        self.connections = {}
        self.sock = socket.socket()
        self.cert = os.path.dirname(os.path.abspath(__file__)) + "/cert.pem"
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.context.load_cert_chain(certfile=self.cert)
        self.bindFlag = False
        self.roomNumber = 0
          
    def run(self):
        self.startButton()

    def stop(self):
        self.parent.addLogs('general', "[Room " + str(self.roomNumber) + "]" + " Shutdown")
        for c in self.connections.values():
            self.parent.addLogs('general' ,"[Client] IP: " + str(c.getpeername()[0]) + " Port: " + str(c.getpeername()[1]) + " - Disconnected from Room: " + str(self.roomNumber))
            c.close()
        self.connections.clear()
        self.sock.close()
        self.terminate()
    
    def setParams(self, ipAddr, portNumber):
        self.ip = socket.gethostbyname(ipAddr)
        self.port = int(portNumber)

    def startButton(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.ip, self.port))
            self.bindFlag = True
            self.parent.addLogs('general', "[Room " + str(self.roomNumber) + "]" + " Running on IP: " + self.ip + " - PORT: " + str(self.port))
        except Exception as e:
            self.bindFlag = False
        
        if self.bindFlag:
            self.acceptConnections()
                 
    @pyqtSlot()            
    def acceptConnections(self):
        self.sock.listen(10)
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=self.cert) 
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.set_ciphers('AES256+ECDH:AES256+EDH')

        while True:
            s, addr = self.sock.accept()
            c = self.context.wrap_socket(s, server_side=True)
           
            if self.checkNick(c):
                self.parent.addLogs('general', "[Client] IP: " + str(c.getpeername()[0]) + " - PORT: " + str(c.getpeername()[1]))
                self.parent.addLogs(str(self.roomNumber), "[Client] IP: " + str(c.getpeername()[0]) + " - PORT: " + str(c.getpeername()[1]))
                self.update.emit()
                self.sendNicks()
                t = threading.Thread(target=self.handleClient, args=(c,addr,))
                t.start()
        
    def broadcast(self, c, data):
        for client in self.connections.values():
            if client != self.sock and client != c:
                try:  
                    client.send(data)
                except:
                    pass

    @pyqtSlot()                
    def handleClient(self, c, addr):
        while 1:
            try:
                data = c.recv(1024)
                self.broadcast(c, data)  
            except socket.error:
                self.parent.addLogs('general', "[Client] IP: " + str(c.getpeername()[0]) + " Port: " + str(c.getpeername()[1]) + " - Disconnected from Room: " + str(self.roomNumber))
                self.parent.addLogs(str(self.roomNumber), "[Client] IP: " + str(c.getpeername()[0]) + " Port: " + str(c.getpeername()[1]) + " - Disconnected from Room: " + str(self.roomNumber))
                self.update.emit()
                c.close()
                self.connections = {key:val for key, val in self.connections.items() if val != c}
                self.sendNicks()

    def checkIP(self, ipAddr):
        def partCheck(ipAddr):
            try: return str(int(ipAddr)) == ipAddr and 0 <= int(ipAddr) <= 255
            except: return False
        if ipAddr.count(".") == 3 and all(partCheck(i) for i in ipAddr.split(".")):
            return True
    
    def checkNick(self, c):
        data = c.recv(1024).decode('utf8')
        if "CHECKNICK:" in data:
            if data[11:] not in self.connections.keys():
                self.connections[data[11:]] = c
                c.send(b"ACK")
                return True
            else:
                c.send(b"NAK")
                c.close()
                return False
    
    def sendNicks(self):
        msg = ' '.join(self.connections.keys())
        msg = "LIST: " + msg
        for client in self.connections.values():
            try: 
                client.send(bytes(msg.encode('utf-8')))
            except:
                pass
