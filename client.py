import socket
from PyQt5.QtWidgets import *
from PyQt5 import uic

    
# Constants

PORT = 5500
HEADER = 64
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
        self.show()
        self.PaperBtn.clicked.connect(lambda:self.handleClick("paper"))
        self.RockBtn.clicked.connect(lambda:self.handleClick("rock"))
        self.ScissorBtn.clicked.connect(lambda:self.handleClick("scissor"))
        self.Status.clicked.connect(lambda:self.handleClick("!CL"))

    def closeEvent(self,event) :
        send(DISCONNECT_MESSAGE)

    def handleClick(self,choice):
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
            



def Main():

    try:
        client.connect(ADDR)
    except :
        print("There is an issue in connection")
    isStarted = client.recv(1024).decode(FORMAT)
    print(isStarted)
    app = QApplication([])
    window = GamePanel()
    app.exec_()
    window.enableButton(isStarted)


def send(msg):
    
    message = msg.encode(FORMAT)
    msg_length = len(message)

    send_lenght = str(msg_length).encode(FORMAT)
    send_lenght += b' '*(HEADER- len(send_lenght))

    client.send(send_lenght)
    client.send(message)

    print(client.recv(1024).decode(FORMAT))
    if msg == DISCONNECT_MESSAGE:
        client.close()
        print("This session has been ended !")
        

if __name__ == "__main__":
    Main()



    


