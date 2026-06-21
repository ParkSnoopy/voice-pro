import re
import pysubs2
import spacy
from spacy.cli.download import download
from typing import List, Optional
from lingua import LanguageDetectorBuilder


class AbusSpacy:
    MAX_MERGE_GAP_MS = 1000
    SENTENCE_ENDINGS = {".", "!", "?", "。", "！", "？", "…"}
    NON_SPACING_LANGUAGES = {"ja", "zh", "th", "km", "lo"}
    MIN_DURATION_MS = 1000

    _nlp_models = {}
    detector = LanguageDetectorBuilder.from_all_languages().build()

    SUPPORTED_LANGUAGES = {
        "en": {"sm": "en_core_web_sm", "md": "en_core_web_md", "lg": "en_core_web_lg"},
        "zh": {"sm": "zh_core_web_sm", "md": "zh_core_web_md", "lg": "zh_core_web_lg"},
        "ja": {
            "sm": "ja_core_news_sm",
            "md": "ja_core_news_md",
            "lg": "ja_core_news_lg",
        },
        "ko": {
            "sm": "ko_core_news_sm",
            "md": "ko_core_news_md",
            "lg": "ko_core_news_lg",
        },
        "fr": {
            "sm": "fr_core_news_sm",
            "md": "fr_core_news_md",
            "lg": "fr_core_news_lg",
        },
        "de": {
            "sm": "de_core_news_sm",
            "md": "de_core_news_md",
            "lg": "de_core_news_lg",
        },
        "es": {
            "sm": "es_core_news_sm",
            "md": "es_core_news_md",
            "lg": "es_core_news_lg",
        },
        "it": {
            "sm": "it_core_news_sm",
            "md": "it_core_news_md",
            "lg": "it_core_news_lg",
        },
        "ru": {
            "sm": "ru_core_news_sm",
            "md": "ru_core_news_md",
            "lg": "ru_core_news_lg",
        },
    }

    @classmethod
    def get_nlp(cls, lang: str, model_size: str = "sm") -> spacy.language.Language:
        if model_size not in ["sm", "md", "lg"]:
            raise ValueError("model_size must be one of 'sm', 'md', or 'lg'")

        key = (lang, model_size)
        if key not in cls._nlp_models:
            model_dict = cls.SUPPORTED_LANGUAGES.get(
                lang, cls.SUPPORTED_LANGUAGES["en"]
            )
            model_name = model_dict.get(model_size, model_dict["sm"])
            try:
                cls._nlp_models[key] = spacy.load(model_name, disable=["tagger", "ner"])
            except OSError:
                download(model_name)
                cls._nlp_models[key] = spacy.load(model_name, disable=["tagger", "ner"])
            cls._nlp_models[key].add_pipe("sentencizer", first=True)
        return cls._nlp_models[key]

    @classmethod
    def detect_language(cls, text: str) -> str:
        if not text.strip():
            return "en"
        detected = cls.detector.detect_language_of(text)
        return detected.iso_code_639_1.name.lower() if detected else "en"

    @classmethod
    def normalize_text(cls, text: str, lang: str) -> str:
        # 특수 문자를 일반 구두점으로 변환
        text = text.translate(
            str.maketrans(
                {
                    "．": ".",
                    "！": "!",
                    "？": "?",
                    "，": ",",
                    "：": ":",
                    "；": ";",
                    "　": " ",
                }
            )
        )
        # 연속된 공백을 단일 공백으로 변환
        text = re.sub(r"\s+", " ", text).strip()
        return text

    @classmethod
    def split_into_sentences(
        cls, text: str, lang: str, model_size: str = "sm"
    ) -> List[str]:
        if len(text) < 10:
            return [text]
        try:
            nlp = cls.get_nlp(lang, model_size)
            doc = nlp(text)
            sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
            return sentences if sentences else [text]
        except Exception:
            return re.split(r"(?<=[.!?。！？])\s+", text.strip())

    @classmethod
    def is_complete_sentence(cls, text: str, lang: str) -> bool:
        if not text or len(text) < 3:
            return False
        return text[-1] in cls.SENTENCE_ENDINGS or len(text) > 20

    @classmethod
    def complete_sentence(cls, text: str, lang: str) -> str:
        text = text.rstrip()
        if text[-1] in cls.SENTENCE_ENDINGS:
            return text
        return text + (
            "?" if re.search(r"^(who|what|when|where|why|how)", text, re.I) else "."
        )

    @classmethod
    def merge_and_split_events(
        cls, subs, lang: Optional[str] = None, model_size: str = "sm"
    ) -> List[pysubs2.SSAEvent]:
        if not subs:
            return []
        lang = lang or cls.detect_language(
            next((e.plaintext for e in subs if e.plaintext.strip()), "")
        )

        events = []
        current_group = []
        for event in subs:
            text = cls.normalize_text(event.plaintext, lang)
            if not text:
                continue
            if (
                current_group
                and event.start - current_group[-1].end > cls.MAX_MERGE_GAP_MS
            ):
                events.extend(cls._process_group(current_group, lang, model_size))
                current_group = []
            current_group.append(event)

        if current_group:
            events.extend(cls._process_group(current_group, lang, model_size))
        return events

    @classmethod
    def _process_group(
        cls, events: List[pysubs2.SSAEvent], lang: str, model_size: str
    ) -> List[pysubs2.SSAEvent]:
        if not events:
            return []
        full_text = " ".join(
            cls.normalize_text(e.plaintext, lang) for e in events if e.plaintext.strip()
        )
        sentences = cls.split_into_sentences(full_text, lang, model_size)

        merged_sentences = []
        current = ""
        for sent in sentences:
            if current and not cls.is_complete_sentence(current, lang):
                current += " " + sent
            else:
                if current:
                    merged_sentences.append(current)
                current = sent
        if current:
            merged_sentences.append(current)

        event_starts = [e.start for e in events if e.plaintext.strip()]
        event_ends = [e.end for e in events if e.plaintext.strip()]
        total_duration = event_ends[-1] - event_starts[0]
        total_chars = len(full_text)

        result = []
        last_end = event_starts[0]

        for sent_idx, sent in enumerate(merged_sentences):
            if not cls.is_complete_sentence(sent, lang):
                sent = cls.complete_sentence(sent, lang)

            sent_start = last_end if sent_idx > 0 else event_starts[0]
            sent_duration = max(
                cls.MIN_DURATION_MS, int(total_duration * len(sent) / total_chars)
            )
            sent_end = sent_start + sent_duration

            for i, (e_start, e_end) in enumerate(zip(event_starts, event_ends)):
                if sent_start >= e_start and sent_start < e_end:
                    sent_end = min(sent_end, event_ends[-1])
                    break
                elif sent_start < e_start and i > 0:
                    sent_start = e_start
                    sent_end = sent_start + sent_duration
                    break

            sent_end = min(sent_end, event_ends[-1])
            if sent_end - sent_start < cls.MIN_DURATION_MS:
                sent_end = sent_start + cls.MIN_DURATION_MS
                if sent_end > event_ends[-1]:
                    sent_start = event_ends[-1] - cls.MIN_DURATION_MS
                    sent_end = event_ends[-1]

            result.append(pysubs2.SSAEvent(start=sent_start, end=sent_end, text=sent))
            last_end = sent_end

        return result

    @classmethod
    def process_subtitle_for_tts(
        cls,
        subtitle_file: str,
        output_file: str,
        lang: Optional[str] = None,
        model_size: str = "lg",
    ):
        try:
            subs = pysubs2.load(subtitle_file, encoding="utf-8")
            processed = cls.merge_and_split_events(subs, lang, model_size)
            new_subs = pysubs2.SSAFile()
            new_subs.events = processed
            new_subs.save(output_file)
            print(
                f"Processed {len(subs)} events into {len(processed)} events with model_size={model_size}"
            )
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False


if __name__ == "__main__":
    AbusSpacy.process_subtitle_for_tts("input.srt", "output.srt")
