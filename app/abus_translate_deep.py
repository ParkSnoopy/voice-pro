import gradio as gr
import pysubs2
from deep_translator import GoogleTranslator

from app.abus_genuine import *
from app.abus_path import *
from app.abus_text import *
from app.abus_nlp_spacy import *

import structlog

logger = structlog.get_logger()


class DeepTranslator:
    def __init__(self) -> None:
        self.translator = GoogleTranslator(source="auto", target="en")
        self.languages_dict = GoogleTranslator().get_supported_languages(as_dict=True)

    def get_languages(self) -> list:
        capitalized_keys = [key.capitalize() for key in self.languages_dict.keys()]
        return capitalized_keys

    def get_language_code(self, language_name) -> str:
        search_name = language_name.lower()
        for key, value in self.languages_dict.items():
            if key.lower() == search_name:
                return value
        return "en"

    def get_language_value(self, language_name):
        search_name = language_name.lower()
        for key, value in self.languages_dict.items():
            if key.lower() == search_name:
                return key
        return None

    def translate_text(
        self, source_lang: str, target_lang: str, text: str, progress=gr.Progress()
    ) -> str:
        source_code = self.get_language_code(source_lang)
        target_code = self.get_language_code(target_lang)

        self.translator.source = source_code
        self.translator.target = target_code

        # line 끝 마침표 확인인
        use_punctuation = AbusText.has_ending_marks([text])

        # 텍스트를 문장 단위로 분리
        sentences = AbusText.split_into_sentences(text, use_punctuation)
        sentences = sentences

        translated_sentences = []

        # 각 문장을 번역
        for sentence in progress.tqdm(sentences, desc="Translating sentences..."):
            try:
                translated = self.translator.translate(text=sentence)
                translated_sentences.append(translated)
                logger.debug(
                    f"[abus_translate_deep.py] translate_text - {source_code}: {sentence} -> {target_code}: {translated}"
                )
            except Exception as e:
                logger.error(f"Translation error: {e}")
                translated_sentences.append(sentence)  # 에러 발생 시 원본 문장 사용

        # 번역된 문장들을 다시 하나의 텍스트로 결합
        final_text = " ".join(translated_sentences)
        return final_text

    def translate_file(
        self,
        source_lang: str,
        target_lang: str,
        subtitle_file_path: str,
        output_file_path: str,
        progress=gr.Progress(),
    ):
        tts_source_file = path_add_postfix(
            subtitle_file_path, f"-{source_lang}", ".srt"
        )

        # AbusText.process_subtitle_for_tts(subtitle_file_path, tts_source_file)
        AbusSpacy.process_subtitle_for_tts(subtitle_file_path, tts_source_file)

        source_code = self.get_language_code(source_lang)
        target_code = self.get_language_code(target_lang)

        translator = GoogleTranslator(source=source_code, target=target_code)
        logger.debug(
            f"[abus_translate_deep.py] translate_file {source_code}: {subtitle_file_path} -> {target_code}: {output_file_path}"
        )

        # Load subtitles using pysubs2
        full_subs = pysubs2.load(tts_source_file)
        subs = full_subs

        # 구두점이 없는 언어의 경우 각 자막을 개별적으로 번역
        for event in progress.tqdm(subs, desc="Translate..."):
            if not event.text:
                continue

            text = event.plaintext
            try:
                translated_text = translator.translate(text)
                if translated_text:
                    event.text = translated_text
                    logger.debug(
                        f"[abus_translate_deep.py] translate_file : text       - {text}"
                    )
                    logger.debug(
                        f"[abus_translate_deep.py] translate_file : translated - {translated_text}"
                    )
                else:
                    logger.warning(
                        f"[abus_translate_deep.py] translate_file - Empty translation for: {text}"
                    )
            except Exception as e:
                logger.error(f"Translation error for text '{text}': {e}")
                # 에러 발생 시 원본 텍스트 유지

        # Save the translated subtitles
        subs.save(output_file_path)
        cmd_delete_file(tts_source_file)
