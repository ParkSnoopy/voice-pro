import gc
import librosa
import soundfile as sf
from pydub import AudioSegment
from pedalboard import Pedalboard, Reverb, Compressor, HighpassFilter
from pedalboard.io import AudioFile

from src.aicover.rvc import Config, load_hubert, get_vc, rvc_infer


from app.abus_path import *


def rvc_change_voice(
    input_path,
    output_path,
    rvc_voice,
    pitch_change,
    f0_method,
    index_rate,
    filter_radius,
    rms_mix_rate,
    protect,
    crepe_hop_length,
):
    voice_model_folder = os.path.join(os.getcwd(), "model", "rvc-voice", rvc_voice)
    voice_pth_path = path_subfile(voice_model_folder, ".pth")
    voice_index_path = path_subfile(voice_model_folder, ".index")

    device = "cpu"
    config = Config(device, False)
    hubert_model = load_hubert(
        device,
        config.is_half,
        os.path.join(os.getcwd(), "model", "rvc-model", "hubert_base.pt"),
    )
    cpt, version, net_g, tgt_sr, vc = get_vc(
        device, config.is_half, config, voice_pth_path
    )

    # convert main vocals
    rvc_infer(
        voice_index_path,
        index_rate,
        input_path,
        output_path,
        pitch_change,
        f0_method,
        cpt,
        version,
        net_g,
        filter_radius,
        tgt_sr,
        rms_mix_rate,
        protect,
        crepe_hop_length,
        vc,
        hubert_model,
    )
    del hubert_model, cpt
    gc.collect()


def rvc_add_effects(
    input_path, output_path, reverb_rm_size, reverb_wet, reverb_dry, reverb_damping
):
    # Initialize audio effects plugins
    board = Pedalboard(
        [
            HighpassFilter(),
            Compressor(ratio=4, threshold_db=-15),
            Reverb(
                room_size=reverb_rm_size,
                dry_level=reverb_dry,
                wet_level=reverb_wet,
                damping=reverb_damping,
            ),
        ]
    )

    with AudioFile(input_path) as f:
        with AudioFile(output_path, "w", f.samplerate, f.num_channels) as o:
            # Read one second of audio at a time, until the file is empty:
            while f.tell() < f.frames:
                chunk = f.read(int(f.samplerate))
                effected = board(chunk, f.samplerate, reset=False)
                o.write(effected)


def rvc_shift_pitch(input_path, output_path, n_steps):
    if not os.path.exists(output_path):
        y, sr = librosa.load(input_path)
        y_changed = librosa.effects.pitch_shift(y, sr, n_steps=n_steps)
        sf.write(output_path, y_changed, sr)


def rvc_combine_audio(
    audio_paths: list,
    output_path: str,
    main_gain: int,
    backup_gain: int,
    inst_gain: int,
    output_format: str,
):
    main_vocal_audio = AudioSegment.from_wav(audio_paths[0]) + main_gain
    backup_vocal_audio = AudioSegment.from_wav(audio_paths[1]) + backup_gain
    instrumental_audio = AudioSegment.from_wav(audio_paths[2]) + inst_gain
    main_vocal_audio.overlay(backup_vocal_audio).overlay(instrumental_audio).export(
        output_path, format=output_format
    )
