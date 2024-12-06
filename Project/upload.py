import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from typing import List

# API Keys
PINECONE_API_KEY = "pcsk_hVSzM_3jRxgv7ABQ5LB1D9LotmRA9PYqqU9AjDBtZjz7cQ2fpKbcEaqQ3AvmWsFcxSZWk"
OPENAI_API_KEY = "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"

# Khởi tạo Pinecone và OpenAI
pc = Pinecone(api_key=PINECONE_API_KEY)

# Kết nối đến index đã tồn tại
index_name = "sample-movies"
# Kiểm tra xem index có tồn tại không và xóa nếu có
if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)
# Tạo mới nếu chưa tồn tại
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Đảm bảo dimension khớp với model embedding
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

# Kết nối đến index
index = pc.Index(index_name)

# Khởi tạo OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def read_file(file_path: str) -> str:
    # Đọc nội dung từ tệp văn bản
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def split_into_chunks(text: str) -> List[str]:
    # Chia văn bản thành các chunk nhỏ hơn dựa trên dấu phân tách '\n\n'.
    chunks = text.split('\n\n')
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    return chunks

def create_embedding(text: str) -> List[float]:
    # Tạo embedding cho văn bản sử dụng OpenAI
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def upload_to_pinecone(chunks: List[str], batch_size: int = 100):
    # Tải các chunk lên Pinecone theo từng batch nhỏ
    vectors = []
    for i, chunk in enumerate(chunks):
        vector = create_embedding(chunk)
        metadata = {
            "text": chunk,
        }
        vectors.append((f"chunk_{i}", vector, metadata))
        
        # Nếu đã đủ batch_size, thực hiện upsert và reset vectors
        if len(vectors) == batch_size:
            index.upsert(vectors)
            vectors = []  # Reset vectors để chuẩn bị cho batch tiếp theo

    # Nếu còn vectors chưa được upsert, thực hiện upsert cuối cùng
    if vectors:
        index.upsert(vectors)


file_path = 'retention-customer.txt'

# Đọc file
raw_text = read_file(file_path)

# Chia thành các chunk
chunks = split_into_chunks(raw_text)

# Upload lên Pinecone
upload_to_pinecone(chunks)

print(f"Đã xử lý và upload {len(chunks)} chunks lên Pinecone.")
