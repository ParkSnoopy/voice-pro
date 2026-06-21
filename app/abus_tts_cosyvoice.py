import os
import pysubs2

from pydub import AudioSegment
import gradio as gr
import torch
import gc

from app.abus_genuine import *
from app.abus_path import *
from app.abus_ffmpeg import *
from app.abus_hf_file import *
from app.abus_text import *
from app.abus_nlp_spacy import *
from app.abus_audio import *

import structlog

logger = structlog.get_logger()


# import soundfile as sf
# from f5_tts.model import DiT, UNetT
from f5_tts.infer.utils_infer import preprocess_ref_audio_text


import librosa
import random

max_val = 0.8
prompt_sr = 16000

import torchaudio
from cosyvoice.cli.cosyvoice import CosyVoice2
from cosyvoice.utils.file_utils import load_wav
from cosyvoice.utils.common import set_all_random_seed

# logging.getLogger().setLevel(logging.WARNING)
# logging.getLogger('matplotlib').setLevel(logging.WARNING)
# logging.basicConfig(level=logging.WARNING,
#                     format='%(asctime)s %(levelname)s %(message)s')



os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "True"


class CosyVoiceInference:
    def __init__(self):
        self.model_dir = os.path.join(
            path_model_folder(), "cosyvoice", "CosyVoice2-0.5B"
        )

        # snapshot_download('iic/CosyVoice2-0.5B', local_dir=self.model_dir)
        # self._download_model()
        self._cosyvoice = None

    def __getattr__(self, name):
        if name == "cosyvoice":
            if self._cosyvoice is None:
                print("Creating CosyVoice2...")
                self._cosyvoice = CosyVoice2(self.model_dir)
            return self._cosyvoice
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

    def _download_model(self):
        CosyVoice2_05B = HF_File(
            "cosyvoice", "ABUS-AI/CosyVoice", "", "CosyVoice2-0.5B.zip", 9003318755, 0
        )
        self.has_model, _ = CosyVoice2_05B.download(force_download=False)

    @staticmethod
    def release_cuda_memory():
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.reset_max_memory_allocated()
            logger.debug("[abus_tts_cosyvoice.py] release_cuda_memory - OK!! ")

    def set_random_seed(self):
        seed = random.randint(1, 100000000)
        set_all_random_seed(seed)

    def generate_audio_zero_shot(
        self, dubbing_text: str, output_file, ref_audio, ref_text, speed_factor
    ):
        logger.debug(
            f"[abus_tts_cosyvoice.py] generate_audio_zero_shot - ref_audio = {ref_audio}, ref_text = {ref_text}, dubbing_text = {dubbing_text}"
        )

        # zero_shot usage
        prompt_speech_16k = self.postprocess(load_wav(ref_audio, prompt_sr))
        for i, j in enumerate(
            self.cosyvoice.inference_zero_shot(
                dubbing_text,
                ref_text,
                prompt_speech_16k,
                stream=False,
                speed=speed_factor,
                text_frontend=False,
            )
        ):
            torchaudio.save(output_file, j["tts_speech"], self.cosyvoice.sample_rate)

    def generate_audio_cross_lingual(
        self, dubbing_text: str, output_file, ref_audio, ref_text, speed_factor
    ):
        logger.debug(
            f"[abus_tts_cosyvoice.py] generate_audio_cross_lingual - ref_audio = {ref_audio}, ref_text = {ref_text}, dubbing_text = {dubbing_text}"
        )

        # fine grained control, for supported control, check cosyvoice/tokenizer/tokenizer.py#L248
        prompt_speech_16k = self.postprocess(load_wav(ref_audio, prompt_sr))
        for i, j in enumerate(
            self.cosyvoice.inference_cross_lingual(
                dubbing_text, prompt_speech_16k, speed=speed_factor, stream=False
            )
        ):
            torchaudio.save(output_file, j["tts_speech"], self.cosyvoice.sample_rate)

    def generate_audio_instruct(
        self, dubbing_text: str, output_file, ref_audio, ref_text, speed_factor
    ):
        logger.debug(
            f"[abus_tts_cosyvoice.py] generate_audio_instruct - ref_audio = {ref_audio}, ref_text = {ref_text}, dubbing_text = {dubbing_text}"
        )

        # instruct usage
        prompt_speech_16k = self.postprocess(load_wav(ref_audio, prompt_sr))
        for i, j in enumerate(
            self.cosyvoice.inference_instruct2(
                dubbing_text, "", prompt_speech_16k, stream=False
            )
        ):
            torchaudio.save(output_file, j["tts_speech"], self.cosyvoice.sample_rate)

    def postprocess(self, speech, top_db=60, hop_length=220, win_length=440):
        speech, _ = librosa.effects.trim(
            speech, top_db=top_db, frame_length=win_length, hop_length=hop_length
        )
        if speech.abs().max() > max_val:
            speech = speech / speech.abs().max() * max_val
        speech = torch.concat(
            [speech, torch.zeros(1, int(self.cosyvoice.sample_rate * 0.2))], dim=1
        )
        return speech

    def request_tts(
        self,
        line: str,
        output_file: str,
        ref_audio,
        ref_text,
        inference_mode,
        speed_factor,
        audio_format,
    ):
        output_voice_file = os.path.join(
            path_dubbing_folder(), path_new_filename(ext=f".{audio_format}")
        )
        line = AbusText.normalize_text(line)
        if len(line) < 1:
            logger.warning("[abus_tts_cosyvoice.py] request_tts - error: no line")
            return False

        logger.debug(f"[abus_tts_cosyvoice.py] request_tts - line = {line}")

        if inference_mode == "Cross-Lingual":
            self.generate_audio_cross_lingual(
                line, output_voice_file, ref_audio, ref_text, speed_factor
            )
        elif inference_mode == "Instruct":
            self.generate_audio_instruct(
                line, output_voice_file, ref_audio, ref_text, speed_factor
            )
        else:
            self.generate_audio_zero_shot(
                line, output_voice_file, ref_audio, ref_text, speed_factor
            )

        trimed_voice_file = path_add_postfix(output_voice_file, "_trimed")
        AbusAudio.trim_silence_file(output_voice_file, trimed_voice_file)
        ffmpeg_to_stereo(trimed_voice_file, output_file)

        try:
            os.remove(output_voice_file)
            os.remove(trimed_voice_file)
        except Exception as e:
            logger.error(f"[abus_tts_cosyvoice.py] request_tts - error: {e}")
            return False
        return True

    def srt_to_voice(
        self,
        subtitle_file: str,
        output_file: str,
        ref_audio,
        ref_text,
        inference_mode,
        speed_factor,
        audio_format,
        progress=gr.Progress(),
    ):
        tts_subtitle_file = path_add_postfix(subtitle_file, "-cosyvoice", ".srt")

        # AbusText.process_subtitle_for_tts(subtitle_file, tts_subtitle_file)
        AbusSpacy.process_subtitle_for_tts(subtitle_file, tts_subtitle_file)

        segments_folder = path_tts_segments_folder(subtitle_file)
        full_subs = pysubs2.load(tts_subtitle_file, encoding="utf-8")
        subs = full_subs

        combined_audio = AudioSegment.empty()
        for i in progress.tqdm(range(len(subs)), desc="Generating..."):
            line = subs[i]
            next_line = subs[i + 1] if i < len(subs) - 1 else None

            if i == 0:
                silence = AudioSegment.silent(duration=line.start)
                combined_audio += silence

            tts_segment_file = os.path.join(
                segments_folder, f"tts_{i + 1}.{audio_format}"
            )
            tts_result = self.request_tts(
                line.text,
                tts_segment_file,
                ref_audio,
                ref_text,
                inference_mode,
                speed_factor,
                audio_format,
            )

            if tts_result == False:
                if next_line:
                    silence = AudioSegment.silent(duration=next_line.start - line.start)
                    combined_audio += silence
                continue

            combined_audio += AudioSegment.from_file(tts_segment_file)

            if next_line and len(combined_audio) < next_line.start:
                silence_length = next_line.start - len(combined_audio)
                silence = AudioSegment.silent(duration=silence_length)
                combined_audio += silence
            elif next_line:
                next_line.start = len(combined_audio)
                next_line.end = next_line.start + (next_line.end - next_line.start)

        combined_audio.export(output_file, format=audio_format)
        cmd_delete_file(tts_subtitle_file)

    def text_to_voice(
        self,
        dubbing_text: str,
        output_file: str,
        ref_audio,
        ref_text,
        inference_mode,
        speed_factor,
        audio_format,
        progress=gr.Progress(),
    ):
        segments_folder = path_tts_segments_folder(output_file)

        use_punctuation = AbusText.has_punctuation_marks(dubbing_text)
        lines = AbusText.split_into_sentences(dubbing_text, use_punctuation)
        lines = lines

        combined_audio = AudioSegment.empty()
        for i in progress.tqdm(range(len(lines)), desc="Generating..."):
            tts_segment_file = os.path.join(
                segments_folder, f"tts_{i + 1:06}.{audio_format}"
            )
            tts_result = self.request_tts(
                lines[i],
                tts_segment_file,
                ref_audio,
                ref_text,
                inference_mode,
                speed_factor,
                audio_format,
            )
            if tts_result == False:
                continue
            combined_audio += AudioSegment.from_file(tts_segment_file)

        combined_audio.export(output_file, format=audio_format)

    def infer_single(
        self,
        dubbing_text: str,
        output_file,
        celeb_audio,
        celeb_transcript,
        inference_mode,
        speed_factor,
        audio_format: str,
        progress=gr.Progress(),
    ):
        self.set_random_seed()

        ref_audio, ref_text = preprocess_ref_audio_text(celeb_audio, celeb_transcript)

        subtitle_file = None
        if AbusText.is_subtitle_format(dubbing_text):
            subs = pysubs2.SSAFile.from_string(dubbing_text)
            subtitle_file = os.path.join(
                path_dubbing_folder(), path_new_filename(f".{subs.format}")
            )
            subs.save(subtitle_file)

        if subtitle_file:
            self.srt_to_voice(
                subtitle_file,
                output_file,
                ref_audio,
                ref_text,
                inference_mode,
                speed_factor,
                audio_format,
                progress,
            )
        else:
            self.text_to_voice(
                dubbing_text,
                output_file,
                ref_audio,
                ref_text,
                inference_mode,
                speed_factor,
                audio_format,
                progress,
            )

        # del self.ema_model
        # self.ema_model = None
        self.release_cuda_memory()
