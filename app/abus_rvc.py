import os

from rvc.lib.tools.prerequisites_download import prequisites_download_pipeline
from rvc.infer.infer import VoiceConverter
from app.abus_path import path_subfolders, path_subfile, path_live_folder
from app.abus_ffmpeg import *
from app.abus_path import *

import structlog

logger = structlog.get_logger()

infer_pipeline = VoiceConverter().infer_pipeline


class RVC:
    def __init__(self):
        self._prepare_model_folder()
        self._run_prerequisites_script("False", "True", "True", "False")

    def _run_prerequisites_script(self, pretraineds_v1, pretraineds_v2, models, exe):
        prequisites_download_pipeline(pretraineds_v1, pretraineds_v2, models, exe)
        return "Prerequisites installed successfully."

    def _prepare_model_folder(self):
        script_dir = os.getcwd()
        rvc_model_folder = os.path.join(script_dir, "rvc", "models")
        logger.debug(
            f"[abus_rvc.py] _prepare_model_folder - rvc_model_folder: {rvc_model_folder}"
        )

        if not os.path.exists(rvc_model_folder):
            os.makedirs(rvc_model_folder, exist_ok=True)

        embedders_folder = os.path.join(rvc_model_folder, "embedders")
        predictors_folder = os.path.join(rvc_model_folder, "predictors")
        pretrained_v1_folder = os.path.join(
            rvc_model_folder, "pretraineds", "pretrained_v1"
        )
        pretrained_v2_folder = os.path.join(
            rvc_model_folder, "pretraineds", "pretrained_v2"
        )

        os.makedirs(embedders_folder, exist_ok=True)
        os.makedirs(predictors_folder, exist_ok=True)
        os.makedirs(pretrained_v1_folder, exist_ok=True)
        os.makedirs(pretrained_v2_folder, exist_ok=True)

        return rvc_model_folder

    def get_voices(self):
        rvc_voice_folder = os.path.join(os.getcwd(), "model", "rvc-voice")
        voice_models = path_subfolders(rvc_voice_folder)
        logger.debug(f"[abus_rvc.py] get_voices - {voice_models}")

        if len(voice_models) == 0:
            voice_models = ["No voice"]
        return voice_models

    def get_voice(self, rvc_voice):
        voice_folder = os.path.join(os.getcwd(), "model", "rvc-voice", rvc_voice)
        voice_pth_path = path_subfile(voice_folder, ".pth")
        voice_index_path = path_subfile(voice_folder, ".index")
        return voice_pth_path, voice_index_path

    def simple_inference(self, input_path, output_path, rvc_voice, export_format="wav"):
        output_voice_file = os.path.join(
            path_live_folder(), path_new_filename(ext=f".{export_format}")
        )
        pth_path, index_path = self.get_voice(rvc_voice)

        f0_up_key = 0  # -24 to +24, Set the pitch of the audio, the higher the value, thehigher the pitch.
        filter_radius = 3  # 0 to 10, If the number is greater than or equal to three, employing median filtering on the collected tone results has the potential to decrease respiration.
        index_rate = 0.3  # 0.0 to 1.0, Influence exerted by the index file; a higher value corresponds to greater influence. However, opting for lower values can help mitigate artifacts present in the audio.
        rms_mix_rate = 1  # 0 to 1, Substitute or blend with the volume envelope of the output. The closer the ratio is to 1, the more the output envelope is employed.
        protect = 0.23  # 0 to 0.5, Safeguard distinct consonants and breathing sounds to prevent electro-acoustic tearing and other artifacts. Pulling the parameter to its maximum value of 0.5 offers comprehensive protection. However, reducing this value might decrease the extent of protection while potentially mitigating the indexing effect.
        hop_length = 256  # 1 to 512, Denotes the duration it takes for the system to transition to a significant pitch change. Smaller hop lengths require more time for inference but tend to yield higher pitch accuracy.
        f0_method = "rmvpe"  # Pitch extraction algorithm to use for the audio conversion. The default algorithm is rmvpe, which is recommended for most cases.

        split_audio = False  # True or False, Split the audio into chunks for inference to obtain better results in some cases.
        f0_autotune = False  # True or False, Apply a soft autotune to your inferences, recommended for singing conversions.
        clean_audio = True  # True or False, Clean your audio output using noise detection algorithms, recommended for speaking audios.
        clean_strength = 0.2  # 0.0 to 1.0, Set the clean-up level to the audio you want, the more you increase it the more it will clean up, but it is possible that the audio will be more compressed.

        embedder_model = "contentvec"  # hubert or contentvec, Embedder model to use for the audio conversion. The default model is hubert, which is recommended for most cases.
        embedder_model_custom = None  # None, Custom Embedder model
        upscale_audio = (
            False  # True or False, Upscale the audio to 48kHz for better results.
        )
        f0_file = None  # None, Path to the f0 file

        logger.debug(
            f"[abus_rvc.py] simple_inference - pth_path = {pth_path}, index_path = {index_path}"
        )

        infer_pipeline(
            str(f0_up_key),
            str(filter_radius),
            str(index_rate),
            str(rms_mix_rate),
            str(protect),
            str(hop_length),
            str(f0_method),
            str(input_path),
            str(output_voice_file),
            str(pth_path),
            str(index_path),
            str(split_audio),
            str(f0_autotune),
            str(clean_audio),
            str(clean_strength),
            str(export_format),
            str(embedder_model),
            embedder_model_custom,
            str(upscale_audio),
            f0_file,
        )

        ffmpeg_to_stereo(output_voice_file, output_path)

        try:
            os.remove(output_voice_file)
        except Exception as e:
            logger.error(f"[abus_rvc.py] simple_inference - error: {e}")

    def call_infer_pipeline(
        self,
        input_path,
        output_path,
        rvc_voice,
        f0_up_key,
        filter_radius,
        index_rate,
        rms_mix_rate,
        protect,
        hop_length,
        clean_strength,
        export_format="wav",
    ):
        output_voice_file = os.path.join(
            path_live_folder(), path_new_filename(ext=f".{export_format}")
        )
        pth_path, index_path = self.get_voice(rvc_voice)

        f0_method = "rmvpe"  # Pitch extraction algorithm to use for the audio conversion. The default algorithm is rmvpe, which is recommended for most cases.

        split_audio = False  # True or False, Split the audio into chunks for inference to obtain better results in some cases.
        f0_autotune = False  # True or False, Apply a soft autotune to your inferences, recommended for singing conversions.
        clean_audio = True  # True or False, Clean your audio output using noise detection algorithms, recommended for speaking audios.

        embedder_model = "contentvec"  # hubert or contentvec, Embedder model to use for the audio conversion. The default model is hubert, which is recommended for most cases.
        embedder_model_custom = None  # None, Custom Embedder model
        upscale_audio = (
            False  # True or False, Upscale the audio to 48kHz for better results.
        )
        f0_file = None  # None, Path to the f0 file

        logger.debug(
            f"[abus_rvc.py] call_infer_pipeline - pth_path = {pth_path}, index_path = {index_path}"
        )

        infer_pipeline(
            str(f0_up_key),
            str(filter_radius),
            str(index_rate),
            str(rms_mix_rate),
            str(protect),
            str(hop_length),
            str(f0_method),
            str(input_path),
            str(output_voice_file),
            str(pth_path),
            str(index_path),
            str(split_audio),
            str(f0_autotune),
            str(clean_audio),
            str(clean_strength),
            str(export_format),
            str(embedder_model),
            embedder_model_custom,
            str(upscale_audio),
            f0_file,
        )

        ffmpeg_to_stereo(output_voice_file, output_path)

        try:
            os.remove(output_voice_file)
        except Exception as e:
            logger.error(f"[abus_rvc.py] call_infer_pipeline - error: {e}")
