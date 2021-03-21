#!/usr/bin/python3

import socket
import threading
import asyncio
from multiprocessing import Process
from PyQt5.QtCore import QThread, QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal, QMutex

class Server(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    flag = True

    def __init__(self):
           super(Server, self).__init__() 
           # self.ip = socket.gethostbyname(socket.gethostname())
           self.connections = []
           self.s = socket.socket()
           self._mutex = QMutex()
           self._running = True
    
    @pyqtSlot()
    def run(self):
        self.start_button()
        self.finished.emit() 

    @pyqtSlot()
    def stop(self):
        print("Stop")
        self._mutex.lock()
        self._running = False
        self._mutex.unlock()
    
    def set_params(self, ip_addr, port_number):
        self.ip = socket.gethostbyname(ip_addr)
        self.port = int(port_number)

    def start_button(self):
        bind_flag = False
        try:
            print(str(self.ip) + " START BUTTON " + str(type(self.ip)))
            print(str(self.port) + " START BUTTON " + str(type(self.port)))
        
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((self.ip, self.port))
            bind_flag = True
            print(bind_flag)
        except:
            print("Couldn't bind to that port")
            bind_flag = False
            print(bind_flag)
        
        if bind_flag == True:
            self.accept_connections()
                 
    def accept_connections(self):
        print(str(self.ip) + " ACCEPT CONN " + str(type(self.ip)))
        print(str(self.port) + " ACCEPT CONN " + str(type(self.port)))
        self.s.listen(10)

        print('Running on IP: ' + self.ip)
        print('Running on port: ' + str(self.port))

        while True:
            c, addr = self.s.accept()
            self.connections.append(c)
            threading.Thread(target=self.handle_client, args=(c,addr,)).start()
     
            # threading.Thread(target=self.handle_client, args=(c,addr,)).start()
         
        
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
                c.close()

    def check_ip(self, ip_addr):
        def partCheck(ip_addr):
            try: return str(int(ip_addr)) == ip_addr and 0 <= int(ip_addr) <= 255
            except: return False
        if ip_addr.count(".") == 3 and all(partCheck(i) for i in ip_addr.split(".")):
            return True

