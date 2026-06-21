import os
import sys
import platform

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import gradio as gr
from src.config import UserConfig

from src.i18n.i18n import I18nAuto

i18n = I18nAuto()

from app.gradio_tts_kokoro import *
from app.gradio_voice_kokoro import *


def tts_kokoro_tab(user_config: UserConfig):
    tts = GradioKokoroTTS(user_config)
    kokoro_voice = GradioKokoroVoice(user_config)
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
    system = platform.system()

    with gr.Row():
        with gr.Column(scale=4):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Voice')}</h4></center>")
                kokoro_language_dropdown = gr.Dropdown(
                    label=i18n("Language"),
                    choices=kokoro_voice.gradio_languages(),
                    value=kokoro_voice.selected_language,
                )
                kokoro_voice_dropdown = gr.Dropdown(
                    label=i18n("Voice"),
                    choices=kokoro_voice.gradio_voices(),
                    value=user_config.get("kokoro_voice", "🚺 Heart ❤️"),
                )
                kokoro_sample_audio = gr.Audio(
                    label="Sample Audio",
                    type="filepath",
                    editable=False,
                    interactive=False,
                    show_download_button=False,
                )
                kokoro_transcript = gr.Textbox(
                    label=i18n("Transcript"),
                    interactive=False,
                    max_lines=6,
                    lines=3,
                    placeholder=i18n("Optional"),
                )

        with gr.Column(scale=8):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Script')}</h4></center>")
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
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Synthesized voice')}</h4></center>")
                dubbing_audio = gr.Audio(
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

        with gr.Column(scale=4):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Speech Generation')}</h4></center>")
                kokoro_tts_speed = gr.Slider(
                    0.3,
                    2.0,
                    value=1.0,
                    step=0.1,
                    label=i18n("Speech rate"),
                    info="0.3 ~ 2.0",
                )
                audio_format_radio = gr.Radio(
                    label=i18n("Audio Format"),
                    choices=["wav", "flac", "mp3"],
                    value=user_config.get("audio_format", "mp3"),
                )
            with gr.Row():
                kokoro_default_button = gr.ClearButton(value=i18n("Load Defaults"))
                kokoro_dubbing_button = gr.Button(
                    value=i18n("Synthesis"), variant="primary"
                )

    # AI debbing
    dubbing_file_in.upload(
        tts.gradio_upload_file,
        inputs=[dubbing_file_in],
        outputs=[kokoro_language_dropdown, dubbing_text_in],
    )

    kokoro_default_button.click(
        tts.gradio_kokoro_default, outputs=[kokoro_tts_speed, audio_format_radio]
    )

    workspace_button.click(tts.gradio_workspace_folder)
    temp_button.click(tts.gradio_temp_folder)

    kokoro_language_dropdown.change(
        kokoro_voice.gradio_change_language,
        inputs=[kokoro_language_dropdown],
        outputs=[kokoro_voice_dropdown],
    )

    kokoro_voice_dropdown.change(
        kokoro_voice.gradio_change_voice,
        inputs=[kokoro_voice_dropdown],
        outputs=[kokoro_sample_audio, kokoro_transcript],
    )

    kokoro_dubbing_button.click(
        tts.gradio_tts_dubbing,
        inputs=[
            dubbing_text_in,
            kokoro_language_dropdown,
            kokoro_voice_dropdown,
            kokoro_tts_speed,
            audio_format_radio,
        ],
        outputs=[dubbing_file_out, dubbing_audio],
    )
