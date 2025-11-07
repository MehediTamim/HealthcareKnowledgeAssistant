from app.utils.logger import Logger


class TranslatorService:
    @staticmethod
    def translate(text: str, source_lang: str, target_lang: str) -> str:
        try:
            if source_lang == target_lang:
                return text

            if not text or len(text.strip()) == 0:
                return text

            Logger.write_info(f"Mock translation: {source_lang} -> {target_lang}")

            if target_lang == 'ja':
                return f"[JA Translation] {text}"
            else:
                return f"[EN Translation] {text}"

        except Exception as e:
            Logger.write_error(f"Translation error: {e}")
            return text


translator_service = TranslatorService()
