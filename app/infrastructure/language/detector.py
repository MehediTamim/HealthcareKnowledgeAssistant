import re
from typing import Optional
from app.utils.logger import Logger

# Try to import dl-translate, fallback to regex if not available
try:
    import dl_translate as dlt
    DL_TRANSLATE_AVAILABLE = True
except ImportError:
    DL_TRANSLATE_AVAILABLE = False
    Logger.write_warning("dl-translate not available, falling back to regex detection")


class LanguageDetector:
    def __init__(self):
        self._dt: Optional[object] = None
        if DL_TRANSLATE_AVAILABLE:
            try:
                # Initialize dl-translate detector
                self._dt = dlt.TranslationModel()
                Logger.write_info("dl-translate language detector initialized")
            except Exception as e:
                Logger.write_warning(f"Failed to initialize dl-translate: {e}, using regex fallback")
                self._dt = None

    def detect(self, text: str) -> str:
        try:
            if not text or len(text.strip()) < 3:
                Logger.write_warning("Text too short for detection, defaulting to 'en'")
                return 'en'

            # Try dl-translate first if available
            if self._dt is not None and DL_TRANSLATE_AVAILABLE:
                try:
                    # Use dl-translate for language detection
                    detected_lang = self._dt.detect_language(text)
                    
                    # Map detected language to our supported languages (en/ja)
                    if detected_lang in ['ja', 'japanese']:
                        Logger.write_debug("dl-translate detected language: ja")
                        return 'ja'
                    else:
                        Logger.write_debug(f"dl-translate detected language: {detected_lang}, mapping to 'en'")
                        return 'en'
                        
                except Exception as e:
                    Logger.write_warning(f"dl-translate detection failed: {e}, falling back to regex")
                    # Fall through to regex detection
            
            # Fallback to regex-based detection
            japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')
            matches = japanese_pattern.findall(text)

            if len(matches) > len(text) * 0.1:
                Logger.write_debug("Regex detected language: ja")
                return 'ja'

            Logger.write_debug("Regex detected language: en")
            return 'en'

        except Exception as e:
            Logger.write_error(f"Language detection error: {e}, defaulting to 'en'")
            return 'en'


language_detector = LanguageDetector()
