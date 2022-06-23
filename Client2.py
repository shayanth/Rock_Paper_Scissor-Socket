from concurrent.futures import thread
import socket
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading

PORT = 5500
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DC"
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = '192.168.1.2'
ADDR = (SERVER,PORT)

#################### Socket For Client Created ###################
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
##################################################################


class GamePanel(QMainWindow):
    def __init__(self):
        super(GamePanel,self).__init__()
        uic.loadUi("GUI.ui",self)
        self.thread = QThreadPool()
        self.show()
        self.PaperBtn.clicked.connect(lambda:self.handleClick("paper"))
        self.RockBtn.clicked.connect(lambda:self.handleClick("rock"))
        self.ScissorBtn.clicked.connect(lambda:self.handleClick("scissor"))
        self.Status.clicked.connect(lambda:self.handleClick("!CL"))
        self.PaperBtn.setEnabled(False)
        self.RockBtn.setEnabled(False)
        self.ScissorBtn.setEnabled(False)
        self.thread.started.connect(self.Reciver)
        self.Reciver()

        
    def closeEvent(self,event) :
        send(DISCONNECT_MESSAGE)
        print("session has been ended")
        client.close()

    def handleClick(self,choice):
        if choice == DISCONNECT_MESSAGE:
            send(choice)
        else:
            self.GameChoice.setText(f"Your choice: {choice}") 
            send(choice)

    def enableButton(self,isStarted):
        if isStarted == "False":
            self.PaperBtn.setEnabled(False)
            self.RockBtn.setEnabled(False)
            self.ScissorBtn.setEnabled(False)
        else:
            self.PaperBtn.setEnabled(True)
            self.RockBtn.setEnabled(True)
            self.ScissorBtn.setEnabled(True)

    def Reciver(self):
        isStarted = "False"
        while isStarted == "False" :
            isStarted = client.recv(1024).decode(FORMAT)
            self.enableButton(isStarted)


def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)   

def Main():
    app = QApplication([])
    window = GamePanel()
    app.exec_()    
    
    # t.daemon =True
    # t.start()
    

    

if __name__ == "__main__":
    try:
        client.connect(ADDR)
    except :
        print("There is an issue in connection")

    Main()
