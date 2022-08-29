import argparse
import base64
import json
import time
from pathlib import Path
import wave
import socket
import threading


HEADER = 64               # every msg header is a 64-byte header telling how big the msg size to the server.
PORT = 5050                 # you could use any port which is not being used.  # port 8080 is more like the http ports.
SERVER = "0.0.0.0"
# "10.111.136.253"   # use your ipv4 address # alternative way # SERVER = socket.gethostbyname("localhost")  # get the ipv4 addess automatically
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
                connected = False

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


# import torch

# from models import frames_to_tensor, ASRInference
# DEVICE = device = f"cuda:0" if torch.cuda.is_available() else "cpu"
# HUGGINGFACE_FOLDER = 'models/huggingface-hub-ciempiess16k'
# MODEL_PATH = 'models/best_model.tar'
# TARGET_SAMPLING_RATE = 16000
# DURATION = 3

# asr = ASRInference(device=DEVICE, huggingface_folder=HUGGINGFACE_FOLDER, model_path=MODEL_PATH, target_sampling_rate=TARGET_SAMPLING_RATE)
# audio_bytes_buffer = []
# buffer_size = DURATION * TARGET_SAMPLING_RATE           # num frames to receive
# i = 0
# while i < buffer_size:
#     print(i)
#     msg_length = conn.recv(HEADER).decode(FORMAT)       # first msg tells us the length of the msg.
#     if msg_length:
#         msg_length = int(msg_length)
#         msg = conn.recv(msg_length).decode(FORMAT)      # receive str
#         audio_bytes = base64.b64decode(bytes(msg, 'utf-8'))  # turn str to bytes
#         audio_bytes_buffer.append(audio_bytes)
#         i += msg_length
#         if msg == DISCONNECT_MESSAGE:
#             connected = False
#             break

# frames = b''.join(audio_bytes_buffer)                   # recvall
# print(f"[{addr}] audio_chunk")
# audio_chunk = frames_to_tensor(frames, TARGET_SAMPLING_RATE, TARGET_SAMPLING_RATE)
# print(audio_chunk.shape)
# partial_transcript = asr.transcribe(audio_chunk)
# print(f'[TRANSCRIBING] {partial_transcript}')