import iso639
from src.iso_country_codes import *


import os
import json5
import csv

from app.abus_path import *
from app.abus_hf_file import *

import structlog

logger = structlog.get_logger()


def captitalize_first_char(string):
    if not string:
        return string
    return string[0].upper() + string[1:]


# 'af-ZA-AdriNeural' : LangCode - CountryCode - Character


class MSVoice:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def __str__(self):
        return f"MSVoice(name={self.name}, gender={self.gender})"

    def getDisplayName(self):
        return f"{self.getCountryName()}-{self.getCharacterName()}-{self.gender}"

    def getLanguageCode(self):
        words = self.name.split("-")
        code = words[0]
        return code

    def getLanguageName(self):
        try:
            code = self.getLanguageCode()
            if len(code) == 2:
                lang = iso639.Language.from_part1(code)
            elif len(code) == 3:
                lang = iso639.Language.from_part2b(code)
            return lang.name
        except iso639.LanguageNotFoundError:
            return "English"

    def getCountryCode(self):
        words = self.name.split("-")
        code = words[1]
        return code

    def getCountryName(self):
        country = CC[self.getCountryCode()]
        return country

    def getCharacterName(self):
        words = self.name.split("-")
        code = words[2]
        name = code.replace("Neural", "")
        return name


class TextSample:
    def __init__(self, language, text):
        self.language = language
        self.text = text

    def __str__(self):
        return f"Language: {self.language}, Text: {self.text}"


class Speaker:
    def __init__(
        self, name, gender, language, country, categories, personalities, sample
    ):
        self.name = name
        self.gender = gender
        self.language = language
        self.country = country
        self.categories = categories
        self.personalities = personalities
        self.sample = sample

    def __str__(self):
        return f"Name: {self.name}, Gender: {self.gender}, Language: {self.language}, Country: {self.country}, Categories: {self.categories}, Personalities: {self.personalities}, Sample: {self.sample}"


