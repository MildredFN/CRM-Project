from flask import Flask, render_template, request
from openai_handler import OpenAIHandler
from gemini_handler import GeminiHandler
from pinecone_handler import configure_pinecone, create_embedding, query_pinecone
from config import Config

# Khởi tạo các handler
openai_handler = OpenAIHandler(Config.OPENAI_API_KEY)
gemini_handler = GeminiHandler(Config.GEMINI_API_KEY)
pc = configure_pinecone(Config.PINECONE_API_KEY, Config.PINECONE_ENVIRONMENT)

app = Flask(__name__)

REASONS = [
    "Chất lượng dịch vụ kém, thái độ nhân viên không tốt",
    "Không có chương trình khách hàng thân thiết",
    "Quên cảm ơn khách hàng",
    "Trải nghiệm sử dụng sản phẩm không tốt",
    "Quy trình trả lại sản phẩm phức tạp",
    "Thiếu sự thấu hiểu nhu cầu của khách hàng",
    "Cạnh tranh gia tăng từ các thương hiệu khác",
    "Thiếu niềm tin, sự cam kết với khách hàng",
    "Không có mặt khi khách hàng cần",
    "Thiếu sự cải tiến",
    "Thiếu trải nghiệm cá nhân hóa"
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Lấy dữ liệu từ form
        selected_reasons = request.form.getlist("reasons")
        llm_choice = request.form.get("llm_choice", "openai")

        # Tăng cường truy vấn Pinecone
        augmented_context = ""
        for reason in selected_reasons:
            # Sử dụng Config.OPENAI_API_KEY
            embedding = create_embedding(reason)  # Không cần truyền API key
            
            # Sử dụng Config.PINECONE_INDEX_NAME
            pinecone_results = query_pinecone(query_embedding=embedding, top_k=4)  
            
            for match in pinecone_results["matches"]:
                augmented_context += f"{match['metadata']}: {reason}\n"

        # Chọn LLM handler
        if llm_choice == "gemini":
            strategy = gemini_handler.generate_strategy(selected_reasons, augmented_context)
        else:
            strategy = openai_handler.generate_strategy(selected_reasons, augmented_context)

        return render_template("index.html", reasons=REASONS, strategy=strategy, llm_choice=llm_choice)

    # Hiển thị trang ban đầu
    return render_template("index.html", reasons=REASONS, strategy=None)

if __name__ == "__main__":
    # Validate keys trước khi chạy ứng dụng
    Config.validate_keys()
    app.run(debug=True)