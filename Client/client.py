import socket, threading, pyaudio
from multiprocessing import Process
from PyQt5.QtCore import QThread, QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal, QMutex

class Client(QThread):
    def __init__(self, parent=None):
        super(Client, self).__init__()       
        self.parent = parent
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recive_flag = True
        self.send_flag = True
        
        chunk_size = 1024 # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)

    def run(self):
        self.start_button()
    
    def stop(self):
        self.s.close()
        self.terminate()   
       
    def start_button(self):
        try:  
            self.s.connect((self.ip_addr, self.port_number))
        except:
            self.parent.updateStatus("Couldn't connect to server: " + self.ip_addr + ":" + str(self.port_number))
            print("Couldn't connect to server")

        #   
        if self.handleNick():
            self.parent.startBtnChangeStatus(True)
            self.parent.updateStatus("Connected to server: " + self.ip_addr + ":" + str(self.port_number))
            receive_thread = threading.Thread(target=self.receive_server_data)
            receive_thread.start()
            self.send_data_to_server()
        else:
            self.parent.nickInput.setText("This nick exist!")
            self.parent.startBtnChangeStatus(False)

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                if bytes("L:".encode('utf-8')) in data:
                    self.parent.fillDropdown(data.decode('utf-8'))
                    print(data.decode('utf-8'))
                else:
                    if self.recive_flag:
                        self.playing_stream.write(data)
            except Exception as e:
                print(str(e))
                print("receive")
                self.handleServerDis()
                break

    def send_data_to_server(self):
        while True:
            try:
                if self.send_flag:
                    data = self.recording_stream.read(1024)
                    self.s.sendall(data)
            except:
                self.handleServerDis()
                break
    
    def set_params(self, ip_addr, port_number):
        self.ip_addr = socket.gethostbyname(ip_addr)
        self.port_number = int(port_number)

    def handleServerDis(self):
        self.parent.updateStatus("Disconnected")
        self.parent.fillDropdown("")
        self.parent.startBtnChangeStatus(False)
        self.stop()

    def handleNick(self):
        msg = "N: " + self.parent.nickInput.text()
        self.s.send(bytes(msg.encode('utf-8')))
        data = self.s.recv(1024).decode('utf-8')
        if  "ACK" in data:
            return True
        elif "NAK" in data:
            return False