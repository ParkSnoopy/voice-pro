<!-- 
    title: Voice-Pro: Ultimate AI Voice Conversion and Multilingual Translation Tool
    description: Powerful AI-powered web application for YouTube video processing, speech recognition, translation, and text-to-speech with multilingual support
    keywords: AI voice conversion, YouTube translation, subtitle generation, speech-to-text, text-to-speech, voice cloning, multilingual translation, ElevenLabs Alternative 
    author: ABUS
    version: 2.0.0
    last-updated: 2025-02-23
    product-type: AI Multimedia Processing Software
    platforms: Linux
    technology-stack: Whisper, Edge-TTS, Gradio, Faster-Whisper, Whisper-Timestamped, WhisperX, E2-TTS, F5-TTS, YouTube Downloader, Demucs, MDX-Net, RVC, CosyVoice, kokoro
    license: LGPL
-->

> [!WARNING]
> Not Tested

---

<h1 align="center">
Voice-Pro
</h1>

<p align="center">
  <i align="center">The best AI speech recognition, translation, and multilingual dubbing solution 🚀</i>
</p>

<h4 align="center">
  <a href="https://deepwiki.com/abus-aikorea/voice-pro">
    <img alt="Ask DeepWiki.com" src="https://deepwiki.com/badge.svg" style="height: 20px;">
  </a>
  <a href="https://www.youtube.com/channel/UCbCBWXuVbk-OBp9T4H5JjAA">
    <img src="https://img.shields.io/badge/youtube-d95652.svg?style=flat-square&logo=youtube" alt="youtube" style="height: 20px;">
  </a>
  <a href="https://www.buymeacoffee.com/abus">
    <img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me a Coffee" style="height: 20px;">
  </a>
  <a href="https://github.com/abus-aikorea/voice-pro/releases">
    <img src="https://img.shields.io/github/v/release/abus-aikorea/voice-pro" alt="release" style="height: 20px;">
  </a>
  <a href="https://github.com/abus-aikorea/voice-pro/stargazers">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/abus-aikorea/voice-pro">
  </a>  
</h4>

<p align="center">
    <img src="docs/images/main_page_crop.eng.jpg?raw=true" alt="Dubbing Studio"/>
</p>
<br />



## 🎙️ An AI-powered web application for speech recognition, translation, and dubbing

Voice-Pro is a state-of-the-art web app that transforms multimedia content creation. It integrates YouTube video downloading, voice separation, speech recognition, translation, and text-to-speech into a single, powerful tool for creators, researchers, and multilingual professionals.
- 🔊 Top-tier speech recognition: **Whisper**, **Faster-Whisper**, **Whisper-Timestamped**, **WhisperX**
- 🎤 Zero-shot voice cloning: **F5-TTS**, **E2-TTS**, **CosyVoice**
- 📢 Multilingual text-to-speech: **Edge-TTS**, **kokoro** (Paid version includes **Azure TTS**)
- 🎥 YouTube processing & audio extraction: **yt-dlp**
- 🌍 Instant translation for 100+ languages: **Deep-Translator** (Paid version includes **Azure Translator**)


A robust alternative to **ElevenLabs**, Voice-Pro empowers podcasters, developers, and creators with advanced voice solutions.

## ⚠️ Please Note

