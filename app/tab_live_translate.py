import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import gradio as gr
from src.config import UserConfig

from src.i18n.i18n import I18nAuto

i18n = I18nAuto()


from app.gradio_live_translate import *


def live_translate_tab(user_config: UserConfig):
    live = GradioLiveTranslate(user_config)
    with gr.Row():
        with gr.Column(scale=3):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Settings')}</h4></center>")
                audio_source = gr.Dropdown(
                    label=i18n("Audio Source"), choices=live.get_audio_sources()
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
                    choices=live.get_asr_engines(),
                    value=asr_engine,
                )

                whisper_model_name = user_config.get(
                    f"{asr_engine.replace('-', '_')}_model", "large"
                )
                whisper_model_dropdown = gr.Dropdown(
                    label=i18n("Whisper Model"),
                    choices=live.get_whisper_models(),
                    value=whisper_model_name,
                    info=i18n(""),
                )
                whisper_language_dropdown = gr.Dropdown(
                    label=i18n("Audio Language"),
                    choices=live.get_whisper_languages(),
                    value=user_config.get("whisper_language", "english"),
                )
                compute_type_dropdown = gr.Dropdown(
                    label=i18n("Compute Type"),
                    choices=live.get_whisper_compute_types(),
                    value=live.get_whisper_default_compute_type(),
                    info=i18n("Only for faster-whisper"),
                )
                denoise_level = gr.Slider(
                    minimum=0,
                    maximum=2,
                    step=1,
                    value=user_config.get("denoise_level", 0),
                    label=i18n("Denoise Level"),
                )
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Translation')}</h4></center>")
                source_language = gr.Dropdown(
                    label=i18n("Source Language"),
                    choices=live.get_translate_languages(),
                    value=user_config.get("translate_source_language", "English"),
                )
                translate_language = gr.Dropdown(
                    label=i18n("Translated Language"),
                    choices=live.get_translate_languages(),
                    value=user_config.get("translate_target_language", "English"),
                )
            with gr.Row():
                start_btn = gr.Button(value=i18n("Start"), variant="primary")
                stop_btn = gr.Button(value=i18n("Stop"), variant="secondary")

        with gr.Column(scale=11):
            with gr.Row():
                with gr.Group():
                    gr.HTML(f"<center><h4>{i18n('Live Transcriptions')}</h4></center>")
                    source_vtt = gr.Textbox(
                        label=i18n("Live Transcriptions"),
                        interactive=False,
                        show_label=True,
                        value=live.get_transcriptions(),
                        every=0.5,
                        max_lines=34,
                        show_copy_button=True,
                        placeholder=i18n("Placeholder for Source VTT"),
                        lines=10,
                    )
                with gr.Group():
                    gr.HTML(f"<center><h4>{i18n('Live Translations')}</h4></center>")
                    target_vtt = gr.Textbox(
                        label=i18n("Live Translations"),
                        interactive=False,
                        show_label=True,
                        value=live.get_translations(),
                        every=0.5,
                        max_lines=34,
                        show_copy_button=True,
                        lines=10,
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

    workspace_button.click(live.gradio_workspace_folder)
    temp_button.click(live.gradio_temp_folder)
    save_button.click(live.gradio_save, inputs=[audio_format_radio])
    clear_button.click(fn=live.gradio_clear, outputs=[source_vtt, target_vtt])

    asr_engine_radio.change(
        live.update_whisper_models,
        inputs=[asr_engine_radio],
        outputs=[whisper_model_dropdown],
    )

    start_btn.click(
        fn=live.gradio_start,
        inputs=[
            audio_source,
            asr_engine_radio,
            whisper_model_dropdown,
            whisper_language_dropdown,
            compute_type_dropdown,
            denoise_level,
            source_language,
            translate_language,
        ],
    )
    stop_btn.click(fn=live.gradio_stop)
