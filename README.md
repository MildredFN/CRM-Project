# CRM-Project
# ⚓ Về AnchorAI
Phiên bản beta của AnchorAI giúp doanh nghiệp đề xuất chiến lược giữ chân khách hàng dựa trên 10 lý do rời bỏ phổ biến. Doanh nghiệp tự xác định lý do khách hàng rời bỏ rồi tick vào ô trống (có thể tick nhiều ô), dữ liệu sẽ được gửi lên AI có sử dụng kỹ thuật RAG (tạo sinh tăng cường bằng truy vấn) để sinh ra chiến lược giữ chân chính xác hơn.

*Lưu ý: AnchorAI vẫn đang trong quá trình thử nghiệm và các chiến lược do AI đề xuất là gợi ý. Dữ liệu chỉ là dữ liệu mẫu, không phải dữ liệu riêng của bất kì doanh nghiệp nào. Vì thế, hãy luôn kết hợp với kinh nghiệm và hiểu biết sâu sắc về doanh nghiệp của bạn. Nếu bạn muốn cá nhân hóa theo doanh nghiệp, hãy cung cấp dữ liệu từ doanh nghiệp của bạn lên cơ sở dữ liệu (xem mục Data Setup).*
## ⚠️ Lưu ý trước khi sử dụng:
Để dùng được AnchorAI, bạn phải tạo file .env với nội dung là các API key (của bạn) cũng như environment và index name trong pinecone tương ứng như dưới đây:
```bash
OPENAI_API_KEY= "your-openai-api"
GEMINI_API_KEY= "your-gemini-api"
PINECONE_API_KEY= "your-pinecone-api"
PINECONE_ENV= your-pinecone-env
PINECONE_INDEX_NAME= your-pinecone-indexname
```
# 📝 Data Setup 
Hiện tại, AnchorAi hỗ trợ lưu dữ liệu lên Pinecone (cơ sở dữ liệu vector). Dữ liệu sử dụng cho AnchorAI là dữ liệu thô, không gán nhãn (file txt). Mỗi chunk sẽ cách nhau bằng hai dấu cách dòng "\n". Trong tương lai, chúng tôi sẽ nghiên cứu cách lưu dữ liệu có gán nhãn để tăng độ chính xác cho các mô hình ngôn ngữ lớn. Dưới đây là cách tải dữ liệu lên Pinecone.

Bước 1: Lưu dữ liệu cho doanh nghiệp của bạn vào file retention-customer.txt (Lưu ý: dữ liệu có sẵn trong repo chỉ là dữ liệu mẫu)

Bước 2: Tạo tài khoản Pinecone cho riêng bạn bằng cách truy cập: https://www.pinecone.io/ (hoặc đăng nhập nếu bạn đã có tài khoản).

Bước 3: Lấy API key của Pinecone và lưu về.

Bước 4: Tạo index mới với dimension là 1536, metric: cosine

Bước 6: Chạy lệnh bên dưới để tiến hành tải dữ liệu lên Pinecone. Đừng quên setup file .env trước khi chạy nhé!

```bash
py upload.py
```
# 🚀 Khởi động AnchorAI
Sau khi tải dữ liệu lên và setup file .env gồm api của các mô hình ngôn ngữ lớn, hãy chạy lệnh dưới đây để khởi động AnchorAI:
```bash
py app.py
```
Và bạn có thể sử dụng như bình thường rồi.

# 📚 Tài liệu tham khảo
[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)


[What is a Vector Database & How Does it Work? Use Cases + Examples](https://www.pinecone.io/learn/vector-database/)

[UITeduQ: AUTOMATIC VIETNAMESE MULTIPLE-CHOICE QUESTION GENERATION WITH LLM AND RAG](https://drive.google.com/file/d/1soZnty_u0peNJyJ7dckWzFZCG_2669zk/view?usp=sharing)

