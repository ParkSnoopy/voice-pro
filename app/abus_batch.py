from app.abus_path import *
from app.abus_files import *


import structlog

logger = structlog.get_logger()


class BatchManager:
    def __init__(self) -> None:
        self.file_managers = {}
        pass

    def get_fm(self, key, default=None):
        fm = self.file_managers.get(key, default)
        return fm

    def set_fm(self, key, fm):
        self.file_managers[key] = fm

    def get_all_fm(self) -> list:
        return self.file_managers.values()

    def get_all_files(self) -> list:
        files = []
        for fm in self.file_managers.values():
            files.extend(fm.get_all_files())

        return files
