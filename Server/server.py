import socket, threading, asyncio, sys, traceback, os
from multiprocessing import Process
from PyQt5.QtCore import QThread, QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal, QMutex

class Server(QThread):
    def __init__(self, parent=None):
        super(Server, self).__init__() 
        self.connections = []
        self.s = socket.socket()
        self.q = list()
        self.isRunning = False
        self.logs = []
        self.parent = parent
        self.bind_flag = False
           
    def run(self):
        self.isRunning = True
        self.start_button()
        print("Serwer startuje")
         
    def stop(self):
        print("Stop")
        self.parent.updateLogs("[Server] Shutdown")
        for c in self.connections:
            self.parent.updateLogs("[Client] IP: " + str(c.getpeername()[0]) + " Port: " + str(c.getpeername()[1]) + " - Disconnected")
            c.close()
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
        except:
            print("Couldn't self.bind to that port")
            self.bind_flag = False
            print(self.bind_flag)
        
        if self.bind_flag:
            self.accept_connections()
                 
    def accept_connections(self):
        print(str(self.ip) + " ACCEPT CONN " + str(type(self.ip)))
        print(str(self.port) + " ACCEPT CONN " + str(type(self.port)))
        self.s.listen(10)

        self.parent.updateLogs('[Server] Running on IP: ' + self.ip)
        self.parent.updateLogs('[Server] Running on port: ' + str(self.port))
        print('[Server] Running on IP: ' + self.ip)
        print('[Server] Running on port: ' + str(self.port))

        while True:
            print("Pan pawel")
            c, addr = self.s.accept()
            self.connections.append(c)
            print("przed nowym wątkiem")
            
            self.parent.updateLogs("[Client] IP: " + str(c.getpeername()[0]) + " Port: " + str(c.getpeername()[1]))
            t = threading.Thread(target=self.handle_client, args=(c,addr,))
            self.q.append(t)
            t.start()
            print("dodano thread")
        
    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:  
                    client.send(data)
                except:
                    pass

    def handle_client(self,c,addr):
        while 1:
            try:
                data = c.recv(1024)
                self.broadcast(c, data)  
            except socket.error:
                self.parent.updateLogs("[Client] IP: " + str(c.getpeername()[0]) + " Port: " + str(c.getpeername()[1]) + " - Disconnected")
                c.close()

    def check_ip(self, ip_addr):
        def partCheck(ip_addr):
            try: return str(int(ip_addr)) == ip_addr and 0 <= int(ip_addr) <= 255
            except: return False
        if ip_addr.count(".") == 3 and all(partCheck(i) for i in ip_addr.split(".")):
            return True