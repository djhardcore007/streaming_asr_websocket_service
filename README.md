# Python Socket Server Example

This repo provices a simple socket server example for sending: string and audio data.

## Usage
Setup
```
conda create -n socket python=3.7.9
conda activate socket
pip install -r requirements.txt
```

Run the server
```
python server.py
```

Client sends msg to server
```
python client.py
```

## Reference
1. [websocket tutorial](https://www.youtube.com/watch?v=3QiPPX-KeSc)
2. [How-to-send-audio-from-PyAudio-over-socket](https://pyshine.com/How-to-send-audio-from-PyAudio-over-socket/)

## TODO
1. [DONE] get ASR inference class working
- get audio chunk working for ASR inference
2. add asr in server
3. load audio in server and have server running
4. client and server handle audio data
5. cient sends audio to server. print transcript in server
6. server sends chunk audio back... like a streaming fashion...