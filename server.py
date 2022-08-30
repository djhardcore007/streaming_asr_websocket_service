import socket
import threading

import torch

from models import frames_to_tensor, ASRInference


DEVICE = device = f"cuda:0" if torch.cuda.is_available() else "cpu"
HUGGINGFACE_FOLDER = 'models/huggingface-hub-ciempiess16k'
MODEL_PATH = 'models/best_model.tar'
ORI_SR = 8000
TARGET_SAMPLING_RATE = 16000

asr = ASRInference(device=DEVICE, huggingface_folder=HUGGINGFACE_FOLDER, model_path=MODEL_PATH, target_sampling_rate=TARGET_SAMPLING_RATE)

HEADER = 64               # every msg header is a 64-byte header telling how big the msg size to the server.
PORT = 5050                 # you could use any port which is not being used.  # port 8080 is more like the http ports.
SERVER = "0.0.0.0"
# "10.111.136.253"   # use your ipv4 address # alternative way # SERVER = socket.gethostbyname("localhost")  # get the ipv4 addess automatically
ADDR = (SERVER, PORT)       # needs a tuple to bind into server
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = b"!DISCONNECT"

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
    chunk_size = 800
    buffer = []
    i = 0
    while connected:
        while connected and i < 3 * 8000:
            msg = conn.recv(chunk_size)
            buffer.append(msg)
            i += chunk_size
            if msg == DISCONNECT_MESSAGE:
                connected = False
                break
            # conn.send("Msg received".encode(FORMAT)) # send msg back to the client
        frames = b''.join(buffer)
        if frames:
            audio_window = frames_to_tensor(frames, ORI_SR, TARGET_SAMPLING_RATE)
            partial_transcript = asr.transcribe(audio_window)
            print(f'[TRANSCRIBING] {partial_transcript}')
            conn.send(f"partial_transcript".encode('utf-8')) # send msg back to the client
        i = 0
        buffer = []

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