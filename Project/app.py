from flask import Flask, render_template, request
from openai_handler import OpenAIHandler
from gemini_handler import GeminiHandler
from pinecone_handler import configure_pinecone, create_embedding, query_pinecone
from pinecone import Pinecone, ServerlessSpec

# Cấu hình API keys
OPENAI_API_KEY = "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"
GEMINI_API_KEY = "AIzaSyDYANoBNurD4dYGNksIFTh2UhQsgkYgnAM"
PINECONE_API_KEY = "pcsk_hVSzM_3jRxgv7ABQ5LB1D9LotmRA9PYqqU9AjDBtZjz7cQ2fpKbcEaqQ3AvmWsFcxSZWk"
PINECONE_ENV = "us-east-1"
INDEX_NAME = "sample-movies"

# Khởi tạo các handler
openai_handler = OpenAIHandler(OPENAI_API_KEY)
gemini_handler = GeminiHandler(GEMINI_API_KEY)

pc = configure_pinecone(PINECONE_API_KEY, PINECONE_ENV)

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
            embedding = create_embedding(reason, OPENAI_API_KEY)  # Tạo embedding từ lý do
            pinecone_results = query_pinecone(INDEX_NAME, embedding, top_k=4)  # Thực hiện truy vấn
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
    app.run(debug=True)