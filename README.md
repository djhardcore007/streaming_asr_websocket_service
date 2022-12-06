# Python ASR Socket Server

A simple streaming ASR service using socket.

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
