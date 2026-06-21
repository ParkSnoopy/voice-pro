import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import gradio as gr
from src.config import UserConfig

from src.i18n.i18n import I18nAuto

i18n = I18nAuto()


from app.gradio_demixing import *
from app.abus_hf import AbusHuggingFace


def demixing_tab(user_config: UserConfig):
    demixer = GradioDemixing(user_config)
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
                open_workspace_button = gr.Button(
                    value=i18n("🗂️ Open workspace folder"), variant="secondary"
                )
                open_temp_button = gr.Button(
                    value=i18n("🗀 Open Temp folder"), variant="secondary"
                )

        with gr.Column(scale=3):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Download MDX Models')}</h4></center>")
                remote_demixing_model_dropdown = gr.Dropdown(
                    label=i18n("MDX Models"),
                    choices=AbusHuggingFace.hf_demixing_names(False),
                    value=None,
                )
                download_info_textbox = gr.Textbox(
                    label=i18n("Model information"),
                    value=i18n("Select a model to download"),
                    interactive=False,
                )
            with gr.Row():
                open_model_folder_button = gr.Button(
                    value=i18n("Open Model folder"), variant="secondary"
                )
                download_model_button = gr.Button(
                    value=i18n("Download"), variant="primary"
                )

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

    clear_button.add(
        [
            input_video,
            input_audio,
            demixing_video1,
            demixing_audio1,
            demixing_video2,
            demixing_audio2,
        ]
    )
    submit_button.click(
        demixer.upload_source,
        inputs=[
            media_file,
            mic_audio,
            url_text,
            youtube_quality_radio,
            audio_format_radio,
        ],
        outputs=[input_video, input_audio, output_files],
    )

    open_workspace_button.click(demixer.open_workspace_folder)
    open_temp_button.click(demixer.open_temp_folder)

    refresh_button.click(
        demixer.update_demixing_models,
        None,
        outputs=[demixing_model_dropdown, remote_demixing_model_dropdown],
    )
    demixing_button.click(
        demixer.demixing,
        inputs=[demixing_model_dropdown, demixing_format_radio],
        outputs=[
            demixing_video1,
            demixing_audio1,
            demixing_video2,
            demixing_audio2,
            output_files,
        ],
    )
    open_model_folder_button.click(demixer.open_model_folder)

    remote_demixing_model_dropdown.change(
        demixer.show_model_info,
        inputs=[remote_demixing_model_dropdown],
        outputs=[download_info_textbox],
    )
    download_model_button.click(
        demixer.download_model,
        inputs=[remote_demixing_model_dropdown],
        outputs=[download_info_textbox],
    )
