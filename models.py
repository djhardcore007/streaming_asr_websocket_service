import os
import wave
import base64
import time
import librosa

import torch
import numpy as np
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC


def frames_to_tensor(frames, ori_sr, tgt_sr):
    if not frames:
        return
    audio_int16 = np.frombuffer(frames, np.int16)
    audio_float32 = audio_int16.astype("float32")
    # Normalize
    abs_max = np.abs(audio_int16).max()
    if abs_max > 0:
        audio_float32 *= 1 / abs_max
    wav = audio_float32.squeeze()  # depends on the use case
    # resampling
    if ori_sr != tgt_sr:
        wav = librosa.resample(wav, orig_sr=ori_sr, target_sr=tgt_sr)
    tensor = torch.from_numpy(wav)
    return tensor


class ASRInference:
    def __init__(self, device, huggingface_folder, model_path, target_sampling_rate) -> None:
        self.device = device
        self.processor = Wav2Vec2Processor.from_pretrained(huggingface_folder)
        self.model = Wav2Vec2ForCTC.from_pretrained(huggingface_folder).to(self.device)
        if model_path is not None:
            self.preload_model(model_path)
        self.target_sampling_rate = target_sampling_rate

    def preload_model(self, model_path) -> None:
        """
        Preload model parameters (in "*.tar" format) at the start of experiment.
        Args:
            model_path: The file path of the *.tar file
        """
        assert os.path.exists(model_path), f"The file {model_path} is not exist. please check path."
        checkpoint = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(checkpoint["model"], strict = True)
        print(f"Model preloaded successfully from {model_path}.")

    def transcribe(self, wav) -> str:
        input_values = self.processor(wav, sampling_rate=self.target_sampling_rate, return_tensors="pt").input_values
        logits = self.model(input_values.to(self.device)).logits
        pred_ids = torch.argmax(logits, dim=-1)
        pred_transcript = self.processor.batch_decode(pred_ids)[0]
        return pred_transcript


if __name__ == '__main__':
    WAV_PATH = 'data/87984097648596_202204032122368798409764859620debacde9b225730fb5e8d9e1cc8071b.amr'

    DEVICE = device = f"cuda:0" if torch.cuda.is_available() else "cpu"
    HUGGINGFACE_FOLDER = 'models/huggingface-hub-ciempiess16k'
    MODEL_PATH = 'models/best_model.tar'
    TARGET_SAMPLING_RATE = 16000
    CHUNK_DURATION = 3

    asr = ASRInference(device=DEVICE, huggingface_folder=HUGGINGFACE_FOLDER, model_path=MODEL_PATH, target_sampling_rate=TARGET_SAMPLING_RATE)

    chunk_size = TARGET_SAMPLING_RATE * CHUNK_DURATION
    i = 0
    transcripts = []
    start_time = time.time()
    print(start_time)
    with wave.open(WAV_PATH) as wav_file:
        sample_rate_hertz = wav_file.getframerate()

        while i * chunk_size < wav_file.getnframes():
            # Pass chunk by chunk to recognizer
            chunk = wav_file.readframes(chunk_size)
            if not chunk: # ending...
                break

            # serialize data
            data = base64.b64encode(chunk).decode('utf-8')      # client sends this to server
            # import pdb; pdb.set_trace()
            chunk_received_by_server = base64.b64decode(bytes(data, 'utf-8'))      # server decode string to chunk

            chunk_tensor = frames_to_tensor(chunk, sample_rate_hertz, sample_rate_hertz)
            print(f'{chunk == chunk_received_by_server}')
            partial_transcript = asr.transcribe(chunk_tensor)
            print(partial_transcript)
            transcripts.append(partial_transcript)

    print("".join(transcripts))
    print(time.time()-start_time)
