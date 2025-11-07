import re
from app.utils.logger import Logger


class LanguageDetector:
    @staticmethod
    def detect(text: str) -> str:
        try:
            if not text or len(text.strip()) < 3:
                Logger.write_warning("Text too short for detection, defaulting to 'en'")
                return 'en'

            japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')
            matches = japanese_pattern.findall(text)

            if len(matches) > len(text) * 0.1:
                Logger.write_debug("Detected language: ja")
                return 'ja'

            Logger.write_debug("Detected language: en")
            return 'en'

        except Exception as e:
            Logger.write_error(f"Language detection error: {e}, defaulting to 'en'")
            return 'en'


language_detector = LanguageDetector()
