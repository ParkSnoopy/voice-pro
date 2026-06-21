# import asyncio
# import edge_tts
import time

# import pysubs2
# import re
from pydub import AudioSegment
# import gradio as gr
# import textwrap

import queue
import threading

import numpy as np

# import pyaudio

import soundfile as sf

from app.abus_path import *
from app.abus_ffmpeg import *
# from app.abus_voice_ms import *

from collections import deque
from src.vad import VoiceActivityDetector
from app.abus_asr_faster_whisper import *

# from src.demucs.api import Separator
# import torchaudio


import structlog

logger = structlog.get_logger()


# 경고를 무시하도록 설정
import warnings

warnings.filterwarnings("ignore")

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class WhisperLive:
    def __init__(self, whisper_inf) -> None:
        self.all_devices = self._all_devices()
        self.device = None

        self.stop_event = threading.Event()
        self.timestamp_offset = 0.0

        self.thread_put_audio = None
        self.thread_get_audio = None

        self.chunk_size = 512  # 512 frames = 32ms, 1024 frames = 64ms
        self.channels = 2
        self.sample_rate = 16000
        self.total_audio = np.empty((0, 2), dtype=np.float32)

        self.audio_queue = None
        self.frames_np = None
        self.segment_queue = queue.Queue()

        self.whisper_params = WhisperParameters()
        self.vad_deque = deque(maxlen=5)
        self.vad_detector = VoiceActivityDetector(frame_rate=self.sample_rate)
        self.whisper_inf = whisper_inf  # FasterWhisperInference()

    def get_whisper_models(self):
        return self.whisper_inf.available_models()

    def get_whisper_languages(self):
        return self.whisper_inf.available_langs()

    def _all_devices(self) -> list:
        devices = []

        try:
            import soundcard as sc

            default_microphone = sc.default_microphone()
            if default_microphone:
                devices.append(default_microphone)
        except Exception as e:
            logger.error(f"[abus_live.py] _all_devices - Error transcribing file: {e}")

        try:
            import soundcard as sc

            default_speaker = sc.default_speaker()
            mics = sc.all_microphones(include_loopback=True)
            for mic in mics:
                if default_speaker.name == mic.name:
                    devices.append(mic)
        except Exception as e:
            logger.error(f"[abus_live.py] _all_devices - Error transcribing file: {e}")

        return devices

    def all_devices_name(self) -> list:
        device_names = []
        for device in self.all_devices:
            device_names.append(device.name)
        return device_names

    def _select_device(self, device_name):
        for device in self.all_devices:
            if device.name == device_name:
                self.device = device
                break

    def stop_thread(self):
        self.stop_event.set()

        if self.thread_put_audio:
            self.thread_put_audio.join()
            self.thread_put_audio = None
        if self.thread_get_audio:
            self.thread_get_audio.join()
            self.thread_get_audio = None

        self.whisper_inf.model = None

        if self.audio_queue:
            self.audio_queue = None
        self.frames_np = None

    def start_thread(self, device_name, params):
        self._select_device(device_name)

        self.audio_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.timestamp_offset = 0.0
        self.frames_np = None

        self.whisper_params = params
        self.whisper_inf.model = None

        self.thread_put_audio = threading.Thread(target=self._thread_put_audio)
        self.thread_put_audio.daemon = True
        self.thread_put_audio.start()

        self.thread_get_audio = threading.Thread(target=self._thread_get_audio)
        self.thread_get_audio.daemon = True
        self.thread_get_audio.start()

    def _thread_put_audio(self):
        logger.debug("[ABUS_LIVE] _thread_put_audio")
        with self.device.recorder(
            samplerate=self.sample_rate, channels=self.channels
        ) as mic:
            while True:
                audio = mic.record(self.chunk_size)
                self.audio_queue.put(audio)
                self.total_audio = np.concatenate((self.total_audio, audio), axis=0)

                if self.stop_event.is_set() == True:
                    self.audio_queue.put(None)
                    logger.debug("[ABUS_LIVE] _thread_put_audio exit....")
                    time.sleep(0.1)
                    break

    def _thread_get_audio(self):
        while not self.stop_event.is_set():
            audio = self.audio_queue.get()
            if audio is None:  # 종료 신호
                self.frames_np = None
                logger.debug("[ABUS_LIVE] _thread_get_audio exit....")
                time.sleep(0.1)
                break

            mono = np.mean(audio, axis=1).astype(np.float32)
            # mono = np.squeeze(audio).astype(np.float32)
            self.frames_np = (
                mono
                if self.frames_np is None
                else np.concatenate((self.frames_np, mono), axis=0)
            )

            audio_length = self.audio_length(self.frames_np, self.sample_rate)
            vad = self.voice_activity(mono)

            if audio_length >= 5.5:
                logger.debug("[ABUS_LIVE] _thread_get_audio 5.5")
                self.run_asr(self.frames_np, self.whisper_params, self.timestamp_offset)
                self.frames_np = None
                time.sleep(0.1)
            elif audio_length > 2.0:
                if vad == False:
                    logger.debug("[ABUS_LIVE] _thread_get_audio 1.0 EOS")
                    self.run_asr(
                        self.frames_np, self.whisper_params, self.timestamp_offset
                    )
                    self.frames_np = None
                    time.sleep(0.1)

            self.timestamp_offset += self.chunk_size / self.sample_rate
            self.audio_queue.task_done()

    def run_asr(self, frames_np, params, timestamp_offset):
        segments, info = self.whisper_inf.transcribe_live(
            frames_np.copy(), params.copy()
        )

        for segment in segments or []:
            segment["start"] += timestamp_offset
            self.segment_queue.put(segment)

        logger.debug(f"[ABUS_LIVE] _thread_asr_frames : {segments}")
        # self.put_segments(segments)

    def voice_activity(self, mono_audio):
        speech_prob = self.vad_detector(mono_audio)
        self.vad_deque.append(speech_prob)
        average = sum(self.vad_deque) / len(self.vad_deque)
        if average < 0.55:
            # logger.debug(f'[SERVER] No Voice : avg = {average}')
            return False
        else:
            return True

    # def put_segments(self, segments):
    #     for segment in segments or []:
    #         self.segment_queue.put(segment)

    def get_segments(self):
        segments = []
        while True:
            try:
                item = self.segment_queue.get_nowait()
                segments.append(item)
                self.segment_queue.task_done()
            except queue.Empty:
                break
        return segments

    def audio_length(self, audio, sr):
        total_samples = len(audio)
        audio_length_seconds = total_samples / sr
        return audio_length_seconds

    def save_audio(self, audio_format: str = "mp3"):
        # output_file_wav = os.path.join(path_live_folder(), f'live-{int(time.time())}.wav')
        # sf.write(file=output_file_wav, data=self.total_audio, samplerate=self.sample_rate)

        denoise_audio = self._denoise(self.total_audio)
        output_file_wav = os.path.join(
            path_live_folder(), f"live-{int(time.time())}.wav"
        )
        sf.write(file=output_file_wav, data=denoise_audio, samplerate=self.sample_rate)

        if audio_format.lower() != "wav":
            output_file = os.path.join(
                path_live_folder(), f"live-{int(time.time())}.{audio_format}"
            )
            wav_audio = AudioSegment.from_wav(output_file_wav)
            wav_audio.export(output_file, format=audio_format)
            os.remove(output_file_wav)

    def clear_audio(self):
        self.total_audio = np.empty((0, 2), dtype=np.float32)

    def _denoise(self, input: np.ndarray, denoise_level: int = 0) -> np.ndarray:
        return input
        # separator = Separator(repo=Path('model/demucs'))

        # waveform = torch.tensor(input, dtype=torch.float32)
        # corrected_input = waveform.transpose(0, 1)
        # origin, separated = separator.separate_tensor(corrected_input, self.sample_rate)
        # for stem, source in separated.items():
        #     if stem == 'vocals':
        #         est_np = source.numpy()
        #         est_np = est_np.reshape(-1, self.channels)
        #         return est_np

        # return input
