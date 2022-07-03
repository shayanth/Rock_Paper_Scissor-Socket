
import socket
import threading



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

def Recv_data(soc):

    data =""
    bufsize = 1024
    while True:
        packet = soc.recv(bufsize)
        data += packet
        if len(packet) < bufsize:
            break

    return data.decode(FORMAT)


def handle_client(id,conn):
    global turn
    print(f"[NEW CONNECTION {addr} CONNECTED]")
    connected = True
    clients_str = ""
    while connected:
        
        if len(clients) < 3:
            conn.send("SFalse".encode(FORMAT))

        elif len(clients) == 3:
            for cl in clients: 
                clients_str += str(cl)+"*"
            conn.send("STrue".encode(FORMAT))
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
                conn.send(clients_str.encode(FORMAT))
            
            if len(clients) > 3 :
                connected = False
                conn.send("Game Is Full".encode(FORMAT))
                print(f"{addr} has been disconnected")
        else:
            conn.send("Server is Full !!".encode(FORMAT))
            connected = False
    conn.close()





print("[STARTING SERVER ...]")
print(f"[LISTENING] Server is listening on {SERVER}")

while True:
    conn,addr = server.accept()

    if len(clients) >= 3:
        print("server full!")
        conn.close()
        continue
    
    clients.add([players_count ,conn])

    thread = threading.Thread(target=handle_client,args=(players_count,conn))
    thread.start()
    if len(clients) == 3:
            for client in clients:
                con = client[1]
                con.send(("Start*"+str(client[0])+"#"+str(turn)).encode(FORMAT))
            print("[Game Started.]")

    players_count += 1 

    print(f"[ACTIVE CONNECTION : {threading.active_count() - 1}]")