import os
import zipfile
import shutil

from pathlib import Path
from huggingface_hub import hf_hub_download

from app.abus_path import *

import structlog

logger = structlog.get_logger()


class HF_File:
    def __init__(
        self,
        file_type,
        repo_id,
        subfolder,
        file_name,
        file_size,
        level,
        display_name: str = "",
    ):
        self.file_type = file_type
        self.repo_id = repo_id
        self.subfolder = subfolder
        self.file_name = file_name
        self.file_size = file_size
        self.level = level
        self.display_name = (
            display_name if display_name != "" else os.path.splitext(file_name)[0]
        )

    def __str__(self):
        return f"HFModel(repo_id={self.repo_id}, subfolder={self.subfolder}, file_name={self.file_name}, file_size={self.file_size}, file_type={self.file_type}, level={self.level})"

    def download_info(self):
        mega_bytes = self.file_size / 1024**2
        return f"{self.file_name} : {mega_bytes: .2f} MB"

    def has_local_file(self):
        file_path = os.path.join(
            path_model_folder(), self.file_type, self.subfolder, self.file_name
        )
        if os.path.exists(file_path):
            if os.path.getsize(file_path) == self.file_size:
                # logger.debug(f'[abus_hf_file.py] has_local_file - True : {file_path}')
                return True
        logger.debug(f"[abus_hf_file.py] has_local_file - False : {file_path}")
        return False

    def download(self, force_download: bool = False):
        try:
            cache_dir = os.path.join(Path.home(), ".cache", "huggingface", "hub")
            hf_download_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=self.file_name,
                subfolder=self.subfolder,
                cache_dir=cache_dir,
                force_download=force_download,
            )
            logger.debug(
                f"[abus_hf_file.py] download - hf_download_path : {hf_download_path}"
            )

            download_folder = os.path.join(
                path_model_folder(), self.file_type, self.subfolder
            )
            if not os.path.exists(download_folder):
                os.makedirs(download_folder, exist_ok=True)

            download_file_path = os.path.join(download_folder, self.file_name)
            if self.has_local_file() == False:
                shutil.copy(hf_download_path, download_file_path)
                logger.debug(
                    f"[abus_hf_file.py] download - download complete : {download_file_path}"
                )

                _, extension = os.path.splitext(download_file_path)
                if extension.lower() == ".zip":
                    self.unzip(make_folder=(self.file_type == "rvc-voice"))
            else:
                logger.debug(
                    f"[abus_hf_file.py] download - skip : {download_file_path}"
                )

            return True, download_file_path
        except Exception as e:
            logger.error(f"[abus_hf_file.py] download - error : {e}")
            return False, None

    def unzip(self, make_folder: bool = False):
        zip_path = os.path.join(
            path_model_folder(), self.file_type, self.subfolder, self.file_name
        )
        extract_to = os.path.dirname(zip_path)
        logger.debug(f"[abus_hf_file.py] unzip: {zip_path}")
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_contents = zip_ref.namelist()
                logger.debug(f"[abus_hf_file.py] unzip - zip_contents: {zip_contents}")

                if not os.path.exists(extract_to):
                    os.makedirs(extract_to)

                if "/" in zip_contents[0]:
                    zip_ref.extractall(extract_to)
                else:
                    if make_folder:
                        folder_name = os.path.splitext(os.path.basename(zip_path))[0]
                        extract_to = os.path.join(extract_to, folder_name)
                        if not os.path.exists(extract_to):
                            os.makedirs(extract_to)
                    zip_ref.extractall(extract_to)
            return True
        except:
            return False

    def download_private(self, token, force_download: bool = False):
        try:
            # logger.warning(f'[abus_hf_file.py] download_private - start download : {self.file_name}')
            cache_dir = os.path.join(Path.home(), ".cache", "huggingface", "hub")
            hf_download_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=self.file_name,
                subfolder=self.subfolder,
                cache_dir=cache_dir,
                token=token,
                force_download=force_download,
            )

            download_folder = os.path.join(
                path_model_folder(), self.file_type, self.subfolder
            )
            if not os.path.exists(download_folder):
                os.makedirs(download_folder, exist_ok=True)

            download_file_path = os.path.join(download_folder, self.file_name)
            shutil.copy(hf_download_path, download_file_path)
            # logger.warning(f'[abus_hf_file.py] download_private - download complete : {download_file_path}')

            _, extension = os.path.splitext(download_file_path)
            if extension.lower() == ".zip":
                self.unzip(make_folder=(self.file_type == "rvc-voice"))
            return True, download_file_path
        except:
            return False, None
