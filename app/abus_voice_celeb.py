import os
import json5

from app.abus_path import *
from app.abus_hf_file import *

import structlog

logger = structlog.get_logger()


os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "True"


class Celebrity:
    def __init__(self, language, audio_file, image_file, display_name, transcript):
        self.language = language
        self.audio_file = audio_file
        self.image_file = image_file
        self.display_name = display_name
        self.transcript = transcript

    def __repr__(self):  # For easy printing
        return f"Celebrity(display_name='{self.display_name}', audio_file='{self.audio_file}')"

    def audio_path(self):
        file_path = os.path.join(
            path_model_folder(),
            "cosyvoice",
            "celebrities30s",
            self.language,
            self.audio_file,
        )
        return file_path

    def image_path(self):
        file_path = os.path.join(
            path_model_folder(),
            "cosyvoice",
            "celebrities30s",
            self.language,
            self.image_file,
        )
        return file_path

    def has_audio(self):
        file_path = self.audio_path()
        if os.path.exists(file_path):
            # logger.debug(f'[abus_voice_celeb.py] has_audio - OK : {file_path}')
            return True

        logger.debug(f"[abus_voice_celeb.py] has_audio - False : {file_path}")
        return False

    def has_image(self):
        file_path = self.image_path()
        if os.path.exists(file_path):
            # logger.debug(f'[abus_voice_celeb.py] has_image - OK : {file_path}')
            return True
        logger.debug(f"[abus_voice_celeb.py] has_image - False : {file_path}")
        return False


class CelebVoiceManager:
    def __init__(self):
        self.celebrities = {}
        # self.selected_language = "English"

        # self._download_hf()

        if True:  # self.download_success:
            celebrities30s_json = os.path.join(
                path_model_folder(),
                "cosyvoice",
                "celebrities30s",
                "celebrities30s.json5",
            )
            self._load_from_json(celebrities30s_json)

    def _download_hf(self):
        celebrities30s = HF_File(
            "cosyvoice", "ABUS-AI/CosyVoice", "", "celebrities30s.zip", 18467946, 0
        )
        self.download_success, _ = celebrities30s.download(force_download=False)

    def _load_from_json(self, celebrities30s_json):
        self.celebrities = {}

        try:
            with open(celebrities30s_json, "r", encoding="utf-8") as file:
                data = json5.load(file)
                for language, files_data in data.items():
                    self.celebrities[language] = []
                    for file_info in files_data["files"]:
                        celebrity = Celebrity(
                            language,
                            file_info["audio_file"],
                            file_info["image_file"],
                            file_info["display_name"],
                            file_info["transcript"],
                        )
                        self.celebrities[language].append(celebrity)

        except Exception as e:
            logger.error(f"[abus_voice_celeb.py] _load_from_json - Error: {e}")

    def voice_names(self, language="English"):
        results = []
        celebrities = self.celebrities[language]

        for celebrity in celebrities:
            if celebrity.has_audio() == True:
                results.append(celebrity.display_name)
        return results

    def find_voice(self, display_name):
        for language, celebrity_list in self.celebrities.items():
            for celebrity in celebrity_list:
                if celebrity.display_name == display_name:
                    return celebrity
        return None

    def languages(self):
        languages = self.celebrities.keys()
        # emoji_languages = ["chinese", "english", "korean", "japanese"]
        return languages
