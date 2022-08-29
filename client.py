import socket
import wave
import base64
import time
# import pickle             # a way of serialized


HEADER = 64                 # every msg header is a 64-byte header telling how big the msg size to the server.
PORT = 5050
FORMAT = 'utf-8'            # you could use any port which is not being used.  # port 8080 is more like the http ports.
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "0.0.0.0"
# "10.111.136.253"   # use your ipv4 address # alternative way # SERVER = socket.gethostbyname("localhost")  # get the ipv4 addess automatically
ADDR = (SERVER, PORT)       # needs a tuple to bind into server


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    """
    come up w ur own way to send the msg.
    you could sen msg in the following format:
    1. utf-8 format string
    2. serializing obj using pickle
    """
    message = str(msg).encode(FORMAT)                   # follow the server's protocol for msg format.
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))   # to make sure the header is 64-bytes long, so we need to pad.

    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))             # 2048 is a large number that we will receive whatever msg is received.


WAV_PATH = 'data/87984097648596_202204032122368798409764859620debacde9b225730fb5e8d9e1cc8071b.amr'
chunk_size = 20
i = 0
start_time = time.time()

with wave.open(WAV_PATH) as wav_file:
    sample_rate_hertz = wav_file.getframerate()

    while i * chunk_size < wav_file.getnframes():
        # Pass chunk by chunk to recognizer
        chunk = wav_file.readframes(chunk_size)
        if not chunk: # ending...
            break
        # serialize data
        data = base64.b64encode(chunk).decode('utf-8')       # client sends this to server
        send(data)

print(time.time()-start_time)
send(DISCONNECT_MESSAGE)