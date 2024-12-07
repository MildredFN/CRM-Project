import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from typing import List
from config import Config

# Khởi tạo Pinecone và OpenAI
pc = Pinecone(api_key=Config.PINECONE_API_KEY)

# Kết nối đến index đã tồn tại
index_name = Config.PINECONE_INDEX_NAME
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
            region='us-east-1'  # Có thể lấy từ Config nếu cần
        )
    )

# Kết nối đến index
index = pc.Index(index_name)

# Khởi tạo OpenAI client
openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)

def read_file(file_path: str) -> str:
    # Đọc nội dung từ tệp văn bản
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def split_into_chunks(text: str, separator: str = '\n\n', max_chunk_size: int = 1000) -> List[str]:
    # Chia văn bản thành các chunk dựa trên separator, đảm bảo không quá dài
    initial_chunks = text.split(separator)
    
    # Kiểm tra và chia nhỏ các chunk quá dài
    refined_chunks = []
    for chunk in initial_chunks:
        # Nếu chunk quá dài, chia nhỏ tiếp
        if len(chunk.split()) > max_chunk_size:
            words = chunk.split()
            while words:
                sub_chunk = words[:max_chunk_size]
                refined_chunks.append(' '.join(sub_chunk))
                words = words[max_chunk_size:]
        else:
            refined_chunks.append(chunk)
    
    # Loại bỏ các chunk trống
    refined_chunks = [chunk.strip() for chunk in refined_chunks if chunk.strip()]
    
    return refined_chunks

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

def main():
    file_path = 'retention-customer.txt'

    # Đọc file
    raw_text = read_file(file_path)

    # Chia thành các chunk
    chunks = split_into_chunks(raw_text)

    # Upload lên Pinecone
    upload_to_pinecone(chunks)

    print(f"Đã xử lý và upload {len(chunks)} chunks lên Pinecone.")

if __name__ == "__main__":
    # Kiểm tra và validate keys trước khi chạy
    Config.validate_keys()
    main()