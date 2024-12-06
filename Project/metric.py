import re
import json
from rouge_score import rouge_scorer

def clean_text(text):
    """Làm sạch văn bản ứng cử"""
    text = re.sub(r'\s+', ' ', text)  # Loại bỏ khoảng trắng thừa
    text = re.sub(r'[^\w\s]', '', text)  # Loại bỏ ký tự đặc biệt
    return text.lower().strip()

def read_txt_file(filepath):
    """Đọc nội dung file txt"""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def calculate_rouge_scores(reference_text, candidate_path):
    candidate_text = read_txt_file(candidate_path)
    cleaned_candidate = clean_text(candidate_text)
    
    # Tính ROUGE scores
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference_text, cleaned_candidate)
    
    return {
        'rouge1': scores['rouge1'].fmeasure,
        'rouge2': scores['rouge2'].fmeasure,
        'rougeL': scores['rougeL'].fmeasure
    }

def main():
    # Đọc văn bản tham chiếu
    reference_path = 'retention-customer.txt'
    reference_text = read_txt_file(reference_path)
    
    # Các file ứng cử
    candidate_paths = [
        'gemini-strategy.txt',
        'gpt-strategy.txt'
    ]
    
    # Tính ROUGE cho từng file ứng cử
    for candidate_path in candidate_paths:
        print(f"\nĐang xử lý file: {candidate_path}")
        rouge_scores = calculate_rouge_scores(reference_text, candidate_path)
        
        print("Kết quả ROUGE:")
        print(f"ROUGE-1: {rouge_scores['rouge1']:.4f}")
        print(f"ROUGE-2: {rouge_scores['rouge2']:.4f}")
        print(f"ROUGE-L: {rouge_scores['rougeL']:.4f}")

if __name__ == "__main__":
    main()