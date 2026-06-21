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

from app.gradio_tts_edge import *
from app.gradio_voice_ms import *


def tts_edge_tab(user_config: UserConfig):
    tts = GradioEdgeTTS(user_config)
    ms_voice = GradioMSVoice(user_config)
    ms_voice.selected_language = user_config.get("ms_language", "English")
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
                ms_language_dropdown = gr.Dropdown(
                    label=i18n("Language"),
                    choices=ms_voice.gradio_languages(),
                    value=ms_voice.selected_language,
                )
                ms_voice_dropdown = gr.Dropdown(
                    label=i18n("Voice"),
                    choices=ms_voice.gradio_voices(),
                    value=user_config.get("ms_voice", "UNITED STATES-Ana-Female"),
                )
                ms_sample_audio = gr.Audio(
                    label="Sample Audio",
                    type="filepath",
                    editable=False,
                    interactive=False,
                    show_download_button=False,
                )
                # sample_transcript = gr.Textbox(label=i18n("Transcript"), interactive=False, show_label=True,
                #                               max_lines=12, show_copy_button=True, lines=6)

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
                    value=user_config.get("audio_format", "mp3"),
                )
            with gr.Row():
                edge_default_button = gr.ClearButton(value=i18n("Load Defaults"))
                edge_dubbing_button = gr.Button(
                    value=i18n("Synthesis"), variant="primary"
                )

    # AI debbing
    dubbing_file_in.upload(
        tts.gradio_upload_file,
        inputs=[dubbing_file_in],
        outputs=[ms_language_dropdown, dubbing_text_in],
    )

    edge_default_button.click(
        tts.gradio_edge_default,
        outputs=[edge_tts_rate, edge_tts_volume, edge_tts_pitch, audio_format_radio],
    )

    workspace_button.click(tts.gradio_workspace_folder)
    temp_button.click(tts.gradio_temp_folder)

    ms_language_dropdown.change(
        ms_voice.gradio_change_language,
        inputs=[ms_language_dropdown],
        outputs=[ms_voice_dropdown],
    )

    ms_voice_dropdown.change(
        ms_voice.gradio_change_voice,
        inputs=[ms_voice_dropdown],
        outputs=[ms_sample_audio],
    )

    edge_dubbing_button.click(
        tts.gradio_tts_dubbing,
        inputs=[
            dubbing_text_in,
            ms_voice_dropdown,
            edge_tts_pitch,
            edge_tts_rate,
            edge_tts_volume,
            audio_format_radio,
        ],
        outputs=[dubbing_file_out, dubbing_audio],
    )
