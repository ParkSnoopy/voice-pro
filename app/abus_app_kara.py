import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import platform
import torch
import gradio as gr
from src.config import UserConfig

import src.ui as ui
from src.i18n.i18n import I18nAuto

i18n = I18nAuto()

import structlog
import logging


logging.getLogger("faster_whisper").setLevel(logging.WARNING)

level = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, level)
structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING)
)
logger = structlog.get_logger()


from app.abus_genuine import *
from app.tab_karaoke import karaoke_tab
from app.tab_demixing import demixing_tab
from app.tab_subtitle import subtitle_tab


##############################################################################################
# Gradio
##############################################################################################


def create_ui(user_config: UserConfig):
    # css/js strings
    css = ui.css
    js = ui.js

    with gr.Blocks(title="Kara Audio", css=css, theme=ui.theme) as gradio_interface:
        gr.HTML(f"<center><h6>{i18n('')}</h6></center>")

        with gr.Tab(i18n("Kara Audio")):
            karaoke_tab(user_config)

        with gr.Tab(i18n("Demixing")):
            demixing_tab(user_config)

        with gr.Tab(i18n("Subtitle")):
            subtitle_tab(user_config)

        create_app_footer()

        gradio_interface.load(
            None,
            None,
            None,
            js="() => document.getElementsByTagName('body')[0].classList.add('dark')",
        )
        gradio_interface.load(None, None, None, js=f"() => {{{js}}}")

    gradio_interface.launch(
        share=False,
        inbrowser=True,
        **user_config.get_gradio_launch_kwargs(default_port=7890),
    )


def create_app_footer():
    gradio_version = gr.__version__
    python_version = platform.python_version()
    torch_version = torch.__version__

    footer_items = ["🔊 [kara-audio](https://github.com/abus-aikorea/kara-audio)"]
    footer_items.append(f"python: `{python_version}`")
    footer_items.append(f"torch: `{torch_version}`")
    footer_items.append(f"gradio: `{gradio_version}`")

    genuine = "activated version"
    footer_items.append(f"{genuine}")

    gr.Markdown(
        " | ".join(footer_items),
        elem_classes=["no-translate"],
    )