class MSVoiceManager:
    def __init__(self, language: str = "English") -> None:
        self.selectedLanguageName = language

        self.text_samples = {}
        self.speakers = []
        # self._download_hf()

        if True:  # self.download_success:
            languages_with_text_json = os.path.join(
                path_model_folder(),
                "edge-tts",
                "edge-tts-samples",
                "languages-with-text.json",
            )
            self._load_languages_with_text(languages_with_text_json)

            tts_samples_csv = os.path.join(
                path_model_folder(), "edge-tts", "edge-tts-samples", "tts-samples.csv"
            )
            self._load_tts_samples(tts_samples_csv)

    def _download_hf(self):
        edge_tts_samples = HF_File(
            "edge-tts", "ABUS-AI/CosyVoice", "", "edge-tts-samples.zip", 8050329, 0
        )
        self.download_success, _ = edge_tts_samples.download(force_download=False)

    def _load_languages_with_text(self, languages_with_text_json):
        self.text_samples = {}

        try:
            with open(languages_with_text_json, "r", encoding="utf-8") as file:
                data = json5.load(file)

                for key, value in data.items():
                    language = value["language"]
                    text = value["text"]
                    self.text_samples[key] = TextSample(language, text)
        except Exception as e:
            logger.error(f"[abus_voice_ms.py] _load_languages_with_text - Error: {e}")

    def _load_tts_samples(self, tts_samples_csv):
        self.speakers = []
        try:
            with open(
                tts_samples_csv, "r", encoding="utf-8"
            ) as file:  # UTF-8 인코딩 명시
                reader = csv.DictReader(file)  # DictReader를 사용하여 헤더를 키로 접근
                for row in reader:
                    speaker = Speaker(
                        row["Name"],
                        row["Gender"],
                        row["Language"],
                        row["Country"],
                        row["Categories"],
                        row["Personalities"],
                        row["Sample"],
                    )
                    self.speakers.append(speaker)
        except Exception as e:
            logger.error(f"[abus_voice_ms.py] _load_tts_samples - Error: {e}")

    def get_all_language_names(self):
        unique_languages = list(set(voice.getLanguageName() for voice in MS_VOICES))
        sorted_languages = sorted(unique_languages)
        return sorted_languages

    def select_language(self, languageName: str):
        self.selectedLanguageName = languageName

    def get_voices(self, languageName: str) -> list:
        if languageName is None or len(languageName) <= 0:
            return []

        splits = languageName.split()
        if len(splits) > 1:
            languageName = splits[0]

        languageName = captitalize_first_char(languageName)
        logger.debug(f"[abus_voice_ms.py] get_voices - languageName = {languageName}")
        try:
            lang = iso639.Language.from_name(languageName)
            voices = [
                voice for voice in MS_VOICES if voice.getLanguageCode() == lang.part1
            ]
            return voices
        except iso639.LanguageNotFoundError:
            return []

    def get_voices_with_code(self, languageCode: str) -> list:
        if languageCode is None or len(languageCode) <= 0:
            return []

        splits = languageCode.split()
        if len(splits) > 1:
            languageCode = splits[0]

        logger.debug(f"get_voices: from_part1: languageCode = {languageCode}")
        voices = [
            voice for voice in MS_VOICES if voice.getLanguageCode() == languageCode
        ]
        return voices

    def get_voice(self, displayName: str) -> MSVoice:
        words = displayName.split("-")
        country = words[0]
        name = words[1]
        gender = words[2]

        for voice in MS_VOICES:
            voice_parts = voice.name.split("-")
            voice_name = voice_parts[2]

            if voice.gender == gender and name + "Neural" == voice_name:
                # logger.debug(f'[abus_voice_ms.py] get_voice - find!! displayName = {displayName}, voice = {voice}')
                return voice
        logger.debug(
            f"[abus_voice_ms.py] get_voice - error!! displayName = {displayName}"
        )
        return None

    def get_voice_sample(self, displayName: str) -> str:
        ms_voice = self.get_voice(displayName)
        logger.debug(f"[abus_voice_ms.py] get_voice_sample - ms_voice = {ms_voice}")

        if ms_voice:
            char_name = ms_voice.getCharacterName().lower()
            for spk in self.speakers:
                logger.debug(f"[abus_voice_ms.py] get_voice_sample - spk = {spk}")
                if (
                    spk.name.lower() == char_name
                    or spk.name.lower() == char_name + "multilingual"
                ):
                    # logger.debug(f'[abus_voice_ms.py] get_voice_sample - find!! displayName = {displayName}, sample = {spk.sample}')
                    return os.path.join(
                        path_model_folder(), "edge-tts", "edge-tts-samples", spk.sample
                    )
        logger.debug(
            f"[abus_voice_ms.py] get_voice_sample - error!! displayName = {displayName}"
        )
        return None


