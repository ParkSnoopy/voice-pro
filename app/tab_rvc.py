import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import gradio as gr
from src.config import UserConfig

from src.i18n.i18n import I18nAuto

i18n = I18nAuto()


from app.gradio_rvc import *


def rvc_tab(user_config: UserConfig):
    rvc = GradioRVC(user_config)
    with gr.Row():
        with gr.Column(scale=3):
            with gr.Group():
                gr.HTML(f"<center><h4>{i18n('Upload media')}</h4></center>")
                media_file = gr.File(
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
                audio_format_radio = gr.Radio(
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
                        gr.HTML(f"<center><h4>{i18n('Output Video')}</h4></center>")
                        dubbing_video = gr.Video(label=i18n("Video"), interactive=False)
                        dubbing_audio = gr.Audio(
                            label=i18n("Audio"), type="filepath", interactive=False
                        )
            dubbing_files = gr.File(
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
                gr.HTML(f"<center><h4>{i18n('RVC')}</h4></center>")
                rvc_voice = gr.Dropdown(
                    label=i18n("RVC Voice"),
                    choices=rvc.gradio_voices(),
                    value=user_config.get("rvc_voice"),
                )
                with gr.Row():
                    refresh_button = gr.Button(
                        i18n("Refresh Models 🔁"), variant="primary"
                    )
                    rvc_voice_button = gr.Button(
                        value=i18n("Open Model folder"), variant="secondary"
                    )

                rvc_f0_up_key = gr.Slider(
                    -24,
                    24,
                    value=user_config.get("rvc_f0_up_key"),
                    step=1,
                    label=i18n("Pitch"),
                    info="-24 ~ +24",
                )
                rvc_filter_radius = gr.Slider(
                    0,
                    10,
                    value=user_config.get("rvc_filter_radius"),
                    step=0.1,
                    label=i18n("Filter Radius"),
                    info="0 ~ 10, 3 이상일때, 중앙값 필터링을 적용하여 숨소리를 줄일 수 있음",
                )
                rvc_index_rate = gr.Slider(
                    0.0,
                    1.0,
                    value=user_config.get("rvc_index_rate"),
                    step=0.01,
                    label=i18n("Index Rate"),
                    info="0.0 ~ 1.0, 인덱스 파일의 영향력. 높으면 음질 저하가능성 존재함",
                )
                rvc_rms_mix_rate = gr.Slider(
                    0.0,
                    1.0,
                    value=user_config.get("rvc_rms_mix_rate"),
                    step=0.01,
                    label=i18n("RMS mix rate"),
                    info="0.0 ~ 1.0, 볼륨 인벨롭 정도",
                )
                rvc_protect = gr.Slider(
                    0,
                    0.5,
                    value=user_config.get("rvc_protect"),
                    step=0.01,
                    label=i18n("Protect"),
                    info="0.0 ~ 0.5, 값을 낮추면 보호 범위가 줄어들 수 있지만, 인덱싱 효과를 완화할 수 있음.",
                )
                rvc_hop_length = gr.Slider(
                    1,
                    512,
                    value=user_config.get("rvc_hop_length"),
                    step=1,
                    label=i18n("Hop length"),
                    info="1 ~ 512, hop 길이가 작을수록 추론 시간이 늘어나지만, 더 정확한 음높이 추정이 가능함.",
                )
                rvc_clean_strength = gr.Slider(
                    0.0,
                    1.0,
                    value=user_config.get("rvc_clean_strength"),
                    step=0.1,
                    label=i18n("Clean strength"),
                    info="0 ~ 1",
                )

            with gr.Row():
                rvc_default_button = gr.ClearButton(value=i18n("Load Defaults"))
                rvc_button = gr.Button(value=i18n("Synthesis"), variant="primary")

    submit_button.click(
        rvc.gradio_upload_source,
        inputs=[
            media_file,
            mic_audio,
            url_text,
            youtube_quality_radio,
            audio_format_radio,
        ],
        outputs=[input_video, input_audio, dubbing_files],
    )
    clear_button.add([media_file, mic_audio, url_text])

    workspace_button.click(rvc.gradio_workspace_folder)
    temp_button.click(rvc.gradio_temp_folder)

    refresh_button.click(rvc.gradio_update_voice, None, outputs=rvc_voice)
    rvc_voice_button.click(rvc.gradio_voice_folder)

    rvc_default_button.click(
        rvc.gradio_default,
        outputs=[
            rvc_f0_up_key,
            rvc_filter_radius,
            rvc_index_rate,
            rvc_rms_mix_rate,
            rvc_protect,
            rvc_hop_length,
            rvc_clean_strength,
        ],
    )

    rvc_button.click(
        rvc.gradio_rvc_dubbing,
        inputs=[
            rvc_voice,
            rvc_f0_up_key,
            rvc_filter_radius,
            rvc_index_rate,
            rvc_rms_mix_rate,
            rvc_protect,
            rvc_hop_length,
            rvc_clean_strength,
            audio_format_radio,
        ],
        outputs=[dubbing_video, dubbing_audio, dubbing_files],
    )