- Due to [WeConnect](https://www.wctokyoseoul.com) development work, Voice-Pro development and updates are not possible for the time being.
- We have made all Voice-Pro code open source and completely free. Voice-Pro can now be freely distributed and modified by anyone.
- It targets Linux Vulkan systems.
- Please leave your requests on the [![GitHub Issues](https://img.shields.io/github/issues/abus-aikorea/voice-pro)](https://github.com/abus-aikorea/voice-pro/issues)  or  [![GitHub Discussions](https://img.shields.io/github/discussions/abus-aikorea/voice-pro)](https://github.com/abus-aikorea/voice-pro/discussions) pages.
- **Troubleshooting**: In most cases, issues can be resolved by deleting the `installer` folder and then running `configure.sh` followed by `start.sh`.


## 📰 News & History

<details open>
<summary>version 3.2</summary>

- We have been focusing on [WeConnect](https://www.wctokyoseoul.com) development for the past few months and have not been able to manage Voice-Pro at all. 
- We have decided to open source all Voice-Pro code.
- Voice-Pro is completely free and supports Linux.
- [WeConnect](https://www.wctokyoseoul.com) is an application for global cultural exchange.
- Connect with people from all over the world for meaningful cultural exchanges, language learning, and international friendships.

<p align="center">
    <img src="docs/images/Hotpot 0.png?raw=true" alt="ScreenShot 0" width="18%"/>
    <img src="docs/images/Hotpot 1.png?raw=true" alt="ScreenShot 1" width="18%"/>
    <img src="docs/images/Hotpot 2.png?raw=true" alt="ScreenShot 2" width="18%"/>
    <img src="docs/images/Hotpot 3.png?raw=true" alt="ScreenShot 3" width="18%"/>
    <img src="docs/images/Hotpot 4.png?raw=true" alt="ScreenShot 4" width="18%"/>
</p>

</details>


<details>
<summary>version 3.1</summary>

- 🪄 Support for fine-tuned models of **F5-TTS**
- 🌍 Supported languages
  - <img src="https://flagcdn.com/16x12/us.png" alt="United Kingdom Flag" style="vertical-align: middle;"> English & <img src="https://flagcdn.com/16x12/cn.png" alt="China Flag" style="vertical-align: middle;"> Chinese: <a href="https://huggingface.co/SWivid/F5-TTS/tree/main/F5TTS_v1_Base"> SWivid/F5-TTS_v1 </a> 
  - <img src="https://flagcdn.com/16x12/fi.png" alt="Spain Flag" style="vertical-align: middle;"> Finnish: <a href="https://huggingface.co/AsmoKoskinen/F5-TTS_Finnish_Model"> AsmoKoskinen/F5-TTS_Finnish_Model </a> 
  - <img src="https://flagcdn.com/16x12/fr.png" alt="Spain Flag" style="vertical-align: middle;"> French: <a href="https://huggingface.co/RASPIAUDIO/F5-French-MixedSpeakers-reduced"> RASPIAUDIO/F5-French-MixedSpeakers-reduced </a> 
  - <img src="https://flagcdn.com/16x12/in.png" alt="Spain Flag" style="vertical-align: middle;"> Hindi: <a href="https://huggingface.co/SPRINGLab/F5-Hindi-24KHz"> SPRINGLab/F5-Hindi-24KHz </a>  
  - <img src="https://flagcdn.com/16x12/it.png" alt="Spain Flag" style="vertical-align: middle;"> Italian: <a href="https://huggingface.co/alien79/F5-TTS-italian"> alien79/F5-TTS-italian </a>  
  - <img src="https://flagcdn.com/16x12/jp.png" alt="Spain Flag" style="vertical-align: middle;"> Japanese: <a href="https://huggingface.co/Jmica/F5TTS/tree/main/JA_21999120"> Jmica/F5TTS/JA_21999120 </a>  
  - <img src="https://flagcdn.com/16x12/ru.png" alt="Spain Flag" style="vertical-align: middle;"> Russian: <a href="https://huggingface.co/hotstone228/F5-TTS-Russian"> hotstone228/F5-TTS-Russian </a> 
  - <img src="https://flagcdn.com/16x12/es.png" alt="Spain Flag" style="vertical-align: middle;"> Spanish: <a href="https://huggingface.co/jpgallegoar/F5-Spanish"> jpgallegoar/F5-Spanish </a> 
  
</details>

<details>
<summary>version 3.0</summary>

- 🔥 Removed the **AI Cover** feature.  
- 🚀 Added support for **m-bain/whisperX**.
  
</details>

<details>
<summary>version 2.0</summary>

- 🐍 Built with Python 3.12, Torch 2.12.1 Vulkan backend, and Gradio 5.14.0.
- 🆓 Free trial supports media up to **60 seconds** in length.  
- 🔥 Added the **AI Cover** feature.  
- 🎤 Introduced support for **CosyVoice** and **kokoro**.  
- ⏳ Initial run downloads **CozyVoice2-0.5B (9GB)**, which may take over an hour depending on network speed.  
- 🎧 Voice samples for cloning will be continuously updated.  
- 📝 Added **spaCy** for natural sentence-by-sentence translation and TTS.  
- ☁️ Subscription version includes **Microsoft Azure** Translator and TTS.  
- 🏪 Subscription offers **unlimited usage** (no 60-second limit) during the subscription period, available via [![Shopify](https://img.shields.io/badge/Shopify-7ab55c.svg?style=flat-square&logo=shopify&logoColor=white)](https://r17wvy-t2.myshopify.com).
  
</details>

## 🎥 YouTube Showcase

<table style="border-collapse: collapse; width: 100%;">
  <tr>
    <td style="padding: 10px; border: none;" align="center">
      <a href="https://youtu.be/scC5CicZ6G0" style="text-decoration: none; color: inherit;">
        <img src="https://img.youtube.com/vi/scC5CicZ6G0/hqdefault.jpg" alt="Demo Video 1" width="240" height="135" style="border-radius: 4px;">
        <br>
        <span style="font-size: 16px; font-weight: 600; color: #0f0f0f; line-height: 1.2;">Demo for Voice-Pro (v2.0)</span>
      </a>
    </td>
    <td style="padding: 10px; border: none;" align="center">
      <a href="https://youtu.be/Wfo7vQCD4no" style="text-decoration: none; color: inherit;">
        <img src="https://img.youtube.com/vi/Wfo7vQCD4no/hqdefault.jpg" alt="Demo Video 2" width="240" height="135" style="border-radius: 4px;">
        <br>
        <span style="font-size: 16px; font-weight: 600; color: #0f0f0f; line-height: 1.2;">F5-TTS: Voice Cloning</span>
      </a>
    </td>
    <td style="padding: 10px; border: none;" align="center">
      <a href="https://youtu.be/GOzCDj4MCpo" style="text-decoration: none; color: inherit;">
        <img src="https://img.youtube.com/vi/GOzCDj4MCpo/hqdefault.jpg" alt="Demo Video 3" width="240" height="135" style="border-radius: 4px;">
        <br>
        <span style="font-size: 16px; font-weight: 600; color: #0f0f0f; line-height: 1.2;">Live Transcription & Translation</span>
      </a>
    </td>
    <td style="padding: 10px; border: none;" align="center">
      <a href="https://youtu.be/YdAq80wjtuQ" style="text-decoration: none; color: inherit;">
        <img src="https://img.youtube.com/vi/YdAq80wjtuQ/hqdefault.jpg" alt="Demo Video 4" width="240" height="135" style="border-radius: 4px;">
        <br>
        <span style="font-size: 16px; font-weight: 600; color: #0f0f0f; line-height: 1.2;">Multi-Lingual Voice Cloning: Korean - German</span>
      </a>
    </td>
  </tr>
  <tr>
    <td style="padding: 10px; border: none;" align="center">
      <a href="https://youtu.be/Tu2okoHY174" style="text-decoration: none; color: inherit;">
        <img src="https://img.youtube.com/vi/Tu2okoHY174/hqdefault.jpg" alt="Demo Video 5" width="240" height="135" style="border-radius: 4px;">
        <br>
        <span style="font-size: 16px; font-weight: 600; color: #0f0f0f; line-height: 1.2;">Multi-Lingual Voice Cloning: English - Korean</span>
      </a>
    </td>
    <td style="padding: 10px; border: none;" align="center">
      <a href="https://youtu.be/dWCEwO56_7Y" style="text-decoration: none; color: inherit;">
        <img src="https://img.youtube.com/vi/dWCEwO56_7Y/hqdefault.jpg" alt="Demo Video 6" width="240" height="135" style="border-radius: 4px;">
        <br>
        <span style="font-size: 16px; font-weight: 600; color: #0f0f0f; line-height: 1.2;">Multi-Lingual Voice Cloning: Korean - Japanese</span>
      </a>
    </td>
    <td style="padding: 10px; border: none;" align="center">
      <a href="https://youtu.be/HXomwoKS3V4" style="text-decoration: none; color: inherit;">
        <img src="https://img.youtube.com/vi/HXomwoKS3V4/hqdefault.jpg" alt="Demo Video 7" width="240" height="135" style="border-radius: 4px;">
        <br>
        <span style="font-size: 16px; font-weight: 600; color: #0f0f0f; line-height: 1.2;">Video Super-Resolution</span>
      </a>
    </td>
    <td style="padding: 10px; border: none;" align="center">
      <a href="https://youtu.be/lZK7pLJBHb4" style="text-decoration: none; color: inherit;">
        <img src="https://img.youtube.com/vi/lZK7pLJBHb4/hqdefault.jpg" alt="Demo Video 8" width="240" height="135" style="border-radius: 4px;">
        <br>
        <span style="font-size: 16px; font-weight: 600; color: #0f0f0f; line-height: 1.2;">AI Karaoke</span>
      </a>
    </td>
  </tr>
  <tr>
    <td style="padding: 10px; border: none;" align="center">
      <a href="https://youtu.be/Co70lh95EsQ" style="text-decoration: none; color: inherit;">
        <img src="https://img.youtube.com/vi/Co70lh95EsQ/hqdefault.jpg" alt="Demo Video 5" width="240" height="135" style="border-radius: 4px;">
        <br>
        <span style="font-size: 16px; font-weight: 600; color: #0f0f0f; line-height: 1.2;">Multi-Lingual Voice Cloning: English - Korean</span>
      </a>
    </td>
  </tr>    
</table>


## ⭐ Key Features

### 1. Dubbing Studio
- YouTube video downloads & audio extraction
- Voice separation with **Demucs**
- Supports 100+ languages for speech recognition & translation

### 2. Speech Technologies
- **Speech-to-Text:** **Whisper**, **Faster-Whisper**, **Whisper-Timestamped**, **WhisperX**
- **Text-to-Speech:** 
  - **Edge-TTS**: 100+ languages, 400+ voices
  - **E2-TTS**, **F5-TTS**, **CosyVoice**: Zero-shot cloning
  - **kokoro**: Ranked #2 in HuggingFace TTS Arena

### 3. Real-Time Translation
- Instant speech recognition
- Multilingual translation on the fly
- Customizable audio inputs


## 🤖 WebUI

### `Dubbing Studio` Tab
- All-in-one hub: YouTube downloads, noise removal, subtitles, translation, & TTS
- Supports all ffmpeg-compatible formats
- Output options: WAV, FLAC, MP3
- Subtitles & recognition for 100+ languages
- TTS with speed, volume, & pitch controls
  
<p align="center">
  <img style="width: 90%; height: 90%" src="docs/images/main_page.eng.jpg?raw=true" alt="Multilingual Voice Conversion and Subtitle Generation Web UI Interface"/>
</p>  


### `Whisper Caption` Tab
- Subtitle-focused: 90+ languages
- Video-integrated subtitle display
- Word-level highlighting & denoise options

### `Translate` Tab
- Translation for 100+ languages
- Supports subtitle files (ASS, SSA, SRT, etc.)
- Real-time voice recognition & translation

<p align="center">
  <img style="width: 90%; height: 90%" src="docs/images/live_translation_bbc.jpg?raw=true" alt="WebUI for Real-Time Speech Recognition and Translation"/>
</p>  

### `Speech Generation` Tab
- Options: **Edge-TTS**, **F5-TTS**, **CosyVoice**, **kokoro**
- Celeb voice podcasts & multilingual support

<p align="center">
  <img style="width: 90%; height: 90%" src="docs/images/tts_f5_multi.jpg?raw=true" alt="Podcast Production WebUI Using Voice-Cloning Technology"/>
</p>  



## 🎤✨ Reference Voice

- Please request the voice you want to add on the Issues page. [Issues](https://github.com/abus-aikorea/voice-pro/issues/50)  

<details>
<summary>
English
</summary> <br />

<table>
  <tr>
    <td align="center"><img src="celebrities30sREADME/English/Andrew Bustamante.jpg" width="150"><br>Andrew Bustamante</td>
    <td align="center"><img src="celebrities30sREADME/English/Andrew Huberman.jpg" width="150"><br>Andrew Huberman</td>
    <td align="center"><img src="celebrities30sREADME/English/Avi Loeb.jpg" width="150"><br>Avi Loeb</td>
    <td align="center"><img src="celebrities30sREADME/English/Ben Shapiro.jpg" width="150"><br>Ben Shapiro</td>
    <td align="center"><img src="celebrities30sREADME/English/Brett Johnson.jpg" width="150"><br>Brett Johnson</td>
    <td align="center"><img src="celebrities30sREADME/English/Brian Keating.jpg" width="150"><br>Brian Keating</td>
  </tr>
  <tr>
    <td align="center"><img src="celebrities30sREADME/English/Coffeezilla.jpg" width="150"><br>Coffeezilla</td>
    <td align="center"><img src="celebrities30sREADME/English/Dan Carlin.jpg" width="150"><br>Dan Carlin</td>
    <td align="center"><img src="celebrities30sREADME/English/David Buss.jpg" width="150"><br>David Buss</td>
    <td align="center"><img src="celebrities30sREADME/English/David Fravor.jpg" width="150"><br>David Fravor</td>
    <td align="center"><img src="celebrities30sREADME/English/David Kipping.jpg" width="150"><br>David Kipping</td>
    <td align="center"><img src="celebrities30sREADME/English/Dennis Whyte.jpg" width="150"><br>Dennis Whyte</td>
  </tr>
  <tr>
    <td align="center"><img src="celebrities30sREADME/English/Donald Hoffman.jpg" width="150"><br>Donald Hoffman</td>
    <td align="center"><img src="celebrities30sREADME/English/Donald Trump.jpg" width="150"><br>Donald Trump</td>
    <td align="center"><img src="celebrities30sREADME/English/Douglas Murray.jpg" width="150"><br>Douglas Murray</td>
    <td align="center"><img src="celebrities30sREADME/English/Duncan Trussell.jpg" width="150"><br>Duncan Trussell</td>
    <td align="center"><img src="celebrities30sREADME/English/Elon Musk.jpg" width="150"><br>Elon Musk</td>
    <td align="center"><img src="celebrities30sREADME/English/Garry Nolan.jpg" width="150"><br>Garry Nolan</td>
  </tr>
  <tr>
    <td align="center"><img src="celebrities30sREADME/English/Jack Barsky.jpg" width="150"><br>Jack Barsky</td>
    <td align="center"><img src="celebrities30sREADME/English/James Sexton.jpg" width="150"><br>James Sexton</td>
    <td align="center"><img src="celebrities30sREADME/English/Jeff Bezos.jpg" width="150"><br>Jeff Bezos</td>
    <td align="center"><img src="celebrities30sREADME/English/Joe Rogan.jpg" width="150"><br>Joe Rogan</td>
    <td align="center"><img src="celebrities30sREADME/English/John Mearsheimer.jpg" width="150"><br>John Mearsheimer</td>
    <td align="center"><img src="celebrities30sREADME/English/Jordan Peterson.jpg" width="150"><br>Jordan Peterson</td>
  </tr>
  <tr>
    <td align="center"><img src="celebrities30sREADME/English/Kanye 'Ye' West.jpg" width="150"><br>Kanye 'Ye' West</td>
    <td align="center"><img src="celebrities30sREADME/English/Mark Zuckerberg.jpg" width="150"><br>Mark Zuckerberg</td>
    <td align="center"><img src="celebrities30sREADME/English/Michael Levin.jpg" width="150"><br>Michael Levin</td>
    <td align="center"><img src="celebrities30sREADME/English/Michael Saylor.jpg" width="150"><br>Michael Saylor</td>
    <td align="center"><img src="celebrities30sREADME/English/Michio Kaku.jpg" width="150"><br>Michio Kaku</td>
    <td align="center"><img src="celebrities30sREADME/English/MrBeast.jpg" width="150"><br>MrBeast</td>
  </tr>
  <tr>
    <td align="center"><img src="celebrities30sREADME/English/Nick Lane.jpg" width="150"><br>Nick Lane</td>
    <td align="center"><img src="celebrities30sREADME/English/Paul Rosolie.jpg" width="150"><br>Paul Rosolie</td>
    <td align="center"><img src="celebrities30sREADME/English/Ryan Graves.jpg" width="150"><br>Ryan Graves</td>
    <td align="center"><img src="celebrities30sREADME/English/Sam Altman.jpg" width="150"><br>Sam Altman</td>
    <td align="center"><img src="celebrities30sREADME/English/Sam Harris.jpg" width="150"><br>Sam Harris</td>
    <td align="center"><img src="celebrities30sREADME/English/Stephen Wolfram.jpg" width="150"><br>Stephen Wolfram</td>
  </tr>
  <tr>
    <td align="center"><img src="celebrities30sREADME/English/Tucker Carlson.jpg" width="150"><br>Tucker Carlson</td>
    <td align="center"><img src="celebrities30sREADME/English/Vitalik Buterin.jpg" width="150"><br>Vitalik Buterin</td>
    <td align="center"><img src="celebrities30sREADME/English/Yuval Harari.jpg" width="150"><br>Yuval Harari</td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
</table>
</details>


<details>
<summary>
Chinese
</summary> <br />

<table>
  <tr>
    <td align="center"><img src="celebrities30sREADME/Chinese/Dilraba Dilmurat.jpg" width="150"><br>迪丽热巴 (Dílì Rèbā)</td>
    <td align="center"><img src="celebrities30sREADME/Chinese/Jolin Tsai.jpg" width="150"><br>蔡依林 (Cài Yīlín)</td>
    <td align="center"><img src="celebrities30sREADME/Chinese/Kris Wu.jpg" width="150"><br>吴亦凡 (Wú Yìfán)</td>
    <td align="center"><img src="celebrities30sREADME/Chinese/Li Yifeng.jpg" width="150"><br>李易峰 (Lǐ Yìfēng)</td>
    <td align="center"><img src="celebrities30sREADME/Chinese/Yang Mi.jpg" width="150"><br>杨幂 (Yáng Mì)</td>
    <td align="center"><img src="celebrities30sREADME/Chinese/Zhao Liying.jpg" width="150"><br>赵丽颖 (Zhào Lìyǐng)</td>
  </tr>
</table>
</details>


<details>
<summary>
Korean
</summary> <br />

<table>
  <tr>
    <td align="center"><img src="celebrities30sREADME/Korean/BTS Jin.jpg" width="150"><br>BTS 진 (Jin)</td>
    <td align="center"><img src="celebrities30sREADME/Korean/BTS RM.jpg" width="150"><br>BTS RM</td>
    <td align="center"><img src="celebrities30sREADME/Korean/IU.jpg" width="150"><br>IU (아이유)</td>
    <td align="center"><img src="celebrities30sREADME/Korean/LeeByungHun.jpg" width="150"><br>이병헌</td>
    <td align="center"><img src="celebrities30sREADME/Korean/LeeJungJae.jpg" width="150"><br>이정재</td>
    <td align="center"><img src="celebrities30sREADME/Korean/YouJaeSuk.jpg" width="150"><br>유재석</td>
  </tr>
</table>
</details>


<details>
<summary>
Japanese
</summary> <br />

<table>
  <tr>
    <td align="center"><img src="celebrities30sREADME/Japanese/Ayase Haruka.jpg" width="150"><br>綾瀬はるか (Ayase Haruka)</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
</table>
</details>
<br />


## 💻 System Requirements
- **OS:** Linux (64-bit)
- **CPU:** x86_64 processor; more cores help
- **RAM:** 8GB+ recommended
- **Storage:** 20GB+ free space
- **Internet:** Required
- **uv:** Install first — `curl -LsSf https://astral.sh/uv/install.sh | sh`



## 📀 Installation

Install Voice-Pro with ease using **configure.sh** and **start.sh**.


### 1. Get the Package

  + Clone or download the latest release (**Source code (zip)**) from  [![GitHub Release](https://img.shields.io/github/v/release/abus-aikorea/voice-pro)](https://github.com/abus-aikorea/voice-pro/)
```bash
git clone https://github.com/abus-aikorea/voice-pro.git
```
  

### 2. Install & Run
1. 🚀 **configure.sh**
   - Sets up git, ffmpeg, and build essentials for the Vulkan install
   - Run once; takes 1+ hour with internet
   - Don't close the terminal
2. 🚀 **start.sh**
   - Launches Voice-Pro WebUI
   - First run syncs the `pyproject.toml` / `uv.lock` project dependencies (1+ hour)
   - Optional WebUI bind settings go in `app/config-user.json5`:
     - `"gradio_host": "0.0.0.0"`
     - `"gradio_port": 7860`
   - Retry after deleting **installer** if issues arise

### 3. Update
- 🚀 **update.sh**: Refreshes Python environment (faster than reinstall)

### 4. Uninstall
- Run **uninstall.sh** or delete the folder (portable install)


## 📁 Folders & Files Written

Voice-Pro is fully portable: **all** runtime writes stay under the project directory. Nothing is written to `~/.cache/`, `~/.local/`, `~/.config/`, `~/stanza_resources/`, or `/tmp/`. `start.sh`, `update.sh`, and `one_click.py` redirect cache/temp dirs with Linux env vars including `HOME`, `TMPDIR`, `XDG_*`, `GRADIO_TEMP_DIR`, `HF_*`, `MODELSCOPE_CACHE`, `UV_*`, `MPLCONFIGDIR`, `TORCH_*`, `NUMBA_CACHE_DIR`, `TRITON_CACHE_DIR`, and `CACHED_PATH_CACHE_DIR`.

### Inside the project directory
| Path | Purpose |
|---|---|
| `installer/env/` | Python venv (uv-managed). ~3GB. |
| `installer/home/` | Process-local `HOME` for libraries that hard-code `~`. |
| `installer/gradio/` | Gradio upload temp (`GRADIO_TEMP_DIR`). |
| `installer/tmp/` | Python `tempfile` / `TMPDIR`. |
| `installer/uv-cache/` | uv project/package download cache (`UV_CACHE_DIR` / `PIP_CACHE_DIR`). |
| `installer/uv-python/` | uv-managed Python downloads (`UV_PYTHON_INSTALL_DIR`) if system Python 3.12 is missing. |
| `installer/yt-dlp-cache/` | yt-dlp extractor cache (`cachedir`). |
| `installer/matplotlib/` | matplotlib font/config cache (`MPLCONFIGDIR`). |
| `installer/xdg-cache/` | Linux default cache redirect (`XDG_CACHE_HOME`) for libraries using platformdirs/appdirs. |
| `installer/xdg-config/` | Linux default config redirect (`XDG_CONFIG_HOME`). |
| `installer/xdg-data/` | Linux default data redirect (`XDG_DATA_HOME`). |
| `installer/xdg-state/` | Linux default state redirect (`XDG_STATE_HOME`). |
| `installer/numba-cache/` | numba compilation cache (`NUMBA_CACHE_DIR`). |
| `model/` | Downloaded ML models: Whisper, Demucs, MDX-Net, RVC, F5-TTS, CosyVoice, Kokoro, Edge-TTS, VAD, Vocos. ~15GB. |
| `model/stanza/` | Stanza NLP models (`STANZA_RESOURCES_DIR`). |
| `model/.hf_cache/` | HuggingFace hub/cache (`HF_HOME`, `HF_HUB_CACHE`, `HUGGINGFACE_HUB_CACHE`). |
| `model/.modelscope_cache/` | ModelScope cache (`MODELSCOPE_CACHE`) — CosyVoice. |
| `model/.torch/` | torch.hub checkpoint cache (`TORCH_HOME`) — demucs remote fallback. |
| `model/.torch_extensions/` | torch JIT extension build dir (`TORCH_EXTENSIONS_DIR`). |
| `model/.cached_path/` | cached-path library cache (`CACHED_PATH_CACHE_DIR`) — F5-TTS fallback. |
| `model/.triton/` | Triton kernel cache (`TRITON_CACHE_DIR`). |
| `workspace/` | User output: `youtube/`, `live/`, `translate/`, `dubbing/`, `demucs/` subfolders. |
| `app/config-user.json5` | User settings (gitignored). |
| `.env` | Azure credentials — user-created from `.env.example` (gitignored). |

### Outside the project directory
None. `configure.sh` installs system packages (git, ffmpeg, build-essential) via apt/yum/dnf/pacman — those go to system paths, but only when you explicitly run `configure.sh`.

### Uninstall
Delete the project folder to remove all runtime data. `uninstall.sh` removes `installer/` and can optionally remove system packages, but it intentionally leaves `model/`, `workspace/`, `.env`, and the project folder for manual deletion.


## ❓Tips & Tricks

#### If Browser does not run automatically
- Close the terminal and run start.sh again.
- Run the browser directly and enter the address displayed in the terminal (e.g. **http://127.0.0.1:7870**) in the address bar.

#### If memory usage is high
- Check system memory and close other heavy apps if needed.
- Set the Denoise level to 0 or 1. Denoise level 2 uses more RAM and is slower.
- Set Compute Type to int type. The float type has better quality, but uses more memory.

#### How to improve the quality of subtitles?
- The quality of subtitles tends to improve with larger Whisper models, but this is not necessarily the case. large > medium > small > base > tiny 
- Among compute types, float type can give better quality. The int type reduces memory usage and can run faster on smaller machines.
- If you increase the denoise level, more background sounds will be removed, and only the remaining voice will be used for voice recognition. It does not always guarantee good results.
  


## 🚨 Notice
- Due to [WeConnect](https://www.wctokyoseoul.com) development work, there will be no Voice-Pro updates for the time being.
- All Voice-Pro code has been made open source. It is now completely free to use.
- [WeConnect](https://www.wctokyoseoul.com) is a communication platform for global cultural exchange.



<br />


## ⏳ SaaS Platforms for Subtitling, Translation, and TTS

The following table lists SaaS platforms supporting subtitling, translation, and text-to-speech (TTS/dubbing) functionalities. Costs are calculated for processing a 60-minute Korean video, including subtitle generation, English translation, and English dubbing, based on the latest available pricing data as of April 15, 2025.

| Platform        | Subtitling | Translation | TTS/Dubbing | Cost for 60-min Video (USD, Approx.) | Key Features                                                                 |
|-----------------|------------|-------------|-------------|-------------------------------------|------------------------------------------------------------------------------|
| **[Maestra](https://maestra.ai)**     | ✅         | ✅          | ✅          | $23.70                              | 125+ languages, real-time captions, SEO keyword extraction, 15-min free trial. |
| **[Kapwing](https://www.kapwing.com)**     | ✅         | ✅          | ✅          | $30~$40 (Pro plan, per minute)     | AI subtitles, 100+ language translations, auto lip-sync dubbing, free tier.   |
| **[VEED.IO](https://www.veed.io)**     | ✅         | ✅          | ❌          | $24~$36 (Pro plan, partial)        | 99.9% accurate subtitles, Instagram-optimized captions, intuitive editor.     |
| **[HappyScribe](https://happyscribe.com)** | ✅         | ✅          | ✅          | $36~$48 (Pay-as-you-go)            | 120+ languages, professional proofreading, secure, meeting transcription.     |
| **[Sonix](https://sonix.ai)**       | ✅         | ✅          | ✅          | $30~$40 (Standard plan)            | 54+ languages, 30-min free transcription, YouTube/Zoom integration.           |
| **[Descript](https://descript.com)**    | ✅         | ✅          | ✅          | $36~$48 (Creator plan)             | Text-based editing, Overdub TTS, filler word removal, 1-hour free transcription. |
| **[AppTek](https://apptek.ai)**      | ✅         | ✅          | ✅          | Custom pricing (Contact)            | Media-focused, custom models, metadata generation, cloud-based Workbench.     |
| **[Transkriptor](https://transkriptor.com)**| ✅         | ✅          | ❌          | $12~$18 (Pay-as-you-go)            | 100+ languages, YouTube link transcription, 99% accuracy, simple editor.      |

### Cost Calculation Details
- **[Maestra](https://maestra.ai/)**: Premium Plan ($158/month, 1200 credits). 60-min video: 60 credits (subtitles) + 60 credits (translation) + 60 credits (dubbing) = 180 credits. Cost = (180/1200) * $158 = $23.70.[](https://maestra.ai/pricing)
- **[Kapwing](https://www.kapwing.com)**: Pro plan (\~$24/month, limited minutes). Estimated $0.50\~$0.67/min for subtitles+translation+dubbing (based on per-minute pricing trends). 60-min cost: $30\~$40. Exact pricing requires confirmation.
- **[VEED.IO](https://www.veed.io)**: Pro plan (\~$24/month). Subtitles+translation estimated at $0.40\~$0.60/min. No TTS, so partial processing. 60-min cost: $24\~$36. Confirm at [veed.io](https://veed.io).
- **[HappyScribe](https://happyscribe.com)**: Pay-as-you-go (\~$0.20/min transcription, $0.20/min translation, $0.20/min dubbing). 60-min cost: $36\~$48 (assuming combined services). Confirm at [happyscribe.com](https://happyscribe.com).
- **[Sonix](https://sonix.ai)**: Standard plan (\~$10/hour transcription, additional for translation/dubbing). Estimated $0.50\~$0.67/min total. 60-min cost: $30\~$40. Confirm at [sonix.ai](https://sonix.ai).
- **[Descript](https://descript.com)**: Creator plan (\~$24/month, limited hours). Estimated $0.60\~$0.80/min for subtitles+translation+dubbing. 60-min cost: $36\~$48. Confirm at [descript.com](https://descript.com).
- **[AppTek](https://apptek.ai)**: Custom pricing for enterprise. No public per-minute rates. Contact [apptek.ai](https://apptek.ai) for quotes.
- **[Transkriptor](https://transkriptor.com)**: Pay-as-you-go ($0.05\~$0.10/min transcription, similar for translation). No TTS, so partial processing. 60-min cost: $12\~$18. Confirm at [transkriptor.com](https://transkriptor.com).

### Notes
- **Cost for 60-min Video**: Costs are approximate and assume processing a 60-minute Korean video for subtitles, English translation, and English dubbing (where available). Platforms without TTS (e.g., VEED.IO, Transkriptor) reflect partial processing costs.
- **Language Support**: Most platforms support Korean and English. Verify specific language availability on their websites.
- **Use Cases**:
  - Media/Entertainment: AppTek, Maestra
  - Social Media: Kapwing, VEED.IO
  - Podcasts/Interviews: Sonix, Descript
  - E-learning/Global Content: Transkriptor, HappyScribe
- **Pricing Updates**: Pricing may vary due to plan changes or promotions. Check official websites for the latest details.
- For contributions or specific use case recommendations, open an issue or submit a pull request in this repository!

<br />

## ☕ Contributions

Hello, I'm David from the Voice-Pro team.
Our team discovers the best AI technologies in the industry and provides them for anyone to use easily and conveniently.
We are a small startup in Korea that has only been around for a year. We are working hard to help you and other creators produce great content.

Your ⭐⭐⭐⭐⭐ review would be greatly appreciated as it helps our business grow with you. Please help support our small team.

Thank you,
ABUS Customer Service

- If you want to participate in and help us with this project, feel free to create an [Issues](https://github.com/abus-aikorea/voice-pro/issues) 
- If something goes wrong, please submit a [Pull requests](https://github.com/abus-aikorea/voice-pro/pulls) to improve this project.
- Any type of contribution is welcome.
- For inquiries related to purchases, business partnerships, technical tuning, investments, and other matters, please contact us by email. (<abus.aikorea@gmail.com>)."
- If you like this project, please star this repository. We would greatly appreciate it. ⭐⭐⭐
- You can support Voice-Pro with a donation here:    
</a>
  <a href="https://www.buymeacoffee.com/abus">
  <img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me a Coffee" style="height: 20px;">
</a>



## 📬 Contact
- Email: <abus.aikorea@gmail.com>
- Homepage (Korean): <https://www.wctokyoseoul.com>
- Paid Version Purchase: [Shopify (Global)](https://r17wvy-t2.myshopify.com), [Naver (Korean)](https://smartstore.naver.com/abus)

## 🙏 Credits
* Demucs: <https://github.com/facebookresearch/demucs>
* yt-dlp: <https://github.com/yt-dlp/yt-dlp>
* gradio: <https://github.com/gradio-app/gradio>
* edge-TTS: <https://github.com/rany2/edge-tts>
* F5-TTS: <https://github.com/SWivid/F5-TTS.git>
* openai-whisper: <https://github.com/openai/whisper>
* faster-whisper: <https://github.com/SYSTRAN/faster-whisper>
* whisper-timestamped: <https://github.com/linto-ai/whisper-timestamped>
* whisperX: <https://github.com/m-bain/whisperX>
* CosyVoice: <https://github.com/FunAudioLLM/CosyVoice>
* kokoro: <https://github.com/hexgrad/kokoro>
* Deep-Translator: <https://github.com/nidhaloff/deep-translator>
* spaCy: <https://github.com/explosion/spaCy>



## ©️ Copyright
  <img src="docs/images/ABUS-logo.jpg" width="100" height="100"> by [ABUS](https://www.wctokyoseoul.com)

