import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import gradio as gr
from src.config import UserConfig

from src.i18n.i18n import I18nAuto

i18n = I18nAuto()

from app.gradio_tts_rvc import *


def tts_rvc_tab(user_config: UserConfig):
    tts_rvc = GradioTTSRVC(user_config)
    subtitle_exts = [
        ".ass",
        ".ssa",
        ".srt",
        ".mpl2",
        ".tmp",
        ".vtt",
        ".microdvd",
        ".json",
    ]

    with gr.Row():
        with gr.Column(scale=11):
            with gr.Row():
                with gr.Column():
                    with gr.Group():
                        gr.HTML(f"<center><h4>{i18n('Upload subtitle')}</h4></center>")
                        # gr.HTML(f'<center><h6>{i18n("Formats")}: {i18n("ass, ssa, srt, mpl2, tmp, vtt, microdvd, json")}</h6></center>')
                        dubbing_file_in = gr.File(
                            label=i18n("Subtitle File"),
                            type="filepath",
                            file_count="single",
                            file_types=subtitle_exts,
                        )
                        dubbing_text_in = gr.Textbox(
                            label=i18n("Source Text"),
                            interactive=True,
                            show_label=True,
                            max_lines=24,
                            show_copy_button=True,
                            placeholder=i18n("Placeholder for Source Text"),
                            lines=5,
                        )
                with gr.Column():
                    with gr.Group():
                        gr.HTML(
                            f"<center><h4>{i18n('Synthesized voice')}</h4></center>"
                        )
                        tts_audio = gr.Audio(
                            label=i18n("Audio"), type="filepath", interactive=False
                        )
                        rvc_audio = gr.Audio(
                            label=i18n("Audio"), type="filepath", interactive=False
                        )
                        dubbing_file_out = gr.File(
                            label=i18n("File"),
                            type="filepath",
                            file_count="single",
                            interactive=False,
                        )
            with gr.Row():
                workspace_button = gr.Button(
                    value=i18n("🗂️ Open workspace folder"), variant="secondary"
                )
                temp_button = gr.Button(
                    value=i18n("🗀 Open Temp folder"), variant="secondary"
                )
                clear_button = gr.ClearButton(value=i18n("🧹Clear"))
                save_button = gr.Button(value="💾 Save")
        with gr.Column(scale=3):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('RVC')}</h4></center>")
                rvc_voice = gr.Dropdown(
                    label=i18n("RVC Voice"),
                    choices=tts_rvc.gradio_rvc_models(),
                    value=user_config.get("rvc_voice"),
                )
                with gr.Row():
                    refresh_button = gr.Button(
                        i18n("Refresh Models 🔁"), variant="primary"
                    )
                    rvc_voice_button = gr.Button(
                        value=i18n("Open Model folder"), variant="secondary"
                    )
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Speech Generation')}</h4></center>")
                ms_language_dropdown = gr.Dropdown(
                    label=i18n("Language"),
                    choices=tts_rvc.gradio_translate_languages(),
                    value=user_config.get("ms_language", "English"),
                )
                ms_voice_dropdown = gr.Dropdown(
                    label=i18n("Voice"),
                    choices=tts_rvc.get_tts_voices(),
                    value=user_config.get("ms_voice", "UNITED STATES-Ana-Female"),
                )
                edge_tts_pitch = gr.Slider(
                    -400,
                    400,
                    value=user_config.get("edge_tts_pitch", 0),
                    step=10,
                    label=i18n("Pitch(Hz)"),
                    info="-400Hz ~ +400Hz",
                )
                edge_tts_rate = gr.Slider(
                    -100,
                    200,
                    value=user_config.get("edge_tts_rate", 0),
                    step=1,
                    label=i18n("Speech rate"),
                    info="-100% ~ +200%",
                )
                edge_tts_volume = gr.Slider(
                    -100,
                    100,
                    value=user_config.get("edge_tts_volume", 0),
                    step=1,
                    label=i18n("Speech volume"),
                    info="-100% ~ +100%",
                )
                audio_format_radio = gr.Radio(
                    label=i18n("Audio Format"),
                    choices=["wav", "flac", "mp3"],
                    value=user_config.get("audio_format", "flac"),
                )
            with gr.Row():
                dubbing_default_button = gr.ClearButton(value=i18n("Load Defaults"))
                dubbing_button = gr.Button(value=i18n("Synthesis"), variant="primary")

    # AI debbing
    dubbing_file_in.upload(
        tts_rvc.gradio_upload_file,
        inputs=[dubbing_file_in],
        outputs=[ms_language_dropdown, dubbing_text_in],
    )

    dubbing_default_button.click(
        tts_rvc.gradio_default,
        outputs=[edge_tts_rate, edge_tts_volume, edge_tts_pitch, rvc_voice],
    )

    workspace_button.click(tts_rvc.gradio_workspace_folder)
    temp_button.click(tts_rvc.gradio_temp_folder)

    ms_language_dropdown.change(
        tts_rvc.gradio_update_tts_voices,
        inputs=[ms_language_dropdown],
        outputs=[ms_voice_dropdown],
    )
    refresh_button.click(tts_rvc.gradio_update_rvc_voice, None, outputs=rvc_voice)
    rvc_voice_button.click(tts_rvc.gradio_rvc_voice_folder)

    dubbing_button.click(
        tts_rvc.gradio_deep_voice,
        inputs=[
            dubbing_text_in,
            ms_language_dropdown,
            ms_voice_dropdown,
            edge_tts_pitch,
            edge_tts_rate,
            edge_tts_volume,
            rvc_voice,
            audio_format_radio,
        ],
        outputs=[tts_audio, rvc_audio, dubbing_file_out],
    )

    save_button.click(
        tts_rvc.gradio_save,
        inputs=[
            dubbing_file_in,
            ms_language_dropdown,
            audio_format_radio,
            dubbing_text_in,
            tts_audio,
        ],
    )
    clear_button.add(
        [dubbing_file_in, dubbing_text_in, tts_audio, rvc_audio, dubbing_file_out]
    )
