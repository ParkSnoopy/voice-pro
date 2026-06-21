import unicodedata
import pysubs2
import re
from lingua import LanguageDetectorBuilder

import structlog

logger = structlog.get_logger()


class AbusText:
    detector = LanguageDetectorBuilder.from_all_languages().build()

    SENTENCE_ENDING_MARKS = {
        ".",  # 영어, 한국어, 대부분의 라틴 문자 언어
        "。",  # 일본어 (Kuten), 중국어 (Jùhào)
        "．",  # 일본어/중국어에서 풀폭 점으로 사용
        "!",  # 영어 등 감탄문
        "！",  # 중국어, 일본어 등 풀폭 감탄 부호
        "?",  # 영어 등 의문문
        "？",  # 중국어, 일본어 등 풀폭 물음표
        "۔",  # 아랍어 Full stop
        "।",  # 힌디어 (Pūrṇa virām)
        "॥",  # 힌디어 (Double Danda, 단락 끝)
    }

    PUNCTUATION_MARKS = {
        ".",  # 영어 등 문장 끝
        "。",  # 일본어, 중국어 문장 끝
        "．",  # 풀폭 점
        "!",  # 감탄
        "！",  # 풀폭 감탄
        "?",  # 의문
        "？",  # 풀폭 의문
        "۔",  # 아랍어 문장 끝
        "।",  # 힌디어 문장 끝
        "॥",  # 힌디어 단락 끝
        ",",  # 영어 등 쉼표
        "，",  # 중국어 쉼표 (Dòuhào)
        "、",  # 일본어 쉼표 (Tōten), 중국어 열거 (Dùnhào)
        ";",  # 세미콜론
        "；",  # 풀폭 세미콜론 (중국어 등)
        ":",  # 콜론
        "：",  # 풀폭 콜론
        "«",  # 인용 부호 (프랑스어, 러시아어, 아랍어)
        "»",  # 인용 부호 닫기
        "“",  # 큰따옴표 열기
        "”",  # 큰따옴표 닫기
        "‘",  # 작은따옴표 열기
        "’",  # 작은따옴표 닫기
        "「",  # 일본어 인용 열기
        "」",  # 일본어 인용 닫기
        "『",  # 일본어 이중 인용 열기
        "』",  # 일본어 이중 인용 닫기
        "(",  # 소괄호 열기
        ")",  # 소괄호 닫기
        "[",  # 대괄호 열기
        "]",  # 대괄호 닫기
        "…",  # 생략 부호
        "—",  # Em dash (삽입, 강조)
        "–",  # En dash (범위)
        "-",  # 하이픈
        "・",  # 일본어 나열 (Nakaguro)
        "·",  # 그리스어 상단 점 (Ano teleia)
    }

    PUNCTUATION_LANGUAGES = {
        "english",  # 영어: . , ; : ! ? 등
        "french",  # 프랑스어: . , ; : ! ? « » 등
        "german",  # 독일어: . , ; : ! ? " " 등
        "spanish",  # 스페인어: . , ; : ! ? ¿ ¡ 등
        "italian",  # 이탈리아어: . , ; : ! ? " " 등
        "portuguese",  # 포르투갈어: . , ; : ! ? " " 등
        "russian",  # 러시아어: . , ; : ! ? « » 등
        "korean",  # 한국어: . , ; : ! ? " " 등
        "japanese",  # 일본어: 。 、 「 」 ・ 등
        "chinese",  # 중국어: 。 ， ； ： ！ ？ " " 등
        "arabic",  # 아랍어: . ، ؛ : ؟ 등
        "hindi",  # 힌디어: । ॥ , 등
        "greek",  # 그리스어: . , ; · ! ? 등
    }

    JAPANESE_SEPARATORS = {
        "でも",
        "だし",
        "から",
        "ので",
    }  # 문맥상 명확한 구분점만 포함

    COMMON_ABBREVIATIONS = {
        "Mr.",
        "Mrs.",
        "Ms.",
        "Dr.",
        "Prof.",
        "Inc.",
        "Co.",
        "Ltd.",
        "U.S.",
        "U.S.A.",
        "E.g.",
        "i.e.",
        "etc.",
        "vs.",
        "Dept.",
    }

    # 일반적인 약어 패턴
    ABBREVIATION_PATTERNS = [
        r"\b([A-Z]\.)+[A-Z]?\b",  # J.D., U.S.A., U.S., etc.
        r"\b(Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.|Sr\.|Jr\.)\b",  # 일반적인 개인 약어
        r"\b(Inc\.|Corp\.|Ltd\.|Co\.)\b",  # 회사 관련 약어
        r"\b(e\.g\.|i\.e\.|vs\.)\b",  # 학술/참고 약어
    ]

    # 다국어 문장 종결 부호 매핑
    SENTENCE_END_MARKS = {
        "western": [".", "!", "?", "।", "॥"],
        "east_asian": ["。", "！", "？"],
        "other": ["۔", "।", "॥"],
    }

    @classmethod
    def is_punctuation_language(cls, language):
        # 구두점을 잘 사용하는 언어들의 리스트
        if language.lower() in cls.PUNCTUATION_LANGUAGES:
            return True
        else:
            return False

    @classmethod
    def split_text(cls, text, line_count):
        """텍스트를 라인 수에 맞게 분할하는 함수. 모든 언어 지원."""
        if not text or line_count < 1:
            return [""] * line_count if line_count > 0 else []

        # 공백으로 단어 분할이 가능한 언어인지 확인
        words = text.split()
        if len(words) > 1 and all(len(word) > 0 for word in words):
            # 공백 기반 언어(영어 등): 기존 단어 단위 분할 유지
            total_units = len(words)
            avg_units_per_line = total_units // line_count
            lines = []
            current_line = []
            unit_count = 0

            for word in words:
                current_line.append(word)
                unit_count += 1
                if unit_count >= avg_units_per_line and len(lines) < line_count - 1:
                    lines.append(" ".join(current_line))
                    current_line = []
                    unit_count = 0

            if current_line:
                lines.append(" ".join(current_line))
        else:
            # 공백이 없는 언어(일본어, 중국어 등): 문자 단위로 분할
            # 문장 부호를 기준으로 자연스럽게 나누기 위해 정규식 사용
            units = re.findall(
                r"[^\s.。．!！?？۔।॥,，、;；:：「」“”‘’「」『』()[]…—–-・·]+[.。．!！?？۔।॥,，、;；:：「」“”‘’「」『』()[]…—–-・·]*|\s+",
                text.strip(),
            )
            total_units = len(units)

            if total_units <= 1:  # 분할되지 않은 경우 문자 단위로 fallback
                units = list(text)
                total_units = len(units)

            avg_units_per_line = max(1, total_units // line_count)  # 최소 1 이상 보장
            lines = []
            current_line = []
            unit_count = 0

            for unit in units:
                current_line.append(unit)
                unit_count += 1
                if unit_count >= avg_units_per_line and len(lines) < line_count - 1:
                    lines.append("".join(current_line))
                    current_line = []
                    unit_count = 0

            if current_line:
                lines.append("".join(current_line))

        # 라인 수가 부족하면 빈 문자열 추가
        while len(lines) < line_count:
            lines.append("")

        return lines

    @classmethod
    def split_into_sentences(cls, text, has_punctuation=True):
        """텍스트를 문장 단위로 분리하는 함수"""
        if not has_punctuation:
            # 구두점이 없는 경우 한 줄을 하나의 문장으로 처리
            return [line.strip() for line in text.split("\n") if line.strip()]

        # 문장 끝 패턴을 정의 (.!? 뒤에 공백이나 문장의 끝)
        sentence_ends = re.compile(r"[.。．!！?？۔।॥]+[\s$]")

        # 문장의 시작 위치를 찾음
        start_positions = [0] + [m.end() for m in sentence_ends.finditer(text)]

        # 마지막 위치가 텍스트 끝이 아니라면 추가
        if start_positions[-1] < len(text):
            start_positions.append(len(text))

        # 문장들을 추출
        sentences = []
        for i in range(len(start_positions) - 1):
            sentence = text[start_positions[i] : start_positions[i + 1]].strip()
            if sentence:  # 빈 문장은 제외
                sentences.append(sentence)

        return sentences

    @classmethod
    def has_punctuation_marks(cls, text):
        if not text or not text.strip():
            return False

        text = text.strip()

        for char in text:
            if char in cls.PUNCTUATION_MARKS:
                return True
        return False

    @classmethod
    def has_ending_marks(cls, lines):
        if not lines or len(lines) < 1:
            return False

        match_count = 0
        for text in lines:
            if cls.check_sentence_ending(text) == True:
                match_count += 1

        # 최소한 5줄당 1번은 마침표가 나와야 True
        match_ratio = match_count / len(lines)
        return True if match_ratio > 0.2 else False

    @classmethod
    def check_sentence_ending(cls, text):
        if not text or not text.strip():
            return False

        text = text.strip()

        last_char = text[-1]
        if last_char in cls.SENTENCE_ENDING_MARKS:
            return True

        return False

    @classmethod
    def normalize_text(cls, text) -> str:
        logger.debug(f"[abus_text.py] normalize_text - text: {text}")

        # 유지할 통화 기호 목록
        currency_symbols = "₩$€£¥₹₽₺₴₱"

        # 허용할 유니코드 카테고리 목록
        allowed_categories = {
            "Lu",
            "Ll",
            "Lt",
            "Lm",
            "Lo",  # 문자 (대문자, 소문자, 타이틀 케이스, 수정자, 기타)
            "Nd",
            "Nl",
            "No",  # 숫자 (십진수, 글자, 기타)
            "Pc",
            "Pd",
            "Ps",
            "Pe",
            "Pi",
            "Pf",
            "Po",  # 문장 부호
            "Zs",  # 공백
            "Mn",
            "Mc",  # 발음 구별 기호 (비간격, 간격)
        }

        def filter_char(ch):
            category = unicodedata.category(ch)
            if category in allowed_categories or ch in currency_symbols:
                return ch
            return ""

        # 1. 괄호 제거
        cleaned_text = re.sub(r"\([^()]*\)", "", text)
        cleaned_text = re.sub(r"\[.*?\]", "", cleaned_text)
        cleaned_text = re.sub(r"\{.*?\}", "", cleaned_text)

        # 2. 특수 기호 및 약어 처리
        cleaned_text = re.sub(r"(\bMr)\.", r"\1", cleaned_text)
        cleaned_text = re.sub(r"&", " and ", cleaned_text)
        cleaned_text = re.sub(r"%", " percent", cleaned_text)
        cleaned_text = re.sub(r"(\d+)km", r"\1 kilometers", cleaned_text)

        # 3. 문자 필터링
        cleaned_text = "".join(filter_char(ch) for ch in cleaned_text)

        # 4. 구두점 최적화
        cleaned_text = re.sub(r"(!)\1+", r"\1", cleaned_text)
        cleaned_text = re.sub(r"(\.)\1+", r".", cleaned_text)

        # 5. 연속 공백 및 단어 반복 제거
        cleaned_text = re.sub(r"\b(\w+)\s+\1\b", r"\1", cleaned_text)
        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

        logger.debug(f"[abus_text.py] normalize_text - cleaned: {cleaned_text}")
        return cleaned_text

    @classmethod
    def is_subtitle_format(cls, text):
        try:
            pysubs2.SSAFile.from_string(text)
            return True
        except Exception:
            return False

    @classmethod
    def merge_and_split_events(cls, subs):
        """
        자막 이벤트를 TTS에 적합하게 변환:
        - 이벤트 단위를 기본으로 존중하며, 종결 부호나 주요 접속사로만 분리
        - 과도한 분할 방지
        """
        final_events = []

        # 1단계: 이벤트별로 기본 분리
        for event in subs:
            text = event.plaintext.strip()
            if not text:
                continue

            # 문장 분리 (종결 부호 또는 주요 접속사 기준)
            sentences = []
            current_sentence = ""

            # 일본어는 공백이 없으므로 전체 텍스트를 순회
            i = 0
            while i < len(text):
                current_sentence += text[i]
                # 문장 끝 종결 부호 확인
                if text[i] in cls.SENTENCE_ENDING_MARKS and i == len(text) - 1:
                    sentences.append(current_sentence.strip())
                    current_sentence = ""
                # 주요 접속사로 분리 (최소 길이 5자 이상 확보)
                elif i + 1 < len(text) and any(
                    text[i - len(sep) + 1 : i + 1] == sep
                    for sep in cls.JAPANESE_SEPARATORS
                ):
                    if len(current_sentence) >= 5:  # 너무 짧은 분할 방지
                        sentences.append(current_sentence.strip())
                        current_sentence = ""
                i += 1

            if current_sentence.strip():
                sentences.append(current_sentence.strip())
            if not sentences:
                sentences = [text.strip()]

            # 타임코드 분배
            duration_per_sentence = (event.end - event.start) // max(1, len(sentences))
            for j, sentence in enumerate(sentences):
                event_start = event.start + j * duration_per_sentence
                event_end = (
                    event_start + duration_per_sentence
                    if j < len(sentences) - 1
                    else event.end
                )
                new_event = pysubs2.SSAEvent(
                    start=event_start, end=event_end, text=sentence
                )
                final_events.append(new_event)

        # 2단계: 병합 (타임 갭이 짧고 종결 부호로 끝나지 않은 경우)
        merged_events = []
        current_event = None

        for event in final_events:
            if not current_event:
                current_event = event
            else:
                gap = event.start - current_event.end
                if gap < 500 and not any(
                    current_event.text.rstrip().endswith(mark)
                    for mark in cls.SENTENCE_ENDING_MARKS
                ):
                    current_event.text += " " + event.text
                    current_event.end = event.end
                else:
                    merged_events.append(current_event)
                    current_event = event

        if current_event:
            merged_events.append(current_event)

        return merged_events

    @classmethod
    def process_subtitle_for_tts(cls, subtitle_file, output_file):
        """자막 파일을 로드하고 TTS에 적합한 형태로 변환 후 저장"""
        subs = pysubs2.load(subtitle_file, encoding="utf-8")

        text_list = [line.text for line in subs]
        if cls.has_ending_marks(text_list):
            new_events = cls.merge_and_split_events(subs)
            new_subs = pysubs2.SSAFile()
            new_subs.events = new_events
            new_subs.save(output_file)
        else:
            subs.save(output_file)

    #########################################################################################

    @classmethod
    def split_translated_subtitles(cls, input_file, translated_file, output_file):
        # no action!!
        translated_subs = pysubs2.load(translated_file)
        translated_subs.save(output_file)

    #########################################################################################

    @classmethod
    def truncate_subs(cls, full_subs, remains=12):
        subs = pysubs2.SSAFile()
        for i, sub in enumerate(full_subs):
            if i < remains:
                subs.append(sub)
            else:
                break
        return subs

    @classmethod
    def detect_language_name(cls, text: str) -> str:
        try:
            detected_lang = cls.detector.detect_language_of(text)
            return detected_lang.name.capitalize()
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return "English"  # 오류 발생 시 영어로 기본 설정
