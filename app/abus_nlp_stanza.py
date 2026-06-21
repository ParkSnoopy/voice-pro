import re
import pysubs2
import stanza
import logging
from typing import List, Optional
from lingua import LanguageDetectorBuilder

# Stanza 로깅 설정
stanza_logger = logging.getLogger("stanza")
stanza_logger.setLevel(logging.ERROR)
if stanza_logger.hasHandlers():
    stanza_logger.handlers.clear()
stanza_logger.addHandler(logging.StreamHandler())


class AbusStanza:
    MAX_MERGE_GAP_MS = 1000  # 2000ms -> 1000ms로 줄임
    SENTENCE_BREAK_MS = 1500
    MAX_SENTENCE_LENGTH = 200  # 300 -> 200으로 조정
    FULL_TO_HALF_MAP = {
        "．": ".",
        "！": "!",
        "？": "?",
        "，": ",",
        "：": ":",
        "；": ";",
        "（": "(",
        "）": ")",
        "［": "[",
        "］": "]",
        "｛": "{",
        "｝": "}",
        "　": " ",
        "＠": "@",
        "＃": "#",
        "＄": "$",
        "％": "%",
        "＆": "&",
    }
    SUPPORTED_LANGUAGES = {
        "ca": "ca",
        "zh": "zh-hans",
        "hr": "hr",
        "da": "da",
        "nl": "nl",
        "en": "en",
        "fi": "fi",
        "fr": "fr",
        "de": "de",
        "el": "el",
        "it": "it",
        "ja": "ja",
        "ko": "ko",
        "lt": "lt",
        "nb": "nb",
        "pl": "pl",
        "pt": "pt",
        "ro": "ro",
        "ru": "ru",
        "es": "es",
        "sv": "sv",
        "uk": "uk",
    }
    SPACE_USAGE = {"ja": False, "zh": False, "th": False}
    _nlp_models = {}
    detector = LanguageDetectorBuilder.from_all_languages().build()

    @classmethod
    def get_nlp(cls, lang: str) -> stanza.Pipeline:
        if lang not in cls._nlp_models:
            model_lang = cls.SUPPORTED_LANGUAGES.get(lang, "en")
            print(f"Initializing Stanza pipeline for {model_lang}")
            cls._nlp_models[lang] = stanza.Pipeline(
                lang=model_lang,
                processors="tokenize,mwt",
                tokenize_no_ssplit=False,
                download_method=stanza.DownloadMethod.REUSE_RESOURCES,
            )
        return cls._nlp_models[lang]

    @classmethod
    def detect_language(cls, text: str) -> str:
        try:
            detected_lang = cls.detector.detect_language_of(text)
            return detected_lang.iso_code_639_1.name.lower()
        except Exception as e:
            print(f"Language detection error: {e}")
            return "en"

    @classmethod
    def normalize_text(cls, text: str) -> str:
        for full, half in cls.FULL_TO_HALF_MAP.items():
            text = text.replace(full, half)
        text = re.sub(r'["""]', '"', text)
        text = re.sub(r"[''']", "'", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    @classmethod
    def split_into_sentences(cls, text: str, lang: str) -> List[str]:
        if not text:
            return []
        try:
            nlp = cls.get_nlp(lang)
            doc = nlp(text)
            sentences = [
                sent.text.strip() for sent in doc.sentences if sent.text.strip()
            ]
            if not sentences:
                return [text]
            # 연속된 짧은 문장을 병합하지 않고, Stanza 결과에 의존
            return sentences
        except Exception as e:
            print(f"Sentence splitting error: {e}")
            return cls._fallback_sentence_split(text, lang)

    @classmethod
    def _fallback_sentence_split(cls, text: str, lang: str) -> List[str]:
        end_marks = {
            "en": [". ", "! ", "? ", ".\n", "!\n", "?\n"],
            "ja": ["。", "！", "？", "…"],
            "zh": ["。", "！", "？", "…"],
            "ko": [". ", "! ", "? ", ".\n", "!\n", "?\n", "다. ", "요. ", "니다. "],
        }
        default_marks = [". ", "! ", "? ", ".\n", "!\n", "?\n"]
        separators = end_marks.get(lang, default_marks)
        segments = [text]
        for sep in separators:
            new_segments = []
            for segment in segments:
                if sep in segment:
                    parts = segment.split(sep)
                    for i in range(len(parts) - 1):
                        new_segments.append(parts[i] + sep.rstrip())
                    if parts[-1]:
                        new_segments.append(parts[-1])
                else:
                    new_segments.append(segment)
            segments = new_segments
        return [segment.strip() for segment in segments if segment.strip()]

    @classmethod
    def merge_and_split_events(
        cls, subs, lang: Optional[str] = None
    ) -> List[pysubs2.SSAEvent]:
        final_events = []
        for event in subs:
            text = event.plaintext.strip()
            if not text:
                continue
            text = cls.normalize_text(text)
            detected_lang = lang or cls.detect_language(text)
            sentences = cls.split_into_sentences(text, detected_lang)
            if not sentences:
                sentences = [text]
            total_length = sum(len(s) for s in sentences)
            current_time = event.start
            for j, sentence in enumerate(sentences):
                if total_length > 0:
                    duration = int(
                        (len(sentence) / total_length) * (event.end - event.start)
                    )
                else:
                    duration = (event.end - event.start) // max(1, len(sentences))
                if j == len(sentences) - 1:
                    event_end = event.end
                else:
                    event_end = current_time + max(duration, 500)
                new_event = pysubs2.SSAEvent(
                    start=current_time, end=event_end, text=sentence
                )
                new_event.meta = {"lang": detected_lang}
                final_events.append(new_event)
                current_time = event_end

        merged_events = []
        current_event = None
        for event in final_events:
            if not current_event:
                current_event = event
            else:
                gap = event.start - current_event.end
                current_text = current_event.text.rstrip()
                next_text = event.text
                curr_lang = current_event.meta.get("lang") or cls.detect_language(
                    current_text
                )
                next_lang = event.meta.get("lang") or cls.detect_language(next_text)
                if curr_lang != next_lang:
                    merged_events.append(current_event)
                    current_event = event
                    continue
                nlp = cls.get_nlp(curr_lang)
                current_complete = cls._is_complete_sentence(current_text, nlp)
                should_merge = (
                    gap < cls.MAX_MERGE_GAP_MS
                    and not current_complete  # 완전한 문장은 병합하지 않음
                    and len(current_text + " " + next_text) <= cls.MAX_SENTENCE_LENGTH
                )
                print(
                    f"Merging check: gap={gap}, complete={current_complete}, length={len(current_text + ' ' + next_text)}"
                )  # 디버깅
                if should_merge:
                    uses_spaces = not cls.SPACE_USAGE.get(curr_lang, False)
                    if uses_spaces:
                        current_event.text = current_text + " " + next_text.lstrip()
                    else:
                        current_event.text += next_text
                    current_event.end = event.end
                    print(f"Merged: {current_event.text}")
                else:
                    merged_events.append(current_event)
                    current_event = event
        if current_event:
            merged_events.append(current_event)

        for i, event in enumerate(merged_events):
            text = event.text.rstrip()
            lang = event.meta.get("lang") or cls.detect_language(text)
            nlp = cls.get_nlp(lang)
            is_complete = cls._is_complete_sentence(text, nlp)
            if not is_complete and (
                i == len(merged_events) - 1
                or merged_events[i + 1].start - event.end > cls.SENTENCE_BREAK_MS
            ):
                event.text = cls._complete_sentence(text, lang, nlp)
        return merged_events

    @classmethod
    def _is_complete_sentence(cls, text: str, nlp: stanza.Pipeline) -> bool:
        if not text:
            return False
        if any(text.endswith(mark) for mark in [".", "!", "?", "。", "！", "？", "…"]):
            return True
        try:
            if "pos" not in nlp.processors:
                nlp = stanza.Pipeline(lang=nlp.lang, processors="tokenize,pos,mwt")
            doc = nlp(text)
            has_subject = False
            has_verb = False
            for sent in doc.sentences:
                for word in sent.words:
                    if word.upos in ("NOUN", "PRON"):
                        has_subject = True
                    if word.upos == "VERB":
                        has_verb = True
            if nlp.lang in ("ja", "ko", "zh"):
                return has_verb
            return has_subject and has_verb
        except Exception as e:
            print(f"Sentence completeness check error: {e}")
            return False

    @classmethod
    def _complete_sentence(cls, text: str, lang: str, nlp: stanza.Pipeline) -> str:
        text = text.rstrip()
        if any(text.endswith(mark) for mark in [".", "!", "?", "。", "！", "？", "…"]):
            return text
        try:
            doc = nlp(text)
            is_question = False
            if lang in ("en", "es", "fr", "de", "it", "pt"):
                wh_words = ["what", "who", "where", "when", "why", "how", "which"]
                first_word = text.lower().split()[0] if text else ""
                if first_word in wh_words:
                    is_question = True
            elif lang == "ja":
                if any(text.endswith(q) for q in ["か", "の"]):
                    is_question = True
            elif lang == "ko":
                if any(text.endswith(q) for q in ["까", "니", "가요", "나요"]):
                    is_question = True
            elif lang == "zh":
                if text.endswith("吗") or text.endswith("呢"):
                    is_question = True
            if is_question:
                ending_map = {"ja": "？", "zh": "？", "ko": "?"}
                return text + ending_map.get(lang, "?")
            else:
                ending_map = {"ja": "。", "zh": "。", "ko": "."}
                return text + ending_map.get(lang, ".")
        except Exception as e:
            print(f"Sentence completion error: {e}")
            return text + "."

    @classmethod
    def process_subtitle_for_tts(cls, subtitle_file, output_file):
        subs = pysubs2.load(subtitle_file, encoding="utf-8")
        processed_events = cls.merge_and_split_events(subs)
        new_subs = pysubs2.SSAFile()
        new_subs.events = processed_events
        new_subs.save(output_file)
