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
players_choice = {}
round = 1
player_scores =[0,0,0]
def Recv_data(soc):

    data =b""
    bufsize = 1024
    while True:
        packet = soc.recv(bufsize)
        data += packet
        if len(packet) < bufsize:
            break

    return data.decode(FORMAT)

def check(ch1,ch2):
    # Rock ch2
    if ch1 == "rock" and ch2 == "rock":
        return 0
    if ch1 == "paper" and ch2 == "rock":
        return 1
    if ch1 == "scissor" and ch2 == "rock":
        return 2

    # scissor ch2
    if ch1 == "rock" and ch2 == "scissor":
        return 1
    if ch1 == "paper" and ch2 == "scissor":
        return 2
    if ch1 == "scissor" and ch2 == "scissor":
        return 0

    #  paper ch2
    if ch1 == "rock" and ch2 == "paper":
        return 2
    if ch1 == "paper" and ch2 == "paper":
        return 0
    if ch1 == "scissor" and ch2 == "paper":
        return 1
    
def Winners(players_choices):
    global player_scores

    if check(players_choices[0],players_choices[1]) == 1:
        player_scores[0] += 1
    elif check(players_choices[0],players_choices[1]) == 2:
        player_scores[1] += 1
    else:
        pass

    if check(players_choices[0],players_choices[2]) == 1:
        player_scores[0] += 1
    elif check(players_choices[0],players_choices[2]) == 2:
        player_scores[2] += 1
    else:
        pass

    if check(players_choices[1],players_choices[2]) == 1:
        player_scores[1] += 1
    elif check(players_choices[1],players_choices[2]) == 2:
        player_scores[2] += 1
    else:
        pass

    return player_scores

        


def handle_client(id,conn):
    global turn
    global players_count
    global players_choice
    print(f"[NEW CONNECTION {addr} CONNECTED]")
    connected = True

    while connected:
            if len(clients)== 0:
                players_count = 0
                turn = 0
                players_choice = {}
                round = 1
                player_scores =[0,0,0]

            msg = Recv_data(conn)
            
            if msg:
                tmp = msg.split("*")
                if tmp[0] == "Next":
                    
                    choice = tmp[1]
                    if turn == id:
                        players_choice[id] = choice
                        print(players_choice)
                        
                        turn += 1
                        if turn == 3:
                            point_list = Winners(players_choice)
                            for client in clients:
                                con = client[1]
                                message = str("winners*"+str(point_list[0])+"$"+str(point_list[1])+"$"+str(point_list[2]))
                                con.send(message.encode(FORMAT))
                            turn = 0

                        print(turn)
                        for client in clients:
                            con = client[1]
                            message = str("continue*"+str(client[0])+"#"+str(turn))
                            con.send(message.encode(FORMAT))
                
                        
                
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    conn.send("Connection is ended".encode(FORMAT))
                    print(f"{addr} has been disconnected")
                    clients.remove((id ,conn))
                    print(clients)
                    continue
                   
    conn.close()





print("[STARTING SERVER ...]")
print(f"[LISTENING] Server is listening on {SERVER}")

while True:
    conn, addr = server.accept()
    if len(clients) == 0:
        players_count = 0
        turn = 0
        players_choice = {}
        round = 1
        player_scores =[0,0,0]
        print("Len 0 executed")

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