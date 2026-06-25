import os
import torch

from app.abus_ffmpeg import *
from app.abus_path import *
from app.abus_downloader import *
from src.aicover.mdx import *

import structlog

logger = structlog.get_logger()


def run_mdx(
    model_params,
    output_dir,
    model_path,
    filename,
    exclude_main=False,
    exclude_inversion=False,
    suffix=None,
    invert_suffix=None,
    denoise=False,
    keep_orig=True,
    m_threads=2,
):
    device = torch.device("cpu")
    total_vram_gb = 0
    free_vram_gb = 0
    m_threads = 1
    logger.debug(f"run_mdx: device = {device}")
    logger.debug(
        f"run_mdx: total_vram_gb = {total_vram_gb}, free_vram_gb = {free_vram_gb} m_threads = {m_threads}"
    )

    model_hash = MDX.get_hash(model_path)
    mp = model_params.get(model_hash)
    model = MDXModel(
        device,
        dim_f=mp["mdx_dim_f_set"],
        dim_t=2 ** mp["mdx_dim_t_set"],
        n_fft=mp["mdx_n_fft_scale_set"],
        stem_name=mp["primary_stem"],
        compensation=mp["compensate"],
    )

    mdx_sess = MDX(model_path, model)
    wave, sr = librosa.load(filename, mono=False, sr=DEFAULT_SR)
    # normalizing input wave gives better output
    peak = max(np.max(wave), abs(np.min(wave)))
    wave /= peak
    if denoise:
        wave_processed = -(mdx_sess.process_wave(-wave, m_threads)) + (
            mdx_sess.process_wave(wave, m_threads)
        )
        wave_processed *= 0.5
    else:
        wave_processed = mdx_sess.process_wave(wave, m_threads)
    # return to previous peak
    wave_processed *= peak
    stem_name = model.stem_name if suffix is None else suffix

    main_filepath = None
    if not exclude_main:
        main_filepath = os.path.join(
            output_dir,
            f"{os.path.basename(os.path.splitext(filename)[0])}_{stem_name}.wav",
        )
        sf.write(main_filepath, wave_processed.T, sr)

    invert_filepath = None
    if not exclude_inversion:
        diff_stem_name = (
            stem_naming.get(stem_name) if invert_suffix is None else invert_suffix
        )
        stem_name = f"{stem_name}_diff" if diff_stem_name is None else diff_stem_name
        invert_filepath = os.path.join(
            output_dir,
            f"{os.path.basename(os.path.splitext(filename)[0])}_{stem_name}.wav",
        )
        sf.write(invert_filepath, (-wave_processed.T * model.compensation) + wave.T, sr)

    if not keep_orig:
        os.remove(filename)

    del mdx_sess, wave_processed, wave
    gc.collect()
    return main_filepath, invert_filepath
