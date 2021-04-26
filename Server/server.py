import socket, threading, asyncio, sys, traceback, os
from multiprocessing import Process
from PyQt5.QtCore import QThread, QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal, QMutex

class Server(QThread):
    update = pyqtSignal()
    def __init__(self, parent=None):
        super(Server, self).__init__() 
        self.connections = {}
        self.s = socket.socket()
        self.q = list()
        self.isRunning = False
        self.logs = []
        self.parent = parent
        self.bind_flag = False
        self.roomNumber = 0
        self.nickArr = []
           
    def run(self):
        self.isRunning = True
        self.start_button()
        print("Serwer startuje")
         
    def stop(self):
        print("Stop")
        self.parent.addLogs('general', "[Room " + str(self.roomNumber) + "]" + " Shutdown")
        for c in self.connections.values():
            self.parent.addLogs('general' ,"[Client] IP: " + str(c.getpeername()[0]) + " Port: " + str(c.getpeername()[1]) + " - Disconnected from Room: " + str(self.roomNumber))
            c.close()
        self.connections.clear()
        self.s.close()
        self.terminate()
        self.isRunning = False
    
    def set_params(self, ip_addr, port_number):
        self.ip = socket.gethostbyname(ip_addr)
        self.port = int(port_number)

    def start_button(self):
        try:
            print(str(self.ip) + " START BUTTON " + str(type(self.ip)))
            print(str(self.port) + " START BUTTON " + str(type(self.port)))
        
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((self.ip, self.port))
            self.bind_flag = True
            print(self.bind_flag)
            self.parent.addLogs('general', "[Room " + str(self.roomNumber) + "]" + " Running on IP: " + self.ip + " - PORT: " + str(self.port))
        except:
            print("Couldn't self.bind to that port")
            self.bind_flag = False
            print(self.bind_flag)
        
        if self.bind_flag:
            self.accept_connections()
                 
    @pyqtSlot()            
    def accept_connections(self):
        print(str(self.ip) + " ACCEPT CONN " + str(type(self.ip)))
        print(str(self.port) + " ACCEPT CONN " + str(type(self.port)))
        self.s.listen(10)

        print('[Server] Running on IP: ' + self.ip)
        print('[Server] Running on port: ' + str(self.port))

        while True:
            print("Pan pawel")
            c, addr = self.s.accept()
            
            print("przed nowym wątkiem")
           
            if self.checkNick(c):
                self.parent.addLogs('general', "[Client] IP: " + str(c.getpeername()[0]) + " - PORT: " + str(c.getpeername()[1]))
                self.parent.addLogs(str(self.roomNumber), "[Client] IP: " + str(c.getpeername()[0]) + " - PORT: " + str(c.getpeername()[1]))
                self.update.emit()
                self.sendNicks()

                t = threading.Thread(target=self.handle_client, args=(c,addr,))
                self.q.append(t)
                t.start()
                print("dodano thread")
        
    def broadcast(self, sock, data):
        for client in self.connections.values():
            if client != self.s and client != sock:
                try:  
                    client.send(data)
                except:
                    pass

    @pyqtSlot()                
    def handle_client(self,c,addr):
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
                print(c)
                print(str(c)  + " O CHUJ " + str(self.connections))

    def check_ip(self, ip_addr):
        def partCheck(ip_addr):
            try: return str(int(ip_addr)) == ip_addr and 0 <= int(ip_addr) <= 255
            except: return False
        if ip_addr.count(".") == 3 and all(partCheck(i) for i in ip_addr.split(".")):
            return True
    
    def checkNick(self, c):
        data = c.recv(1024).decode('utf8')
        if "N:" in data:
            if data[3:] not in self.connections.keys():
                self.connections[data[3:]] = c
                print(self.connections)
                c.send(b"ACK")
                print(data[3:])
                print("ACK")
                return True
            else:
                c.send(b"NAK")
                print("NAK")
                c.close()
                return False
    
    def sendNicks(self):
        msg = ' '.join(self.connections.keys())
        msg = "L: " + msg
        for client in self.connections.values():
            try: 
                client.send(bytes(msg.encode('utf-8')))
            except:
                pass
