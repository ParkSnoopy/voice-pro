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

from app.gradio_translate import *


def translate_tab(user_config: UserConfig):
    translate = GradioTranslate(user_config)
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
        with gr.Column():
            with gr.Row():
                with gr.Group():
                    gr.HTML(f"<center><h4>{i18n('Upload subtitle')}</h4></center>")
                    # gr.HTML(f'<center><h6>{i18n("Formats")}: {i18n("ass, ssa, srt, mpl2, tmp, vtt, microdvd, json")}</h6></center>')
                    source_language = gr.Dropdown(
                        label=i18n("Source Language"),
                        choices=translate.gradio_translate_languages(),
                        value=user_config.get("translate_source_language", "English"),
                    )
                    translate_file_in = gr.File(
                        label=i18n("Subtitle File"),
                        type="filepath",
                        file_count="single",
                        file_types=subtitle_exts,
                    )
                    source_srt = gr.Textbox(
                        label=i18n("Source Text"),
                        interactive=True,
                        show_label=True,
                        max_lines=24,
                        show_copy_button=True,
                        placeholder=i18n("Placeholder for Source Text"),
                        lines=10,
                    )
                with gr.Group():
                    gr.HTML(f"<center><h4>{i18n('Target Text')}</h4></center>")
                    translate_language = gr.Dropdown(
                        label=i18n("Translated Language"),
                        choices=translate.gradio_translate_languages(),
                        value=user_config.get("translate_target_language", "English"),
                    )
                    translate_file_out = gr.File(
                        label=i18n("Subtitle File"),
                        interactive=False,
                        type="filepath",
                        file_count="single",
                        file_types=subtitle_exts,
                    )
                    target_srt = gr.Textbox(
                        label=i18n("Translated captions"),
                        interactive=False,
                        show_label=True,
                        max_lines=24,
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
                start_btn = gr.Button(value=i18n("Translate"), variant="primary")
                clear_button = gr.ClearButton(value=i18n("🧹Clear"))
                save_button = gr.Button(value="💾 Save")

    translate_file_in.upload(
        translate.gradio_upload_file,
        inputs=[translate_file_in],
        outputs=[source_language, source_srt],
    )

    start_btn.click(
        fn=translate.gradio_translate,
        inputs=[source_srt, source_language, translate_language],
        outputs=[translate_file_out, target_srt],
    )

    workspace_button.click(translate.gradio_workspace_folder)
    temp_button.click(translate.gradio_temp_folder)

    save_button.click(
        translate.gradio_save,
        inputs=[
            translate_file_in,
            source_language,
            translate_language,
            source_srt,
            target_srt,
        ],
    )
    clear_button.add([translate_file_in, source_srt, translate_file_out, target_srt])
