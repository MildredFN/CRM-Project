from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

openai_client = OpenAI(api_key="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")
# Cấu hình Pinecone
def configure_pinecone(api_key, environment):
    pc = Pinecone(api_key=api_key)
    return pc

# Hàm tạo embedding từ OpenAI
def create_embedding(text, api_key):
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding  # Sử dụng .data để truy cập dữ liệu

# Hàm tìm kiếm vector trong Pinecone
def query_pinecone(index_name, query_embedding, top_k= 4):
    pc = Pinecone(api_key="pcsk_hVSzM_3jRxgv7ABQ5LB1D9LotmRA9PYqqU9AjDBtZjz7cQ2fpKbcEaqQ3AvmWsFcxSZWk")
    index = pc.Index(index_name)
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    print("Kết quả truy vấn vector:")
    for match in results['matches']:
        print("\nVector ID:", match['id'])
        print("Độ tương đồng (Score):", match['score'])
        
        if 'metadata' in match:
            print("Metadata:")
            for key, value in match['metadata'].items():
                print(f"  {key}: {value}")
        
        print("Vector (một phần):", match['values'][:5], "...")
    
    return results