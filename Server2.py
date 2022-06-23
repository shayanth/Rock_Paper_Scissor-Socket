from pydoc import cli
import socket
import threading
import pickle


PORT = 5500
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
        if len(clients) == 3:
            for client in clients:
                client[0].send("True".encode(FORMAT))

            msg = conn.recv(1024).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                conn.send("Connection is ended".encode(FORMAT))
                print(f"{addr} has been disconnected")
                clients.remove((conn,addr))
                print(clients)
                continue
            if msg == CLIENT_LIST_MESSAGE:
                print(clients)
            print(f"[{addr}] {msg}")
            conn.send(f"your message was : {msg}".encode(FORMAT))
        elif len(clients) > 3:
            connected = False
            conn.send("Game Is Full".encode(FORMAT))
            print(f"{addr} has been disconnected")
            
    conn.close()


clients = set()
pickeled_clients = pickle.dumps(clients)

server.listen(2)
print("[STARTING SERVER ...]")
print(f"[LISTENING] Server is listening on {SERVER}")

while True:
    conn,addr = server.accept()
    clients.add((conn,addr))
    thread = threading.Thread(target=handle_client,args=(conn,addr))
    thread.start()
    print(len(clients))
    print(f"[ACTIVE CONNECTION : {threading.active_count() - 1}]")