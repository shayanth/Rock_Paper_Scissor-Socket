
from ast import arg
from glob import glob
import socket
import threading
from tracemalloc import start



PORT = 5500
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = '192.168.1.2'
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DC"
CLIENT_LIST_MESSAGE = "!CL"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(2)

clients = list()
players_count = 0
turn = 0
players_choice = {}

def Recv_data(soc):

    data =b""
    bufsize = 1024
    while True:
        packet = soc.recv(bufsize)
        data += packet
        if len(packet) < bufsize:
            break

    return data.decode(FORMAT)

def Winners(choices):
    pass


def handle_client(id,conn):
    global turn
    global players_count
    global players_choice
    print(f"[NEW CONNECTION {addr} CONNECTED]")
    connected = True

    while connected:
            msg = Recv_data(conn)
            tmp = msg.split("*")
            if turn == id:
                
            if msg == DISCONNECT_MESSAGE:
                connected = False
                conn.send("Connection is ended".encode(FORMAT))
                print(f"{addr} has been disconnected")
                clients.remove((id ,conn))
                players_count -= 1
                print(clients)
                continue
            if
    conn.close()





print("[STARTING SERVER ...]")
print(f"[LISTENING] Server is listening on {SERVER}")

while True:
    conn, addr = server.accept()
    if len(clients) >= 3:
        print("server full!")
        conn.send("!DC")
        conn.close()
        continue

    threading.Thread(target = handle_client , args=(players_count , conn)).start()
    clients.append((players_count ,conn))
    print(f"[Connecting] Server connected to {addr}")


    if len(clients) == 3:
        print("Loop Started")
        for client in clients:
            con = client[1]
            message = str("Start*"+str(client[0])+"#"+str(turn))
            con.send((message).encode())
        print("[Game Started.]")
    

    print(clients)
    players_count += 1



    print(f"[ACTIVE CONNECTION : {threading.active_count() - 1}]")