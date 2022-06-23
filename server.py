from audioop import add
import socket
import threading


PORT = 5500
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = '192.168.1.2'
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DC"
CLIENT_LIST_MESSAGE = "!CL"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn,addr):
    print(f"[NEW CONNECTION {addr} CONNECTED]")
    connected = True
    while connected:
        
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                conn.send("Connection is ended".encode(FORMAT))
                print(f"{addr} has been disconnected")
                continue
            if msg == CLIENT_LIST_MESSAGE:
                print(clients)
            print(f"[{addr}] {msg}")
            conn.send(f"your message was : {msg}".encode(FORMAT))
    conn.close()
    

clients = []

server.listen(2)
print("[STARTING SERVER ...]")
print(f"[LISTENING] Server is listening on {SERVER}")
while True:
    print(server.listen(2))
    conn,addr = server.accept()
    clients.append(addr)
    thread = threading.Thread(target=handle_client,args=(conn,addr))
    thread.start()
    print(f"[ACTIVE CONNECTION : {threading.active_count() - 1}]")

