import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from collections import Counter

class RAGModel:
    def __init__(self, index_path, data_path):
        self.index = faiss.read_index(index_path)
        self.logs = np.load(data_path, allow_pickle=True)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
    
    def retrieve(self, query, k=50):
        query_vector = self.encoder.encode([query])
        _, I = self.index.search(query_vector, k)
        return [self.logs[i] for i in I[0]]
    
    def analyze_logs(self, logs):
        url_counter = Counter(log['url'] for log in logs)
        method_counter = Counter(log['method'] for log in logs)
        status_counter = Counter(log['status'] for log in logs)
        
        total_logs = len(logs)
        top_urls = url_counter.most_common(10)
        top_methods = method_counter.most_common(5)
        top_status_codes = status_counter.most_common(5)
        
        return {
            'total_logs': total_logs,
            'top_urls': top_urls,
            'top_methods': top_methods,
            'top_status_codes': top_status_codes
        }

    def generate(self, query, log_analysis):
        context = f"""
Web traffic log analysis:
- Total logs analyzed: {log_analysis['total_logs']}
- Top 10 URLs accessed:
{chr(10).join([f"  {url}: {count} times" for url, count in log_analysis['top_urls']])}
- Top HTTP methods:
{chr(10).join([f"  {method}: {count} times" for method, count in log_analysis['top_methods']])}
- Top status codes:
{chr(10).join([f"  {status}: {count} times" for status, count in log_analysis['top_status_codes']])}

Based on this analysis, please answer the following question: {query}

Provide a detailed and informative answer. Focus on addressing the specific question asked. Include relevant statistics and insights from the log analysis. If the question cannot be fully answered with the given information, explain what can be determined and what additional information might be needed.
"""

        input_ids = self.tokenizer(context, return_tensors="pt").input_ids
        outputs = self.model.generate(
            input_ids, 
            max_length=700, 
            num_return_sequences=1, 
            do_sample=True, 
            temperature=0.7,
            top_k=50,
            top_p=0.95
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    def answer(self, query):
        retrieved_logs = self.retrieve(query)
        log_analysis = self.analyze_logs(retrieved_logs)
        return self.generate(query, log_analysis)

if __name__ == "__main__":
    rag = RAGModel("log_vectors.index", "log_data.npy")
    query = "What are the most common URLs accessed?"
    answer = rag.answer(query)
    print(f"Query: {query}")
    print(f"Answer: {answer}")