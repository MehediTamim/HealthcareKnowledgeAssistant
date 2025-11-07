from typing import Optional
from app.utils.logger import Logger

# Try to import dl-translate, fallback to mock if not available
try:
    import dl_translate as dlt
    DL_TRANSLATE_AVAILABLE = True
except ImportError:
    DL_TRANSLATE_AVAILABLE = False
    Logger.write_warning("dl-translate not available, falling back to mock translation")


class TranslatorService:
    def __init__(self):
        self._mt: Optional[object] = None
        if DL_TRANSLATE_AVAILABLE:
            try:
                # Initialize dl-translate model
                self._mt = dlt.TranslationModel()
                Logger.write_info("dl-translate translator initialized")
            except Exception as e:
                Logger.write_warning(f"Failed to initialize dl-translate: {e}, using mock translation")
                self._mt = None

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        try:
            if source_lang == target_lang:
                return text

            if not text or len(text.strip()) == 0:
                return text

            # Try dl-translate first if available
            if self._mt is not None and DL_TRANSLATE_AVAILABLE:
                try:
                    # Map our language codes to dl-translate format
                    source_code = 'ja' if source_lang == 'ja' else 'en'
                    target_code = 'ja' if target_lang == 'ja' else 'en'
                    
                    Logger.write_info(f"dl-translate translation: {source_code} -> {target_code}")
                    
                    # Use dl-translate for actual translation
                    translated = self._mt.translate(text, source=source_code, target=target_code)
                    
                    Logger.write_debug(f"Translation completed: {len(text)} -> {len(translated)} chars")
                    return translated
                    
                except Exception as e:
                    Logger.write_warning(f"dl-translate translation failed: {e}, falling back to mock")
                    # Fall through to mock translation
            
            # Fallback to mock translation
            Logger.write_info(f"Mock translation: {source_lang} -> {target_lang}")

            if target_lang == 'ja':
                return f"[JA Translation] {text}"
            else:
                return f"[EN Translation] {text}"

        except Exception as e:
            Logger.write_error(f"Translation error: {e}")
            return text


translator_service = TranslatorService()
