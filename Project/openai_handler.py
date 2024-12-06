import openai
from llm_handler import LLMHandler

class OpenAIHandler(LLMHandler):
    def configure_api(self):
        """Cấu hình API OpenAI"""
        self.client = openai.OpenAI(api_key=self.api_key)

    def generate_strategy(self, reasons, augmented_context=None):
        """Sinh chiến lược sử dụng OpenAI"""
        self.configure_api()

        if not reasons:
            return "Không có lý do nào được chọn. Vui lòng chọn ít nhất một lý do."

        prompt = self._prepare_prompt(reasons, augmented_context)

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Bạn là một chuyên gia tư vấn chiến lược khách hàng."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4096,
                temperature=0
            )
            return response.choices[0].message.content.strip()  # Lấy kết quả từ response
        except Exception as e:
            return f"Đã xảy ra lỗi khi kết nối OpenAI: {str(e)}"
