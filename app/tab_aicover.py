import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import gradio as gr
from src.config import UserConfig

from src.i18n.i18n import I18nAuto

i18n = I18nAuto()

from app.abus_genuine import *
from app.gradio_aicover import *


def aicover_tab(user_config: UserConfig):
    aicover = GradioAICover(user_config)

    with gr.Row():
        with gr.Column(scale=3):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Upload media')}</h4></center>")
                original_file = gr.File(
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
                    youtube_format_radio = gr.Radio(
                        label=i18n("Audio Format"),
                        choices=["wav", "flac", "mp3"],
                        value=user_config.get("audio_format", "flac"),
                    )
            with gr.Row():
                clear_button = gr.ClearButton(value=i18n("Clear"))
                submit_button = gr.Button(value=i18n("Submit"), variant="primary")
        with gr.Column(scale=8):
            with gr.Row():
                with gr.Column():
                    with gr.Group():
                        gr.HTML(f"<center><h4>{i18n('Input Video')}</h4></center>")
                        input_video = gr.Video(label=i18n("Video"), interactive=False)
                        input_audio = gr.Audio(
                            label=i18n("Audio"), type="filepath", interactive=False
                        )
                with gr.Column():
                    with gr.Group():
                        gr.HTML(f"<center><h4>{i18n('Cover Video')}</h4></center>")
                        rvc_video = gr.Video(label=i18n("Video"), interactive=False)
                        rvc_audio = gr.Audio(
                            label=i18n("Audio"), type="filepath", interactive=False
                        )
            cover_files = gr.File(
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

        with gr.Column(scale=4):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('AI Cover')}</h4></center>")
                rvc_voice = gr.Dropdown(
                    label=i18n("Voice Models"),
                    choices=aicover.get_voice_models(),
                    value=user_config.get("rvc_voice"),
                )
                gr.HTML(
                    f'<center><h4>{i18n("Download voice models: ")}<a href="https://discord.com/channels/1159260121998827560/@home">Discord AI Hub</a></h4></center>'
                )

            with gr.Row():
                refresh_button = gr.Button(i18n("Refresh Models 🔁"), variant="primary")
                voice_model_button = gr.Button(
                    value=i18n("Open Model folder"), variant="secondary"
                )

            with gr.Tab(i18n("Pitch")):
                pitch_change = gr.Slider(
                    -3,
                    3,
                    value=user_config.get("pitch_change"),
                    step=1,
                    label=i18n("Pitch Change (Vocals ONLY)"),
                    info=i18n(
                        "Generally, use 1 for male to female conversions and -1 for vice-versa. (Octaves)"
                    ),
                )
                pitch_change_all = gr.Slider(
                    -12,
                    12,
                    value=user_config.get("pitch_change_all"),
                    step=1,
                    label=i18n("Overall Pitch Change"),
                    info=i18n(
                        "Changes pitch/key of vocals and instrumentals together. Altering this slightly reduces sound quality. (Semitones)"
                    ),
                )

            with gr.Tab(i18n("Voice conversion")):
                index_rate = gr.Slider(
                    0,
                    1,
                    value=user_config.get("index_rate"),
                    label=i18n("Index Rate"),
                    info=i18n(
                        "Controls how much of the AI voice's accent to keep in the vocals"
                    ),
                )
                filter_radius = gr.Slider(
                    0,
                    7,
                    value=user_config.get("filter_radius"),
                    step=1,
                    label=i18n("Filter radius"),
                    info=i18n(
                        "If >=3: apply median filtering median filtering to the harvested pitch results. Can reduce breathiness"
                    ),
                )
                rms_mix_rate = gr.Slider(
                    0,
                    1,
                    value=user_config.get("rms_mix_rate"),
                    label=i18n("RMS mix rate"),
                    info=i18n(
                        "Control how much to mimic the original vocal's loudness (0) or a fixed loudness (1)"
                    ),
                )
                protect = gr.Slider(
                    0,
                    0.5,
                    value=user_config.get("protect"),
                    label=i18n("Protect rate"),
                    info=i18n(
                        "Protect voiceless consonants and breath sounds. Set to 0.5 to disable."
                    ),
                )

            with gr.Tab(i18n("Mixing")):
                gr.HTML(f"<center><h4>{i18n('Volume Change (decibels)')}</h4></center>")
                with gr.Row():
                    main_vocal_gain = gr.Slider(
                        -20,
                        20,
                        value=user_config.get("main_vocal_gain"),
                        step=1,
                        label=i18n("Main Vocals"),
                    )
                    backup_vocal_gain = gr.Slider(
                        -20,
                        20,
                        value=user_config.get("backup_vocal_gain"),
                        step=1,
                        label=i18n("Backup Vocals"),
                    )
                    inst_gain = gr.Slider(
                        -20,
                        20,
                        value=user_config.get("inst_gain"),
                        step=1,
                        label=i18n("Instrumentals"),
                    )

                gr.HTML(f"<center><h4>{i18n('Reverb Control')}</h4></center>")
                with gr.Column():
                    reverb_rm_size = gr.Slider(
                        0,
                        1,
                        value=user_config.get("reverb_rm_size"),
                        label=i18n("Room size"),
                        info=i18n("The larger the room, the longer the reverb time"),
                    )
                    reverb_wet = gr.Slider(
                        0,
                        1,
                        value=user_config.get("reverb_wet"),
                        label=i18n("Wetness level"),
                        info=i18n("Level of AI vocals with reverb"),
                    )
                    reverb_dry = gr.Slider(
                        0,
                        1,
                        value=user_config.get("reverb_dry"),
                        label=i18n("Dryness level"),
                        info=i18n("Level of AI vocals without reverb"),
                    )
                    reverb_damping = gr.Slider(
                        0,
                        1,
                        value=user_config.get("reverb_damping"),
                        label=i18n("Damping level"),
                        info=i18n("Absorption of high frequencies in the reverb"),
                    )
            with gr.Row():
                default_button = gr.ClearButton(value=i18n("Load Defaults"))
                rvc_button = gr.Button(value=i18n("Generate"), variant="primary")

    clear_button.add([input_video, input_audio, rvc_video, rvc_audio])
    submit_button.click(
        aicover.upload_source,
        inputs=[
            original_file,
            mic_audio,
            url_text,
            youtube_quality_radio,
            youtube_format_radio,
        ],
        outputs=[input_video, input_audio, cover_files],
    )

    workspace_button.click(aicover.open_workspace_folder)
    temp_button.click(aicover.open_temp_folder)

    refresh_button.click(aicover.update_voice_models, None, outputs=rvc_voice)
    voice_model_button.click(aicover.open_model_folder)
    default_button.click(
        aicover.gradio_default_rvc,
        outputs=[
            pitch_change,
            pitch_change_all,
            index_rate,
            filter_radius,
            rms_mix_rate,
            protect,
            main_vocal_gain,
            backup_vocal_gain,
            inst_gain,
            reverb_rm_size,
            reverb_wet,
            reverb_dry,
            reverb_damping,
        ],
    )
    rvc_button.click(
        aicover.make_cover,
        inputs=[
            rvc_voice,
            pitch_change,
            pitch_change_all,
            index_rate,
            filter_radius,
            rms_mix_rate,
            protect,
            main_vocal_gain,
            backup_vocal_gain,
            inst_gain,
            reverb_rm_size,
            reverb_wet,
            reverb_dry,
            reverb_damping,
        ],
        outputs=[rvc_video, rvc_audio, cover_files],
    )
