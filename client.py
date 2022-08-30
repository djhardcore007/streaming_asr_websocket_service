import socket
import wave
import time


PORT = 5050
DISCONNECT_MESSAGE = b"!DISCONNECT"
SERVER = "0.0.0.0"
# "10.111.136.253"   # use your ipv4 address # alternative way # SERVER = socket.gethostbyname("localhost")  # get the ipv4 addess automatically
ADDR = (SERVER, PORT)       # needs a tuple to bind into server


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg: bytes):
    """
    come up w ur own way to send the msg.
    you could sen msg in the following format:
    1. utf-8 format string
    2. serializing obj using pickle
    """
    client.sendall(msg)                                 # avoid all the hassle and sendall bytes


WAV_PATH = 'data/87984097648596_202204032122368798409764859620debacde9b225730fb5e8d9e1cc8071b.amr'
chunk_size = 800

i = 0
start_time = time.time()

with wave.open(WAV_PATH) as wav_file:
    sample_rate_hertz = wav_file.getframerate()

    while i * chunk_size < wav_file.getnframes():
        # Pass chunk by chunk to recognizer
        chunk = wav_file.readframes(chunk_size)
        if not chunk: # ending...
            break
        send(chunk)          # send audio directly


print(time.time()-start_time)
send(DISCONNECT_MESSAGE)