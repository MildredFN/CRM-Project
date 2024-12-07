from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from config import Config

# Khởi tạo OpenAI client với API key từ Config
openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Cấu hình Pinecone
def configure_pinecone(api_key, environment):
    pc = Pinecone(api_key=api_key)
    return pc

# Hàm tạo embedding từ OpenAI
def create_embedding(text, api_key=Config.OPENAI_API_KEY):
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding  # Sử dụng .data để truy cập dữ liệu

# Hàm tìm kiếm vector trong Pinecone
def query_pinecone(index_name=Config.PINECONE_INDEX_NAME, query_embedding=None, top_k=4):
    # Kiểm tra nếu không có embedding được truyền vào
    if query_embedding is None:
        raise ValueError("Phải cung cấp query_embedding")
    
    pc = Pinecone(api_key=Config.PINECONE_API_KEY)
    index = pc.Index(index_name)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    
    # In kết quả truy vấn (có thể bỏ qua nếu không muốn in ra)
    print("Kết quả truy vấn vector:")
    for match in results['matches']:
        print("\nVector ID:", match['id'])
        print("Độ tương đồng (Score):", match['score'])
        
        if 'metadata' in match:
            print("Metadata:")
            for key, value in match['metadata'].items():
                print(f"  {key}: {value}")
    
    return results