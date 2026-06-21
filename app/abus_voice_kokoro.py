import os
import json5

from app.abus_path import *
from app.abus_hf_file import *

import structlog

logger = structlog.get_logger()


os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "True"


class KokoroVoice:
    def __init__(
        self, language, lang_code, voice_code, audio_file, display_name, transcript
    ):
        self.language = language
        self.lang_code = lang_code
        self.voice_code = voice_code
        self.audio_file = audio_file
        self.display_name = display_name
        self.transcript = transcript

    def __repr__(self):  # For easy printing
        return f"KokoroVoice(display_name='{self.display_name}', lang_code='{self.lang_code}', voice_code='{self.voice_code}', audio_file='{self.audio_file}')"

    def audio_path(self):
        file_path = os.path.join(
            path_model_folder(),
            "kokoro",
            "kokoro-tts-samples",
            "mp3",
            self.language,
            self.audio_file,
        )
        return file_path

    def has_audio(self):
        file_path = self.audio_path()
        if os.path.exists(file_path):
            # logger.debug(f'[abus_voice_kokoro.py] has_audio - OK : {file_path}')
            return True
        logger.debug(f"[abus_voice_kokoro.py] has_audio - False : {file_path}")
        return False


class KokoroVoiceManager:
    def __init__(self):
        self.samples = {}

        # self._download_hf()

        if True:  # self.download_success:
            kokoro_tts_samples_json = os.path.join(
                path_model_folder(),
                "kokoro",
                "kokoro-tts-samples",
                "kokoro-tts-samples.json5",
            )
            self._load_from_json(kokoro_tts_samples_json)

    def _download_hf(self):
        kokoro_tts_samples = HF_File(
            "kokoro", "ABUS-AI/CosyVoice", "", "kokoro-tts-samples.zip", 5112515, 0
        )
        self.download_success, _ = kokoro_tts_samples.download(force_download=False)

    def _load_from_json(self, kokoro_tts_samples_json):
        self.samples = {}

        try:
            with open(kokoro_tts_samples_json, "r", encoding="utf-8") as file:
                data = json5.load(file)
                for language, files_data in data.items():
                    self.samples[language] = []
                    for file_info in files_data["files"]:
                        kv = KokoroVoice(
                            language,
                            file_info["lang_code"],
                            file_info["voice_code"],
                            file_info["audio_file"],
                            file_info["display_name"],
                            file_info["transcript"],
                        )
                        self.samples[language].append(kv)

        except Exception as e:
            logger.error(f"[abus_voice_kokoro.py] _load_from_json - Error: {e}")

    def voice_list(self, language="American English"):
        return self.samples[language]

    def find_voice(self, language, display_name):
        voice_list = self.samples[language]
        for kv in voice_list:
            if kv.display_name == display_name:
                return kv
        return None

    def languages(self):
        languages = self.samples.keys()
        # emoji_languages = ["chinese", "english", "korean", "japanese"]
        return languages
