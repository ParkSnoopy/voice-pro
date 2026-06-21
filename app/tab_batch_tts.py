import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import gradio as gr
from src.config import UserConfig

from src.i18n.i18n import I18nAuto

i18n = I18nAuto()


from app.gradio_batch_tts import *
from app.gradio_voice_ms import *


def batch_tts_tab(user_config: UserConfig):
    batch = GradioBatchTTS(user_config)
    ms_voice = GradioMSVoice(user_config)
    ms_voice.selected_language = user_config.get("ms_language", "English")

    with gr.Row():
        with gr.Column(scale=3):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Settings')}</h4></center>")
                with gr.Row():
                    folder_path_text = gr.Textbox(
                        label=i18n("Select folder"),
                        value=user_config.get("last_folder", "."),
                    )
                    folder_button = gr.Button(
                        value=i18n("📂"), elem_id="batch_select_folder_btn"
                    )
                audio_format_radio = gr.Radio(
                    label=i18n("Audio Format"),
                    choices=["wav", "flac", "mp3"],
                    value=user_config.get("audio_format", "flac"),
                )
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Whisper subtitles')}</h4></center>")
                asr_engine = user_config.get("asr_engine", "faster-whisper")
                asr_engine_radio = gr.Radio(
                    label=i18n("Whisper Engine"),
                    choices=batch.get_asr_engines(),
                    value=asr_engine,
                )

                whisper_model_name = user_config.get(
                    f"{asr_engine.replace('-', '_')}_model", "large"
                )
                whisper_model_dropdown = gr.Dropdown(
                    label=i18n("Whisper Model"),
                    choices=batch.get_whisper_models(),
                    value=whisper_model_name,
                    info=i18n(""),
                )
                whisper_language_dropdown = gr.Dropdown(
                    label=i18n("Media Language"),
                    choices=batch.get_whisper_languages(),
                    value=user_config.get("whisper_language", "english"),
                    info=i18n(""),
                )
                compute_type_dropdown = gr.Dropdown(
                    label=i18n("Compute Type"),
                    choices=batch.get_whisper_compute_types(),
                    value=user_config.get("whisper_compute_type", "default"),
                    info=i18n("Only for faster-whisper"),
                )
                denoise_level = gr.Slider(
                    minimum=0,
                    maximum=2,
                    step=1,
                    value=user_config.get("denoise_level", 0),
                    label=i18n("Denoise Level"),
                )
            with gr.Row():
                clear_button = gr.ClearButton(value=i18n("Clear"))
                whisper_button = gr.Button(value=i18n("Transcribe"), variant="primary")

        with gr.Column(scale=8):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Output files')}</h4></center>")
                output_files = gr.File(
                    label=i18n("Files"),
                    type="filepath",
                    file_count="multiple",
                    interactive=False,
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
                gr.HTML(f"<center><h4>{i18n('Translation')}</h4></center>")
                source_language = gr.Dropdown(
                    label=i18n("Source Language"),
                    choices=batch.gradio_translate_languages(),
                    value=user_config.get("translate_source_language", "English"),
                )
                translate_language = gr.Dropdown(
                    label=i18n("Translated Language"),
                    choices=batch.gradio_translate_languages(),
                    value=user_config.get("translate_source_language", "English"),
                )
            translate_button = gr.Button(value=i18n("Translate"), variant="primary")

            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Speech Generation')}</h4></center>")
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
            with gr.Row():
                tts_default_button = gr.ClearButton(value=i18n("Load Defaults"))
                tts_button = gr.Button(value=i18n("Synthesis"), variant="primary")

    folder_button.click(batch.gradio_select_folder, outputs=[folder_path_text])
    clear_button.add([folder_path_text])

    asr_engine_radio.change(
        batch.update_whisper_models,
        inputs=[asr_engine_radio],
        outputs=[whisper_model_dropdown],
    )
    whisper_button.click(
        batch.gradio_whisper,
        inputs=[
            folder_path_text,
            audio_format_radio,
            asr_engine_radio,
            whisper_model_dropdown,
            whisper_language_dropdown,
            compute_type_dropdown,
            denoise_level,
        ],
        outputs=[output_files],
    )

    workspace_button.click(batch.gradio_workspace_folder)
    temp_button.click(batch.gradio_temp_folder)

    translate_button.click(
        batch.gradio_translate_batch,
        inputs=[source_language, translate_language],
        outputs=[output_files],
    )

    ms_language_dropdown.change(
        ms_voice.gradio_change_language,
        inputs=[ms_language_dropdown],
        outputs=[ms_voice_dropdown],
    )

    tts_default_button.click(
        batch.gradio_default_tts,
        outputs=[edge_tts_rate, edge_tts_volume, edge_tts_pitch],
    )

    tts_button.click(
        batch.gradio_dubbing_batch,
        inputs=[
            ms_voice_dropdown,
            edge_tts_pitch,
            edge_tts_rate,
            edge_tts_volume,
            audio_format_radio,
        ],
        outputs=[output_files],
    )
