import os

import time
import numpy as np
from typing import BinaryIO, Union, Tuple, List


import whisper_timestamped
import gc
from whisper.utils import get_writer
import gradio as gr


from app.abus_path import *
from app.abus_asr_parameters import *

from src.whisperProgressHook import create_progress_listener_handle


import structlog

logger = structlog.get_logger()


class PrintingProgressListener:
    def __init__(self, progress=None):
        self.progress = progress

    def on_progress(self, current: Union[int, float], total: Union[int, float]):
        # print(f"Progress: {current}/{total}")
        if self.progress is not None:
            self.progress(current / total, desc="Transcribing...")

    def on_finished(self):
        # print("Finished")
        if self.progress is not None:
            self.progress(1.0, desc="Transcribing...")


class WhisperTimestampedInference:
    def __init__(self):
        self.current_model_size = None
        self.model = None
        self.translatable_models = ["large", "large-v1", "large-v2", "large-v3"]
        self.device = "vulkan"
        self.current_compute_type = "float32"

    @staticmethod
    def release_memory():
        gc.collect()
        logger.debug(
            "[abus_asr_whisper_timestamped.py] release_memory - OK!! "
        )

    @staticmethod
    def remove_input_files(file_paths: List[str]):
        if not file_paths:
            return

        for file_path in file_paths:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

    @staticmethod
    def available_models():
        return whisper_timestamped.available_models()

    @staticmethod
    def available_langs():
        return sorted(list(whisper_timestamped.tokenizer.LANGUAGES.values()))

    def transcribe_live(
        self, input_sample: np.ndarray, params: WhisperParameters, progress=None
    ) -> Tuple[List[dict], float]:
        try:
            denoise_sample = self._denoise_live(input_sample, params.denoise_level)
            result, time_for_task = self.transcribe(
                denoise_sample, params.copy(), progress
            )
            return result["segments"], time_for_task

        except Exception as e:
            logger.error(
                f"[abus_asr_whisper_timestamped.py] transcribe_live - An error occurred: {e}"
            )
            return None, None
        finally:
            self.release_memory()

    def transcribe_file(
        self,
        input_path: str,
        params: WhisperParameters,
        highlight_words: bool,
        progress=None,
    ) -> list:
        try:
            with create_progress_listener_handle(
                PrintingProgressListener(progress)
            ) as listener:
                # transcribed_segments, time_for_task = self.transcribe(input_path, params.copy(), progress)
                # subtitles = self.generate_and_write_file(input_path, transcribed_segments, highlight_words)
                result, time_for_task = self.transcribe(
                    input_path, params.copy(), progress
                )
                subtitles = self.write_file(input_path, result, highlight_words)
                return subtitles
        except Exception as e:
            logger.error(
                f"[abus_asr_whisper_timestamped.py] transcribe_file - An error occurred: {e}"
            )
        finally:
            self.model = None
            self.release_memory()

    def transcribe(
        self, audio: Union[str, BinaryIO, np.ndarray], params, progress: gr.Progress
    ) -> Tuple[List[dict], float]:

        start_time = time.time()

        if (
            params.model_size != self.current_model_size
            or self.model is None
            or params.compute_type != self.current_compute_type
        ):
            self.update_model(params.model_size, params.compute_type, progress)

        if params.lang == "Automatic Detection":
            params.lang = None
        else:
            language_code_dict = {
                value: key
                for key, value in whisper_timestamped.tokenizer.LANGUAGES.items()
            }
            params.lang = language_code_dict[params.lang]

        decode_options = {
            "beam_size": 5,
            "best_of": 5,
        }

        result = self.model.transcribe(
            audio=audio,
            verbose=True,
            language=params.lang,
            task="translate"
            if params.is_translate
            and self.current_model_size in self.translatable_models
            else "transcribe",
            # vad_filter=params.vad_filter,
            # beam_size=params.beam_size,
            # log_prob_threshold=params.log_prob_threshold,
            # no_speech_threshold=params.no_speech_threshold,
            # best_of=params.best_of,
            patience=params.patience,
            condition_on_previous_text=params.condition_on_previous_text,
            temperature=params.temperature,
            word_timestamps=params.word_timestamps,
            initial_prompt=params.initial_prompt,
            # hallucination_silence_threshold=params.hallucination_silence_threshold,
            # repetition_penalty=params.repetition_penalty,
            # vad_parameters=params.vad_parameters,
            **decode_options,
        )

        if progress is not None:
            progress(0, desc="Loading audio..")

        # segments_result = []
        # for segment in result["segments"]:
        #     segments_result.append(segment)

        elapsed_time = time.time() - start_time
        # return segments_result, elapsed_time
        return result, elapsed_time

    def update_model(self, model_size: str, compute_type: str, progress: gr.Progress):
        """
        Update current model setting

        Parameters
        ----------
        model_size: str
            Size of whisper model
        compute_type: str
            Compute type for transcription.
            see more info : https://opennmt.net/CTranslate2/quantization.html
        progress: gr.Progress
            Indicator to show progress directly in gradio.
        """
        if progress is not None:
            progress(0, desc="Initializing Model..")

        self.current_model_size = model_size
        self.current_compute_type = compute_type

        self.model = whisper_timestamped.load_model(
            device=self.device, name=model_size, download_root="model"
        )

    def _denoise_live(self, input: np.ndarray, denoise_level: int = 0) -> np.ndarray:
        logger.debug(
            f"[abus_asr_whisper_timestamped.py] _denoise_live:input.shape = {input.shape}"
        )

        return input

    def write_file(self, input_path: str, result, highlight_words):
        subtitles = []
        if len(result) < 1:
            return subtitles

        folder_path = os.path.dirname(input_path)
        writer_args = {
            "highlight_words": highlight_words,
            "max_line_count": None,
            "max_line_width": None,
            "max_words_per_line": None,
        }

        try:
            # vtt
            writer_vtt = get_writer("vtt", folder_path)
            writer_vtt(result, input_path, **writer_args)
            vtt_path = path_change_ext(input_path, ".vtt")
            subtitles.append(vtt_path)

            # tsv
            writer_tsv = get_writer("tsv", folder_path)
            writer_tsv(result, input_path, **writer_args)
            tsv_path = path_change_ext(input_path, ".tsv")
            subtitles.append(tsv_path)

            # txt
            writer_txt = get_writer("txt", folder_path)
            writer_txt(result, input_path, **writer_args)
            txt_path = path_change_ext(input_path, ".txt")
            subtitles.append(txt_path)

            # srt
            writer_srt = get_writer("srt", folder_path)
            writer_srt(result, input_path, **writer_args)
            srt_path = path_change_ext(input_path, ".srt")
            subtitles.append(srt_path)

            # json
            writer_json = get_writer("json", folder_path)
            writer_json(result, input_path, **writer_args)
            json_path = path_change_ext(input_path, ".json")
            subtitles.append(json_path)

        except Exception as e:
            logger.error(
                f"[abus_asr_whisper_timestamped.py] write_file - An error occurred: {e}"
            )

        finally:
            return subtitles

    @staticmethod
    def format_time(elapsed_time: float) -> str:
        """
        Get {hours} {minutes} {seconds} time format string

        Parameters
        ----------
        elapsed_time: str
            Elapsed time for transcription

        Returns
        ----------
        Time format string
        """
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)

        time_str = ""
        if hours:
            time_str += f"{hours} hours "
        if minutes:
            time_str += f"{minutes} minutes "
        seconds = round(seconds)
        time_str += f"{seconds} seconds"

        return time_str.strip()
