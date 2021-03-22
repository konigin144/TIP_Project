#!/usr/bin/python3

import socket
import threading
import asyncio
import sys, traceback, os
from multiprocessing import Process
from PyQt5.QtCore import QThread, QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal, QMutex

class Server(QThread):
    def __init__(self, parent=None):
           super(Server, self).__init__() 
           # self.ip = socket.gethostbyname(socket.gethostname())
           self.connections = []
           self.s = socket.socket()
           self.q = list()
           self.flag = False
           self.logs = []
           self.parent = parent
           
    def run(self):
        self.flag = True
        self.start_button()
    
    def stop(self):
        print("Stop")
        self.parent.updateLogs("[Server] Shutdown")
        for c in self.connections:
            c.close()
        self.s.close()

        self.terminate()
        self.flag = False
    
    def set_params(self, ip_addr, port_number):
        self.ip = socket.gethostbyname(ip_addr)
        self.port = int(port_number)

    def start_button(self):
        bind_flag = False
        try:
            print(str(self.ip) + " START BUTTON " + str(type(self.ip)))
            print(str(self.port) + " START BUTTON " + str(type(self.port)))
        
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((self.ip, self.port))
            bind_flag = True
            print(bind_flag)
        except:
            print("Couldn't bind to that port")
            bind_flag = False
            print(bind_flag)
        
        if bind_flag:
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
            
            t = threading.Thread(target=self.handle_client, args=(c,addr,))
            self.q.append(t)
            t.start()
            # t.daemon = True 
            print("dodano thread")

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





#Zawartość przed kopią
    # finished = pyqtSignal()
    # started = pyqtSignal()
    # progress = pyqtSignal(int)
    # flag = True

    # def __init__(self):
    #        super(Server, self).__init__() 
    #        # self.ip = socket.gethostbyname(socket.gethostname())
    #        self.connections = []
    #        self.s = socket.socket()
    #        self._mutex = QMutex()
    #        self._running = True
    #        self.q = []
           
    
    # @pyqtSlot()
    # def run(self):
    #     self.flag = True
    #     self.start_button()
    #     self.finished.emit()
    
    # @pyqtSlot()
    # def stop(self):
    #     print("Stop")
    #     self.flag = False
    #     self._mutex.lock()
    #     self._running = False
    #     self._mutex.unlock()
    #     self.finished.emit()

    
    # def set_params(self, ip_addr, port_number):
    #     self.ip = socket.gethostbyname(ip_addr)
    #     self.port = int(port_number)

    # def start_button(self):
    #     bind_flag = False
    #     try:
    #         print(str(self.ip) + " START BUTTON " + str(type(self.ip)))
    #         print(str(self.port) + " START BUTTON " + str(type(self.port)))
        
    #         self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         self.s.bind((self.ip, self.port))
    #         bind_flag = True
    #         print(bind_flag)
    #     except:
    #         print("Couldn't bind to that port")
    #         bind_flag = False
    #         print(bind_flag)
        
    #     if bind_flag:
    #         self.accept_connections()
                 
    # def accept_connections(self):
    #     print(str(self.ip) + " ACCEPT CONN " + str(type(self.ip)))
    #     print(str(self.port) + " ACCEPT CONN " + str(type(self.port)))
    #     self.s.listen(10)

    #     print('Running on IP: ' + self.ip)
    #     print('Running on port: ' + str(self.port))

    #     while self.flag == True:
    #         print("Pan pawel")
    #         c, addr = self.s.accept()
    #         self.connections.append(c)
    #         print("przed nowym wątkiem")
    #         self.q.append(threading.Thread(target=self.handle_client, args=(c,addr,)).start())
    #         # t.daemon = True 
    #         print("dodano thread")
              
        
    #     for th in self.q:
    #         print(" usuwam watki")
    #         th.join()

    #         # threading.Thread(target=self.handle_client, args=(c,addr,)).start()
         
        
    # def broadcast(self, sock, data):
    #     for client in self.connections:
    #         if client != self.s and client != sock:
    #             try:  
    #                 client.send(data)
    #             except:
    #                 pass

    # def handle_client(self,c,addr):
    #     while 1:
    #         try:
    #             data = c.recv(1024)
    #             self.broadcast(c, data)  
    #         except socket.error:
    #             c.close()

    # def check_ip(self, ip_addr):
    #     def partCheck(ip_addr):
    #         try: return str(int(ip_addr)) == ip_addr and 0 <= int(ip_addr) <= 255
    #         except: return False
    #     if ip_addr.count(".") == 3 and all(partCheck(i) for i in ip_addr.split(".")):
    #         return True

