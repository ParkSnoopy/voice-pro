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

from app.gradio_tts_f5 import *
from app.gradio_voice_celeb import *


def tts_f5_multi_tab(user_config: UserConfig):
    tts = GradioF5TTS(user_config)
    voice_spk1 = GradioCelebVoice(user_config)
    voice_spk2 = GradioCelebVoice(user_config)
    system = platform.system()

    with gr.Row():
        with gr.Column(scale=4):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Speaker 1')}</h4></center>")
                language_radio_spk1 = gr.Radio(
                    choices=voice_spk1.gradio_f5_languages(),
                    label=i18n("Language"),
                    value="English",
                )
                celeb_voice_dropdown_spk1 = gr.Dropdown(
                    label=i18n("Voice"), choices=voice_spk1.gradio_voices(), value=None
                )
                celeb_audio_spk1 = gr.Audio(
                    label="Reference Audio",
                    sources=["upload", "microphone"],
                    type="filepath",
                    interactive=True,
                )
                celeb_transcript_spk1 = gr.Textbox(
                    label=i18n("Transcript"),
                    interactive=True,
                    max_lines=12,
                    lines=6,
                    placeholder=i18n("Optional"),
                )
                celeb_image_spk1 = gr.Image(
                    label="Photo",
                    type="filepath",
                    interactive=False,
                    show_download_button=False,
                )
            with gr.Row():
                add_button_spk1 = gr.Button(
                    value=i18n("Add Label: {spk1}"), variant="primary"
                )
        with gr.Column(scale=8):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Script')}</h4></center>")
                dubbing_text_in = gr.Textbox(
                    label=i18n("Source Text"),
                    interactive=True,
                    show_label=False,
                    max_lines=24,
                    show_copy_button=True,
                    placeholder=i18n("Placeholder for Podcast script"),
                    lines=10,
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
                gr.HTML(f"<center><h4>{i18n('Speaker 2')}</h4></center>")
                language_radio_spk2 = gr.Radio(
                    choices=voice_spk2.gradio_f5_languages(),
                    label=i18n("Language"),
                    value="English",
                )
                celeb_voice_dropdown_spk2 = gr.Dropdown(
                    label=i18n("Voice"), choices=voice_spk2.gradio_voices(), value=None
                )
                celeb_audio_spk2 = gr.Audio(
                    label="Reference Audio",
                    sources=["upload", "microphone"],
                    type="filepath",
                    interactive=True,
                )
                celeb_transcript_spk2 = gr.Textbox(
                    label=i18n("Transcript"),
                    interactive=True,
                    max_lines=12,
                    lines=6,
                    placeholder=i18n("Optional"),
                )
                celeb_image_spk2 = gr.Image(
                    label="Photo",
                    type="filepath",
                    interactive=False,
                    show_download_button=False,
                )
            with gr.Row():
                add_button_spk2 = gr.Button(
                    value=i18n("Add Label: {spk2}"), variant="primary"
                )
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Speech Generation')}</h4></center>")
                model_choice = gr.Dropdown(
                    choices=tts.gradio_available_models(),
                    label="Choose Model",
                    value="SWivid/F5-TTS_v1",
                )
                f5_tts_speed = gr.Slider(
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
                f5_default_button = gr.ClearButton(value=i18n("Load Defaults"))
                dubbing_button = gr.Button(value=i18n("Synthesis"), variant="primary")

    # AI debbing

    workspace_button.click(tts.gradio_workspace_folder)
    temp_button.click(tts.gradio_temp_folder)

    language_radio_spk1.change(
        voice_spk1.gradio_change_language,
        inputs=[language_radio_spk1],
        outputs=[celeb_voice_dropdown_spk1],
    )

    celeb_voice_dropdown_spk1.change(
        voice_spk1.gradio_change_voice,
        inputs=[celeb_voice_dropdown_spk1],
        outputs=[celeb_audio_spk1, celeb_transcript_spk1, celeb_image_spk1],
    )

    celeb_audio_spk1.clear(
        voice_spk1.gradio_clear_voice,
        inputs=None,
        outputs=[celeb_transcript_spk1, celeb_image_spk1],
    )

    add_button_spk1.click(
        tts.gradio_add_label_spk1, inputs=[dubbing_text_in], outputs=[dubbing_text_in]
    )

    language_radio_spk2.change(
        voice_spk2.gradio_change_language,
        inputs=[language_radio_spk2],
        outputs=[celeb_voice_dropdown_spk2],
    )

    celeb_voice_dropdown_spk2.change(
        voice_spk2.gradio_change_voice,
        inputs=[celeb_voice_dropdown_spk2],
        outputs=[celeb_audio_spk2, celeb_transcript_spk2, celeb_image_spk2],
    )

    celeb_audio_spk2.clear(
        voice_spk2.gradio_clear_voice,
        inputs=None,
        outputs=[celeb_transcript_spk2, celeb_image_spk2],
    )

    add_button_spk2.click(
        tts.gradio_add_label_spk2, inputs=[dubbing_text_in], outputs=[dubbing_text_in]
    )

    f5_default_button.click(
        tts.gradio_f5_default, outputs=[model_choice, f5_tts_speed, audio_format_radio]
    )

    dubbing_button.click(
        tts.gradio_tts_dubbing_multi,
        inputs=[
            dubbing_text_in,
            celeb_audio_spk1,
            celeb_transcript_spk1,
            celeb_audio_spk2,
            celeb_transcript_spk2,
            model_choice,
            f5_tts_speed,
            audio_format_radio,
        ],
        outputs=[dubbing_audio, dubbing_file_out],
    )
