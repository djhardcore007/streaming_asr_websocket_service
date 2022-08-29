import socket
import threading


HEADER = 64                 # every msg header is a 64-byte header telling how big the msg size to the server.
PORT = 5050                 # you could use any port which is not being used.  # port 8080 is more like the http ports.
SERVER = "10.111.136.253"   # use your ipv4 address # alternative way # SERVER = socket.gethostbyname("localhost")  # get the ipv4 addess automatically
ADDR = (SERVER, PORT)       # needs a tuple to bind into server
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET tells we pick ipv4 address, SOCK_STREAM mean we send streaming data.
server.bind(ADDR)


# you could add a list in here that stores all msg received from different ppl.
def handle_client(conn, addr):
    """
    handle a connection for a single client.
    each client uses one thread and would be running concurrently.
    """
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # first msg tells us the length of the msg.
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connect = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT)) # send msg back to the client

    conn.close()


def start():
    """
    set up server for listening
    """
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() # when a connection occurs, it will communicate the conn and addr of the clients to the server
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # this handles multiple clients, and
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}') # tells how many clients are active.


print('[STARTING] starting server is starting...')
start()
