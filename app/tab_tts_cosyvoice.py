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

from app.gradio_tts_cosyvoice import *
from app.gradio_voice_celeb import *


def tts_cosyvoice_tab(user_config: UserConfig):
    tts = GradioCosyVoice(user_config)
    cosy_reference_voice = GradioCelebVoice(user_config)
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
                cosy_language_radio = gr.Radio(
                    choices=cosy_reference_voice.gradio_languages(),
                    label=i18n("Language"),
                    value="English",
                )
                cosy_voice_dropdown = gr.Dropdown(
                    label=i18n("Voice"),
                    choices=cosy_reference_voice.gradio_voices(),
                    value=None,
                )
                cosy_reference_audio = gr.Audio(
                    label="Reference Audio",
                    sources=["upload", "microphone"],
                    type="filepath",
                    interactive=True,
                )
                cosy_reference_transcript = gr.Textbox(
                    label=i18n("Transcript"),
                    interactive=True,
                    max_lines=12,
                    lines=6,
                    placeholder=i18n("Required"),
                )
                cosy_reference_image = gr.Image(
                    label="Photo",
                    type="filepath",
                    interactive=False,
                    show_download_button=False,
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
                cosy_mode_choice = gr.Radio(
                    choices=["Zero-Shot", "Cross-Lingual", "Instruct"],
                    label="Inference Mode",
                    value="Zero-Shot",
                )
                cosy_tts_speed = gr.Slider(
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
                cosy_default_button = gr.ClearButton(value=i18n("Load Defaults"))
                cosy_dubbing_button = gr.Button(
                    value=i18n("Synthesis"), variant="primary"
                )

    # AI debbing
    dubbing_file_in.upload(
        tts.gradio_upload_file, inputs=[dubbing_file_in], outputs=[dubbing_text_in]
    )

    workspace_button.click(tts.gradio_workspace_folder)
    temp_button.click(tts.gradio_temp_folder)

    cosy_language_radio.change(
        cosy_reference_voice.gradio_change_language,
        inputs=[cosy_language_radio],
        outputs=[cosy_voice_dropdown],
    )

    cosy_voice_dropdown.change(
        cosy_reference_voice.gradio_change_voice,
        inputs=[cosy_voice_dropdown],
        outputs=[cosy_reference_audio, cosy_reference_transcript, cosy_reference_image],
    )

    cosy_reference_audio.clear(
        cosy_reference_voice.gradio_clear_voice,
        inputs=None,
        outputs=[cosy_reference_transcript, cosy_reference_image],
    )

    cosy_default_button.click(
        tts.gradio_cosy_default,
        outputs=[cosy_mode_choice, cosy_tts_speed, audio_format_radio],
    )

    cosy_dubbing_button.click(
        tts.gradio_tts_dubbing_single,
        inputs=[
            dubbing_text_in,
            cosy_reference_audio,
            cosy_reference_transcript,
            cosy_mode_choice,
            cosy_tts_speed,
            audio_format_radio,
        ],
        outputs=[dubbing_audio, dubbing_file_out],
    )
