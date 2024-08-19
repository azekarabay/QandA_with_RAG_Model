import re
from datetime import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

def parse_log_entry(entry):
    pattern = r'(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
    match = re.match(pattern, entry)
    if match:
        ip, timestamp, request, status, size, _, user_agent = match.groups()
        method, url, _ = request.split()
        return {
            'ip': ip,
            'timestamp': datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z"),
            'method': method,
            'url': url,
            'status': int(status),
            'size': int(size),
            'user_agent': user_agent
        }
    return None

def load_logs(file_path):
    with open(file_path, 'r') as f:
        return [parse_log_entry(line.strip()) for line in f if parse_log_entry(line.strip())]

def vectorize_logs(logs):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = [f"{log['method']} {log['url']} {log['status']} {log['user_agent']}" for log in logs]
    return model.encode(texts)

def create_faiss_index(vectors):
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)
    return index

if __name__ == "__main__":
    logs = load_logs("web_traffic.log")
    vectors = vectorize_logs(logs)
    index = create_faiss_index(vectors)
    
    faiss.write_index(index, "log_vectors.index")
    np.save("log_data.npy", logs)
    
    print(f"Processed {len(logs)} log entries. Vector index and data saved.")