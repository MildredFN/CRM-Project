from abc import ABC, abstractmethod

class LLMHandler(ABC):
    def __init__(self, api_key):
        self.api_key = api_key

    @abstractmethod
    def configure_api(self):
        """Cấu hình API cho từng LLM"""
        pass

    @abstractmethod
    def generate_strategy(self, reasons, augmented_context=None):
        """Sinh chiến lược chung cho các LLM"""
        pass

    def _prepare_prompt(self, reasons, augmented_context=None):
        """Chuẩn bị prompt chung"""
        content = "\n".join(f"- {reason}" for reason in reasons)
        
        prompt = f"""
        Hãy tạo một chiến lược giữ chân khách hàng sáng tạo và cá nhân hóa dựa trên lý do sau:

        Lý do rời bỏ khách hàng: 
        {content}

        {"Dữ liệu bổ sung: " + augmented_context if augmented_context else ""}

        Yêu cầu:
        1. Đề xuất chiến lược phải chia thành các bước cụ thể.
        2. Mỗi bước cần dễ thực hiện và trực tiếp giải quyết lý do rời bỏ.
        3. Sử dụng giọng văn chuyên nghiệp, nhưng thân thiện và dễ tiếp cận.
        4. Gợi ý kênh thực hiện (email, mạng xã hội, ứng dụng, v.v.) cho từng bước.
        5. Nếu có thể, cung cấp ví dụ minh họa thực tế từ các case study nổi tiếng.
        6. Hãy viết bình thường, không sử dụng ngôn ngữ markdown. (Don't use markdown language)
        7. Không ghi ý gạch đầu dòng. (No bullets) GHI THÀNH ĐOẠN VĂN
        8. Chỉ sử dụng content có sẵn, không tự ý chế thêm.
        9. Chỉ rõ điều người dùng cần tập trung giải quyết trong tiêu đề chiến lược.

        Ví dụ format:
        Tiêu đề chiến lược
        Bước 1: (Tiêu đề bước)
        (Mô tả chi tiết)
        (Gợi ý kênh thực hiện)
        Bước 2: (Tiêu đề bước)
        (Mô tả chi tiết)
        (Gợi ý kênh thực hiện)
        Bước 3: (Tiêu đề bước)
        (Mô tả chi tiết)
        (Gợi ý kênh thực hiện)
        ...
        Case study nổi tiếng: (mô tả case study chi tiết)

        """
        return prompt