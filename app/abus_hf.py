import os
import json
from pathlib import Path
from typing import List

from app.abus_path import *
from app.abus_hf_file import *

import structlog

logger = structlog.get_logger()


def load_hf_files(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    hf_files = []
    for item in data:
        hf_file = HF_File(
            file_type=item["file_type"],
            repo_id=item["repo_id"],
            subfolder=item["subfolder"],
            file_name=item["file_name"],
            file_size=item["file_size"],
            level=item["level"],
            display_name=item["display_name"],
        )
        hf_files.append(hf_file)

    return hf_files


class AbusHuggingFace:
    HF_FILES = []

    @classmethod
    def initialize(cls, app_name: str = "voice"):
        """
        클래스를 초기화하는 클래스 메서드
        """
        json_file_name = f"abus_hf_files-{app_name}.json"
        cls.hf_files_path = os.path.join(
            Path(__file__).resolve().parent, json_file_name
        )
        cls.app_name = app_name
        cls.HF_FILES = cls._load_files()
        return cls

    @classmethod
    def _load_files(cls) -> List[HF_File]:
        return load_hf_files(cls.hf_files_path)

    @classmethod
    def reload_files(cls) -> None:
        cls.HF_FILES = cls._load_files()

    @classmethod
    def hf_all_display_names(cls):
        """Return a list of hf model names."""
        return [hf_file.display_name for hf_file in cls.HF_FILES]

    @classmethod
    def hf_download_all_models(cls):
        os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "True"
        for hf_file in cls.HF_FILES:
            if hf_file.has_local_file():
                continue
            hf_file.download()

    @classmethod
    def hf_download_models(cls, file_type: str, level: int):
        logger.debug(
            f"[abus_hf.py] hf_download_models - file_type = {file_type}, level = {level}"
        )

        os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "True"
        for hf_file in cls.HF_FILES:
            if hf_file.level > level:
                continue
            if hf_file.file_type != file_type:
                continue
            if hf_file.has_local_file():
                continue

            hf_file.download()

    @classmethod
    def hf_get_from_name(cls, display_name: str) -> HF_File:
        hf_file = next(
            (model for model in cls.HF_FILES if model.display_name == display_name),
            None,
        )
        return hf_file

    @classmethod
    def hf_display_names(cls, file_types, max_level):
        results = []

        for hf_file in cls.HF_FILES:
            if hf_file.file_type in file_types:
                if hf_file.level <= max_level:
                    results.append(hf_file)
        return results

    @classmethod
    def hf_demixing_names(cls, has_local_file: bool):
        results = []
        for hf_file in cls.HF_FILES:
            # logger.debug(f'[abus_hf.py] hf_demixing_names - hf_file = {hf_file}')
            if hf_file.file_type == "mdxnet-model" or hf_file.file_type == "demucs":
                if has_local_file == hf_file.has_local_file():
                    results.append(hf_file.display_name)
        return results