MS_VOICES = [
    MSVoice("af-ZA-AdriNeural", "Female"),
    MSVoice("af-ZA-WillemNeural", "Male"),
    MSVoice("af-ZA-AdriNeural", "Female"),
    MSVoice("af-ZA-WillemNeural", "Male"),
    MSVoice("am-ET-AmehaNeural", "Male"),
    MSVoice("am-ET-MekdesNeural", "Female"),
    MSVoice("ar-AE-FatimaNeural", "Female"),
    MSVoice("ar-AE-HamdanNeural", "Male"),
    MSVoice("ar-BH-AliNeural", "Male"),
    MSVoice("ar-BH-LailaNeural", "Female"),
    MSVoice("ar-DZ-AminaNeural", "Female"),
    MSVoice("ar-DZ-IsmaelNeural", "Male"),
    MSVoice("ar-EG-SalmaNeural", "Female"),
    MSVoice("ar-EG-ShakirNeural", "Male"),
    MSVoice("ar-IQ-BasselNeural", "Male"),
    MSVoice("ar-IQ-RanaNeural", "Female"),
    MSVoice("ar-JO-SanaNeural", "Female"),
    MSVoice("ar-JO-TaimNeural", "Male"),
    MSVoice("ar-KW-FahedNeural", "Male"),
    MSVoice("ar-KW-NouraNeural", "Female"),
    MSVoice("ar-LB-LaylaNeural", "Female"),
    MSVoice("ar-LB-RamiNeural", "Male"),
    MSVoice("ar-LY-ImanNeural", "Female"),
    MSVoice("ar-LY-OmarNeural", "Male"),
    MSVoice("ar-MA-JamalNeural", "Male"),
    MSVoice("ar-MA-MounaNeural", "Female"),
    MSVoice("ar-OM-AbdullahNeural", "Male"),
    MSVoice("ar-OM-AyshaNeural", "Female"),
    MSVoice("ar-QA-AmalNeural", "Female"),
    MSVoice("ar-QA-MoazNeural", "Male"),
    MSVoice("ar-SA-HamedNeural", "Male"),
    MSVoice("ar-SA-ZariyahNeural", "Female"),
    MSVoice("ar-SY-AmanyNeural", "Female"),
    MSVoice("ar-SY-LaithNeural", "Male"),
    MSVoice("ar-TN-HediNeural", "Male"),
    MSVoice("ar-TN-ReemNeural", "Female"),
    MSVoice("ar-YE-MaryamNeural", "Female"),
    MSVoice("ar-YE-SalehNeural", "Male"),
    MSVoice("az-AZ-BabekNeural", "Male"),
    MSVoice("az-AZ-BanuNeural", "Female"),
    MSVoice("bg-BG-BorislavNeural", "Male"),
    MSVoice("bg-BG-KalinaNeural", "Female"),
    MSVoice("bn-BD-NabanitaNeural", "Female"),
    MSVoice("bn-BD-PradeepNeural", "Male"),
    MSVoice("bn-IN-BashkarNeural", "Male"),
    MSVoice("bn-IN-TanishaaNeural", "Female"),
    MSVoice("bs-BA-GoranNeural", "Male"),
    MSVoice("bs-BA-VesnaNeural", "Female"),
    MSVoice("ca-ES-EnricNeural", "Male"),
    MSVoice("ca-ES-JoanaNeural", "Female"),
    MSVoice("cs-CZ-AntoninNeural", "Male"),
    MSVoice("cs-CZ-VlastaNeural", "Female"),
    MSVoice("cy-GB-AledNeural", "Male"),
    MSVoice("cy-GB-NiaNeural", "Female"),
    MSVoice("da-DK-ChristelNeural", "Female"),
    MSVoice("da-DK-JeppeNeural", "Male"),
    MSVoice("de-AT-IngridNeural", "Female"),
    MSVoice("de-AT-JonasNeural", "Male"),
    MSVoice("de-CH-JanNeural", "Male"),
    MSVoice("de-CH-LeniNeural", "Female"),
    MSVoice("de-DE-AmalaNeural", "Female"),
    MSVoice("de-DE-ConradNeural", "Male"),
    MSVoice("de-DE-FlorianMultilingualNeural", "Male"),
    MSVoice("de-DE-FlorianNeural", "Male"),
    MSVoice("de-DE-KatjaNeural", "Female"),
    MSVoice("de-DE-KillianNeural", "Male"),
    MSVoice("de-DE-SeraphinaMultilingualNeural", "Female"),
    MSVoice("de-DE-SeraphinaNeural", "Female"),
    MSVoice("el-GR-AthinaNeural", "Female"),
    MSVoice("el-GR-NestorasNeural", "Male"),
    MSVoice("en-AU-NatashaNeural", "Female"),
    MSVoice("en-AU-WilliamNeural", "Male"),
    MSVoice("en-CA-ClaraNeural", "Female"),
    MSVoice("en-CA-LiamNeural", "Male"),
    MSVoice("en-GB-LibbyNeural", "Female"),
    MSVoice("en-GB-MaisieNeural", "Female"),
    MSVoice("en-GB-RyanNeural", "Male"),
    MSVoice("en-GB-SoniaNeural", "Female"),
    MSVoice("en-GB-ThomasNeural", "Male"),
    MSVoice("en-HK-SamNeural", "Male"),
    MSVoice("en-HK-YanNeural", "Female"),
    MSVoice("en-IE-ConnorNeural", "Male"),
    MSVoice("en-IE-EmilyNeural", "Female"),
    MSVoice("en-IN-NeerjaExpressiveNeural", "Female"),
    MSVoice("en-IN-NeerjaNeural", "Female"),
    MSVoice("en-IN-PrabhatNeural", "Male"),
    MSVoice("en-KE-AsiliaNeural", "Female"),
    MSVoice("en-KE-ChilembaNeural", "Male"),
    MSVoice("en-NG-AbeoNeural", "Male"),
    MSVoice("en-NG-EzinneNeural", "Female"),
    MSVoice("en-NZ-MitchellNeural", "Male"),
    MSVoice("en-NZ-MollyNeural", "Female"),
    MSVoice("en-PH-JamesNeural", "Male"),
    MSVoice("en-PH-RosaNeural", "Female"),
    MSVoice("en-SG-LunaNeural", "Female"),
    MSVoice("en-SG-WayneNeural", "Male"),
    MSVoice("en-TZ-ElimuNeural", "Male"),
    MSVoice("en-TZ-ImaniNeural", "Female"),
    MSVoice("en-US-AnaNeural", "Female"),
    MSVoice("en-US-AndrewMultilingualNeural", "Male"),
    MSVoice("en-US-AndrewNeural", "Male"),
    MSVoice("en-US-AriaNeural", "Female"),
    MSVoice("en-US-AvaMultilingualNeural", "Female"),
    MSVoice("en-US-AvaNeural", "Female"),
    MSVoice("en-US-BrianMultilingualNeural", "Male"),
    MSVoice("en-US-BrianNeural", "Male"),
    MSVoice("en-US-ChristopherNeural", "Male"),
    MSVoice("en-US-EmmaMultilingualNeural", "Female"),
    MSVoice("en-US-EmmaNeural", "Female"),
    MSVoice("en-US-EricNeural", "Male"),
    MSVoice("en-US-GuyNeural", "Male"),
    MSVoice("en-US-JennyNeural", "Female"),
    MSVoice("en-US-MichelleNeural", "Female"),
    MSVoice("en-US-RogerNeural", "Male"),
    MSVoice("en-US-SteffanNeural", "Male"),
    MSVoice("en-ZA-LeahNeural", "Female"),
    MSVoice("en-ZA-LukeNeural", "Male"),
    MSVoice("es-AR-ElenaNeural", "Female"),
    MSVoice("es-AR-TomasNeural", "Male"),
    MSVoice("es-BO-MarceloNeural", "Male"),
    MSVoice("es-BO-SofiaNeural", "Female"),
    MSVoice("es-CL-CatalinaNeural", "Female"),
    MSVoice("es-CL-LorenzoNeural", "Male"),
    MSVoice("es-CO-GonzaloNeural", "Male"),
    MSVoice("es-CO-SalomeNeural", "Female"),
    MSVoice("es-CR-JuanNeural", "Male"),
    MSVoice("es-CR-MariaNeural", "Female"),
    MSVoice("es-CU-BelkysNeural", "Female"),
    MSVoice("es-CU-ManuelNeural", "Male"),
    MSVoice("es-DO-EmilioNeural", "Male"),
    MSVoice("es-DO-RamonaNeural", "Female"),
    MSVoice("es-EC-AndreaNeural", "Female"),
    MSVoice("es-EC-LuisNeural", "Male"),
    MSVoice("es-ES-AlvaroNeural", "Male"),
    MSVoice("es-ES-ElviraNeural", "Female"),
    MSVoice("es-ES-XimenaNeural", "Female"),
    MSVoice("es-GQ-JavierNeural", "Male"),
    MSVoice("es-GQ-TeresaNeural", "Female"),
    MSVoice("es-GT-AndresNeural", "Male"),
    MSVoice("es-GT-MartaNeural", "Female"),
    MSVoice("es-HN-CarlosNeural", "Male"),
    MSVoice("es-HN-KarlaNeural", "Female"),
    MSVoice("es-MX-DaliaNeural", "Female"),
    MSVoice("es-MX-JorgeNeural", "Male"),
    MSVoice("es-NI-FedericoNeural", "Male"),
    MSVoice("es-NI-YolandaNeural", "Female"),
    MSVoice("es-PA-MargaritaNeural", "Female"),
    MSVoice("es-PA-RobertoNeural", "Male"),
    MSVoice("es-PE-AlexNeural", "Male"),
    MSVoice("es-PE-CamilaNeural", "Female"),
    MSVoice("es-PR-KarinaNeural", "Female"),
    MSVoice("es-PR-VictorNeural", "Male"),
    MSVoice("es-PY-MarioNeural", "Male"),
    MSVoice("es-PY-TaniaNeural", "Female"),
    MSVoice("es-SV-LorenaNeural", "Female"),
    MSVoice("es-SV-RodrigoNeural", "Male"),
    MSVoice("es-US-AlonsoNeural", "Male"),
    MSVoice("es-US-PalomaNeural", "Female"),
    MSVoice("es-UY-MateoNeural", "Male"),
    MSVoice("es-UY-ValentinaNeural", "Female"),
    MSVoice("es-VE-PaolaNeural", "Female"),
    MSVoice("es-VE-SebastianNeural", "Male"),
    MSVoice("et-EE-AnuNeural", "Female"),
    MSVoice("et-EE-KertNeural", "Male"),
    MSVoice("fa-IR-DilaraNeural", "Female"),
    MSVoice("fa-IR-FaridNeural", "Male"),
    MSVoice("fi-FI-HarriNeural", "Male"),
    MSVoice("fi-FI-NooraNeural", "Female"),
    MSVoice("fil-PH-AngeloNeural", "Male"),
    MSVoice("fil-PH-BlessicaNeural", "Female"),
    MSVoice("fr-BE-CharlineNeural", "Female"),
    MSVoice("fr-BE-GerardNeural", "Male"),
    MSVoice("fr-CA-AntoineNeural", "Male"),
    MSVoice("fr-CA-JeanNeural", "Male"),
    MSVoice("fr-CA-SylvieNeural", "Female"),
    MSVoice("fr-CA-ThierryNeural", "Male"),
    MSVoice("fr-CH-ArianeNeural", "Female"),
    MSVoice("fr-CH-FabriceNeural", "Male"),
    MSVoice("fr-FR-DeniseNeural", "Female"),
    MSVoice("fr-FR-EloiseNeural", "Female"),
    MSVoice("fr-FR-HenriNeural", "Male"),
    MSVoice("fr-FR-RemyMultilingualNeural", "Male"),
    MSVoice("fr-FR-RemyNeural", "Male"),
    MSVoice("fr-FR-VivienneMultilingualNeural", "Female"),
    MSVoice("fr-FR-VivienneNeural", "Female"),
    MSVoice("ga-IE-ColmNeural", "Male"),
    MSVoice("ga-IE-OrlaNeural", "Female"),
    MSVoice("gl-ES-RoiNeural", "Male"),
    MSVoice("gl-ES-SabelaNeural", "Female"),
    MSVoice("gu-IN-DhwaniNeural", "Female"),
    MSVoice("gu-IN-NiranjanNeural", "Male"),
    MSVoice("he-IL-AvriNeural", "Male"),
    MSVoice("he-IL-HilaNeural", "Female"),
    MSVoice("hi-IN-MadhurNeural", "Male"),
    MSVoice("hi-IN-SwaraNeural", "Female"),
    MSVoice("hr-HR-GabrijelaNeural", "Female"),
    MSVoice("hr-HR-SreckoNeural", "Male"),
    MSVoice("hu-HU-NoemiNeural", "Female"),
    MSVoice("hu-HU-TamasNeural", "Male"),
    MSVoice("id-ID-ArdiNeural", "Male"),
    MSVoice("id-ID-GadisNeural", "Female"),
    MSVoice("is-IS-GudrunNeural", "Female"),
    MSVoice("is-IS-GunnarNeural", "Male"),
    MSVoice("it-IT-DiegoNeural", "Male"),
    MSVoice("it-IT-ElsaNeural", "Female"),
    MSVoice("it-IT-GiuseppeMultilingualNeural", "Male"),
    MSVoice("it-IT-GiuseppeNeural", "Male"),
    MSVoice("it-IT-IsabellaNeural", "Female"),
    MSVoice("ja-JP-KeitaNeural", "Male"),
    MSVoice("ja-JP-NanamiNeural", "Female"),
    MSVoice("jv-ID-DimasNeural", "Male"),
    MSVoice("jv-ID-SitiNeural", "Female"),
    MSVoice("ka-GE-EkaNeural", "Female"),
    MSVoice("ka-GE-GiorgiNeural", "Male"),
    MSVoice("kk-KZ-AigulNeural", "Female"),
    MSVoice("kk-KZ-DauletNeural", "Male"),
    MSVoice("km-KH-PisethNeural", "Male"),
    MSVoice("km-KH-SreymomNeural", "Female"),
    MSVoice("kn-IN-GaganNeural", "Male"),
    MSVoice("kn-IN-SapnaNeural", "Female"),
    MSVoice("ko-KR-HyunsuMultilingualNeural", "Male"),
    MSVoice("ko-KR-HyunsuNeural", "Male"),
    MSVoice("ko-KR-InJoonNeural", "Male"),
    MSVoice("ko-KR-SunHiNeural", "Female"),
    MSVoice("lo-LA-ChanthavongNeural", "Male"),
    MSVoice("lo-LA-KeomanyNeural", "Female"),
    MSVoice("lt-LT-LeonasNeural", "Male"),
    MSVoice("lt-LT-OnaNeural", "Female"),
    MSVoice("lv-LV-EveritaNeural", "Female"),
    MSVoice("lv-LV-NilsNeural", "Male"),
    MSVoice("mk-MK-AleksandarNeural", "Male"),
    MSVoice("mk-MK-MarijaNeural", "Female"),
    MSVoice("ml-IN-MidhunNeural", "Male"),
    MSVoice("ml-IN-SobhanaNeural", "Female"),
    MSVoice("mn-MN-BataaNeural", "Male"),
    MSVoice("mn-MN-YesuiNeural", "Female"),
    MSVoice("mr-IN-AarohiNeural", "Female"),
    MSVoice("mr-IN-ManoharNeural", "Male"),
    MSVoice("ms-MY-OsmanNeural", "Male"),
    MSVoice("ms-MY-YasminNeural", "Female"),
    MSVoice("mt-MT-GraceNeural", "Female"),
    MSVoice("mt-MT-JosephNeural", "Male"),
    MSVoice("my-MM-NilarNeural", "Female"),
    MSVoice("my-MM-ThihaNeural", "Male"),
    MSVoice("nb-NO-FinnNeural", "Male"),
    MSVoice("nb-NO-PernilleNeural", "Female"),
    MSVoice("ne-NP-HemkalaNeural", "Female"),
    MSVoice("ne-NP-SagarNeural", "Male"),
    MSVoice("nl-BE-ArnaudNeural", "Male"),
    MSVoice("nl-BE-DenaNeural", "Female"),
    MSVoice("nl-NL-ColetteNeural", "Female"),
    MSVoice("nl-NL-FennaNeural", "Female"),
    MSVoice("nl-NL-MaartenNeural", "Male"),
    MSVoice("pl-PL-MarekNeural", "Male"),
    MSVoice("pl-PL-ZofiaNeural", "Female"),
    MSVoice("ps-AF-GulNawazNeural", "Male"),
    MSVoice("ps-AF-LatifaNeural", "Female"),
    MSVoice("pt-BR-AntonioNeural", "Male"),
    MSVoice("pt-BR-FranciscaNeural", "Female"),
    MSVoice("pt-BR-ThalitaMultilingualNeural", "Female"),
    MSVoice("pt-BR-ThalitaNeural", "Female"),
    MSVoice("pt-PT-DuarteNeural", "Male"),
    MSVoice("pt-PT-RaquelNeural", "Female"),
    MSVoice("ro-RO-AlinaNeural", "Female"),
    MSVoice("ro-RO-EmilNeural", "Male"),
    MSVoice("ru-RU-DmitryNeural", "Male"),
    MSVoice("ru-RU-SvetlanaNeural", "Female"),
    MSVoice("si-LK-SameeraNeural", "Male"),
    MSVoice("si-LK-ThiliniNeural", "Female"),
    MSVoice("sk-SK-LukasNeural", "Male"),
    MSVoice("sk-SK-ViktoriaNeural", "Female"),
    MSVoice("sl-SI-PetraNeural", "Female"),
    MSVoice("sl-SI-RokNeural", "Male"),
    MSVoice("so-SO-MuuseNeural", "Male"),
    MSVoice("so-SO-UbaxNeural", "Female"),
    MSVoice("sq-AL-AnilaNeural", "Female"),
    MSVoice("sq-AL-IlirNeural", "Male"),
    MSVoice("sr-RS-NicholasNeural", "Male"),
    MSVoice("sr-RS-SophieNeural", "Female"),
    MSVoice("su-ID-JajangNeural", "Male"),
    MSVoice("su-ID-TutiNeural", "Female"),
    MSVoice("sv-SE-MattiasNeural", "Male"),
    MSVoice("sv-SE-SofieNeural", "Female"),
    MSVoice("sw-KE-RafikiNeural", "Male"),
    MSVoice("sw-KE-ZuriNeural", "Female"),
    MSVoice("sw-TZ-DaudiNeural", "Male"),
    MSVoice("sw-TZ-RehemaNeural", "Female"),
    MSVoice("ta-IN-PallaviNeural", "Female"),
    MSVoice("ta-IN-ValluvarNeural", "Male"),
    MSVoice("ta-LK-KumarNeural", "Male"),
    MSVoice("ta-LK-SaranyaNeural", "Female"),
    MSVoice("ta-MY-KaniNeural", "Female"),
    MSVoice("ta-MY-SuryaNeural", "Male"),
    MSVoice("ta-SG-AnbuNeural", "Male"),
    MSVoice("ta-SG-VenbaNeural", "Female"),
    MSVoice("te-IN-MohanNeural", "Male"),
    MSVoice("te-IN-ShrutiNeural", "Female"),
    MSVoice("th-TH-NiwatNeural", "Male"),
    MSVoice("th-TH-PremwadeeNeural", "Female"),
    MSVoice("tr-TR-AhmetNeural", "Male"),
    MSVoice("tr-TR-EmelNeural", "Female"),
    MSVoice("uk-UA-OstapNeural", "Male"),
    MSVoice("uk-UA-PolinaNeural", "Female"),
    MSVoice("ur-IN-GulNeural", "Female"),
    MSVoice("ur-IN-SalmanNeural", "Male"),
    MSVoice("ur-PK-AsadNeural", "Male"),
    MSVoice("ur-PK-UzmaNeural", "Female"),
    MSVoice("uz-UZ-MadinaNeural", "Female"),
    MSVoice("uz-UZ-SardorNeural", "Male"),
    MSVoice("vi-VN-HoaiMyNeural", "Female"),
    MSVoice("vi-VN-NamMinhNeural", "Male"),
    MSVoice("zh-CN-XiaoxiaoNeural", "Female"),
    MSVoice("zh-CN-XiaoyiNeural", "Female"),
    MSVoice("zh-CN-YunjianNeural", "Male"),
    MSVoice("zh-CN-YunxiNeural", "Male"),
    MSVoice("zh-CN-YunxiaNeural", "Male"),
    MSVoice("zh-CN-YunyangNeural", "Male"),
    MSVoice("zh-CN-liaoning-XiaobeiNeural", "Female"),
    MSVoice("zh-CN-shaanxi-XiaoniNeural", "Female"),
    MSVoice("zh-HK-HiuGaaiNeural", "Female"),
    MSVoice("zh-HK-HiuMaanNeural", "Female"),
    MSVoice("zh-HK-WanLungNeural", "Male"),
    MSVoice("zh-TW-HsiaoChenNeural", "Female"),
    MSVoice("zh-TW-HsiaoYuNeural", "Female"),
    MSVoice("zh-TW-YunJheNeural", "Male"),
    MSVoice("zu-ZA-ThandoNeural", "Female"),
    MSVoice("zu-ZA-ThembaNeural", "Male"),
]
