import google.generativeai as genai
from llm_handler import LLMHandler

class GeminiHandler(LLMHandler):
    def configure_api(self):
        """Cấu hình API Gemini"""
        genai.configure(api_key=self.api_key)

    def generate_strategy(self, reasons, augmented_context=None):
        """Sinh chiến lược sử dụng Gemini"""
        self.configure_api()

        if not reasons:
            return "Không có lý do nào được chọn. Vui lòng chọn ít nhất một lý do."

        prompt = self._prepare_prompt(reasons, augmented_context)

        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Đã xảy ra lỗi khi kết nối Gemini: {str(e)}"