import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'YOUR-API-HERE')
    
    # Gemini Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR-API-HERE')
    
    # Pinecone Configuration
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', 'YOUR-API-HERE')
    PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENV', 'us-east-1')
    PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME', 'default-index')

    # Additional method to validate keys (optional)
    @classmethod
    def validate_keys(cls):
        missing_keys = []
        if cls.OPENAI_API_KEY == 'YOUR-API-HERE':
            missing_keys.append('OpenAI API Key')
        if cls.GEMINI_API_KEY == 'YOUR-API-HERE':
            missing_keys.append('Gemini API Key')
        if cls.PINECONE_API_KEY == 'YOUR-API-HERE':
            missing_keys.append('Pinecone API Key')
        
        if missing_keys:
            raise ValueError(f"Missing API keys: {', '.join(missing_keys)}. Please set them in .env file.")

# Example .env file content:
# OPENAI_API_KEY=your_openai_api_key_here
# GEMINI_API_KEY=your_gemini_api_key_here
# PINECONE_API_KEY=your_pinecone_api_key_here
# PINECONE_ENV=us-east-1
# PINECONE_INDEX_NAME=your-index-name