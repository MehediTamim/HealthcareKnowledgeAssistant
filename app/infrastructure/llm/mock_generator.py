from typing import List, Dict
from app.utils.logger import Logger


class MockLLMGenerator:
    def generate(self, query: str, context_docs: List[Dict], language: str) -> str:
        try:
            if not context_docs:
                return self.generate_no_results_response(language)

            if language == 'ja':
                return self._generate_japanese(query, context_docs)
            else:
                return self._generate_english(query, context_docs)

        except Exception as e:
            Logger.write_error(f"Error generating response: {e}")
            return self._error_response(language)

    def _generate_english(self, query: str, context_docs: List[Dict]) -> str:
        context_text = self._format_context(context_docs, 'en')

        response = "Based on the medical guidelines and research documents, here is the information regarding your question:\n\n"
        response += f"**Query:** {query}\n\n"
        response += "**Answer:**\n\n"
        response += context_text
        response += "\n\n**Summary:**\n"
        response += f"The information above is extracted from {len(context_docs)} relevant document(s). "
        response += "The key recommendations and findings are presented based on the latest medical guidelines. "
        response += "Please consult with healthcare professionals for personalized medical advice.\n\n"
        response += "**Sources:**\n"

        for i, doc in enumerate(context_docs, 1):
            doc_id = doc.get('document_id', 'unknown')
            chunk_id = doc.get('chunk_id', 0)
            response += f"{i}. Document: {doc_id}, Section: {chunk_id}\n"

        return response

    def _generate_japanese(self, query: str, context_docs: List[Dict]) -> str:
        context_text = self._format_context(context_docs, 'ja')

        response = "医療ガイドラインおよび研究文書に基づいて、ご質問に関する情報を以下に示します：\n\n"
        response += f"**質問:** {query}\n\n"
        response += "**回答:**\n\n"
        response += context_text
        response += "\n\n**要約:**\n"
        response += f"上記の情報は、{len(context_docs)}件の関連文書から抽出されたものです。"
        response += "最新の医療ガイドラインに基づく主要な推奨事項と所見が提示されています。"
        response += "個別の医療アドバイスについては、医療専門家にご相談ください。\n\n"
        response += "**出典:**\n"

        for i, doc in enumerate(context_docs, 1):
            doc_id = doc.get('document_id', 'unknown')
            chunk_id = doc.get('chunk_id', 0)
            response += f"{i}. 文書: {doc_id}, セクション: {chunk_id}\n"

        return response

    def _format_context(self, context_docs: List[Dict], language: str) -> str:
        formatted = ""

        for i, doc in enumerate(context_docs, 1):
            content = doc.get('content', '')
            doc_id = doc.get('document_id', 'unknown')

            if language == 'ja':
                formatted += f"【文書 {i}】({doc_id})\n"
            else:
                formatted += f"[Document {i}] ({doc_id})\n"

            formatted += f"{content}\n\n"

        return formatted

    def generate_no_results_response(self, language: str) -> str:
        if language == 'ja':
            return "申し訳ございませんが、ご質問に関連する情報が見つかりませんでした。別の質問をお試しいただくか、医療専門家にご相談ください。"
        else:
            return "I apologize, but I couldn't find relevant information to answer your question. Please try rephrasing your query or consult with a healthcare professional."

    def _error_response(self, language: str) -> str:
        if language == 'ja':
            return "申し訳ございません。回答の生成中にエラーが発生しました。もう一度お試しください。"
        else:
            return "I apologize, but an error occurred while generating the response. Please try again."


mock_llm_generator = MockLLMGenerator()
