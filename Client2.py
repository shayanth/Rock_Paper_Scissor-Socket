
import socket
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from time import sleep
from _thread import *
import threading
import sys

PORT = 5500
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DC"
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = '192.168.1.2'
ADDR = (SERVER,PORT)
CLIENT_LIST_MESSAGE = "!CL"

#################### Socket For Client Created ###################
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
##################################################################

def Recv_data(sock):

    data = b""
    bufsize = 1024
    while True:
        packet = sock.recv(bufsize)
        data += packet
        if len(packet) < bufsize:
            break

    return data.decode(FORMAT)



class Worker(QThread):
    signal = pyqtSignal(str)
    def run(self):
        while True:
            sleep(1)
            self.signal.emit("broadcast")

class GamePanel(QMainWindow):

    def __init__(self):
        super(GamePanel,self).__init__()
        uic.loadUi("GUI.ui",self)
        self.show()
        self.turn = "0#0"
        self.id ="0"
        self.isRunning = True
        self.PaperBtn.clicked.connect(lambda:self.handleClick("paper"))
        self.RockBtn.clicked.connect(lambda:self.handleClick("rock"))
        self.ScissorBtn.clicked.connect(lambda:self.handleClick("scissor"))
        # self.Status.clicked.connect(lambda:self.handleClick("!CL"))
        self.PaperBtn.setEnabled(False)
        self.RockBtn.setEnabled(False)
        self.ScissorBtn.setEnabled(False)
        self.check = 0
        self.players = []
        self.thread = threading.Thread(target = self.connectToServer,args=())
        self.thread.start()
        self.worker = Worker()
        self.worker.signal.connect(self.Signal_Handler)
        self.worker.start()
        
    def setButton(self,status):
        self.PaperBtn.setEnabled(status)
        self.RockBtn.setEnabled(status)
        self.ScissorBtn.setEnabled(status)

    def connectToServer(self):
        while True:
            try:
                msg = Recv_data(client)
                tmp = msg.split("*")
                if tmp:
                    if tmp[0] == "Start":
                        self.id =tmp[1].split("#")[0]
                        self.turn = tmp[1].split("#")[1]
                        self.check = 1
                        print(self.id)
                        print(self.turn)
            except:
                continue

    def Signal_Handler(self):
        if self.check == 1:
            if self.id == self.turn:
                self.setButton(True)
                self.GameChoice.setText("choose your Toy :)")            

    def closeEvent(self,event) :
        send(DISCONNECT_MESSAGE)
        print("session has been ended")
        self.thread.join()
        client.close()

    def handleClick(self,choice):
        if choice == DISCONNECT_MESSAGE:
            send(choice)
        elif choice == CLIENT_LIST_MESSAGE:
            send(choice)

        else:
            self.GameChoice.setText(f"Your choice: {choice}") 
            send(choice)

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)   

def Main():
    app = QApplication([])
    window = GamePanel()
    sys.exit(app.exec_() )   
  

if __name__ == "__main__":
    try:
        client.connect(ADDR)
        client.send(f"Connected from{client.getpeername()}".encode(FORMAT))
    except :
        print("There is an issue in connection")

    Main()
