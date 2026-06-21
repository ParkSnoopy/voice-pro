import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import gradio as gr
from src.config import UserConfig

from src.i18n.i18n import I18nAuto

i18n = I18nAuto()

from app.gradio_kara import *
from app.abus_hf import AbusHuggingFace


def karaoke_tab(user_config: UserConfig):
    studio = GradioKara(user_config)
    with gr.Row():
        with gr.Column(scale=3):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Upload media')}</h4></center>")
                media_file = gr.File(
                    label=i18n("Upload File"),
                    type="filepath",
                    file_count="single",
                    file_types=["audio", "video"],
                )
                mic_audio = gr.Audio(
                    label=i18n("Microphone Input"),
                    sources=["microphone"],
                    type="filepath",
                )
                with gr.Group():
                    url_text = gr.Textbox(
                        label=i18n("YouTube URL"),
                        placeholder="https://youtu.be/abcdefgh...",
                    )
                    youtube_quality_radio = gr.Radio(
                        label=i18n("YouTube Video Quality"),
                        choices=["low", "good", "best"],
                        value=user_config.get("video_quality", "good"),
                    )
                audio_format_radio = gr.Radio(
                    label=i18n("Audio Format"),
                    choices=["wav", "flac", "mp3"],
                    value=user_config.get("audio_format", "flac"),
                )

            with gr.Row():
                clear_button = gr.ClearButton(value=i18n("Clear"))
                submit_button = gr.Button(value=i18n("Submit"), variant="primary")
        with gr.Column(scale=9):
            with gr.Row():
                with gr.Column():
                    with gr.Group():
                        gr.HTML(f"<center><h4>{i18n('Original')}</h4></center>")
                        input_video = gr.Video(label=i18n("Video"), interactive=False)
                        input_audio = gr.Audio(
                            label=i18n("Audio"), type="filepath", interactive=False
                        )
            with gr.Row():
                with gr.Column():
                    with gr.Group():
                        gr.HTML(f"<center><h4>{i18n('Primary Stem')}</h4></center>")
                        demixing_video1 = gr.Video(
                            label=i18n("Video"), interactive=False
                        )
                        demixing_audio1 = gr.Audio(
                            label=i18n("Audio"), type="filepath", interactive=False
                        )
                with gr.Column():
                    with gr.Group():
                        gr.HTML(f"<center><h4>{i18n('Secondary Stem')}</h4></center>")
                        demixing_video2 = gr.Video(
                            label=i18n("Video"), interactive=False
                        )
                        demixing_audio2 = gr.Audio(
                            label=i18n("Audio"), type="filepath", interactive=False
                        )

            output_files = gr.File(
                label=i18n("Files"), type="filepath", file_count="multiple"
            )

            with gr.Row():
                workspace_button = gr.Button(
                    value=i18n("🗂️ Open workspace folder"), variant="secondary"
                )
                temp_button = gr.Button(
                    value=i18n("🗀 Open Temp folder"), variant="secondary"
                )

        with gr.Column(scale=3):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Demixing')}</h4></center>")
                demixing_model_dropdown = gr.Dropdown(
                    label=i18n("MDX Models"),
                    choices=AbusHuggingFace.hf_demixing_names(True),
                    value=user_config.get("demixing_model", "htdemucs"),
                )
                demixing_format_radio = gr.Radio(
                    label=i18n("Audio Format"),
                    choices=["wav", "flac", "mp3"],
                    value=user_config.get("audio_format", "flac"),
                )
            with gr.Row():
                refresh_button = gr.Button(
                    i18n("Refresh Models 🔁"), variant="secondary"
                )
                demixing_button = gr.Button(value=i18n("Demixing"), variant="primary")
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Whisper subtitles')}</h4></center>")
                asr_engine = user_config.get("asr_engine", "faster-whisper")
                asr_engine_dropdown = gr.Dropdown(
                    label=i18n("Whisper Engine"),
                    choices=studio.get_asr_engines(),
                    value=asr_engine,
                    info=i18n(""),
                )

                whisper_model_name = user_config.get(
                    f"{asr_engine.replace('-', '_')}_model", "large"
                )
                whisper_model_dropdown = gr.Dropdown(
                    label=i18n("Whisper Model"),
                    choices=studio.get_whisper_models(),
                    value=whisper_model_name,
                    info=i18n(""),
                )
                whisper_language_dropdown = gr.Dropdown(
                    label=i18n("Media Language"),
                    choices=studio.get_whisper_languages(),
                    value=user_config.get("whisper_language", "english"),
                    info=i18n(""),
                )
                compute_type_dropdown = gr.Dropdown(
                    label=i18n("Compute Type"),
                    choices=studio.get_whisper_compute_types(),
                    value=user_config.get("whisper_compute_type", "default"),
                    info=i18n("Only for faster-whisper"),
                )
                highlight_checkbox = gr.Checkbox(
                    label=i18n("Highlight Words"),
                    value=user_config.get("whisper_highlight_words", False),
                )
                denoise_level = gr.Slider(
                    minimum=0,
                    maximum=2,
                    step=1,
                    value=user_config.get("denoise_level", 0),
                    label=i18n("Denoise Level"),
                )

            with gr.Row():
                whisper_button = gr.Button(value=i18n("Transcribe"), variant="primary")

    clear_button.add([media_file, mic_audio, url_text])
    submit_button.click(
        studio.upload_source,
        inputs=[
            media_file,
            mic_audio,
            url_text,
            youtube_quality_radio,
            audio_format_radio,
        ],
        outputs=[input_video, input_audio, output_files],
    )

    workspace_button.click(studio.open_workspace_folder)
    temp_button.click(studio.open_temp_folder)

    refresh_button.click(
        studio.update_demixing_models, None, outputs=[demixing_model_dropdown]
    )
    demixing_button.click(
        studio.demixing,
        inputs=[demixing_model_dropdown, demixing_format_radio],
        outputs=[
            demixing_video1,
            demixing_audio1,
            demixing_video2,
            demixing_audio2,
            output_files,
        ],
    )

    asr_engine_dropdown.change(
        studio.update_whisper_models,
        inputs=[asr_engine_dropdown],
        outputs=[whisper_model_dropdown],
    )
    whisper_button.click(
        studio.transcribe,
        inputs=[
            asr_engine_dropdown,
            whisper_model_dropdown,
            whisper_language_dropdown,
            compute_type_dropdown,
            highlight_checkbox,
            denoise_level,
        ],
        outputs=[input_video, demixing_video1, demixing_video2, output_files],
    )
