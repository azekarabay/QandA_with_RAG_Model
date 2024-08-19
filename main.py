from rag_model import RAGModel

def main():
    rag = RAGModel("log_vectors.index", "log_data.npy")
    
    while True:
        query = input("Enter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        
        answer = rag.answer(query)
        print(f"\nAnswer: {answer}\n")

if __name__ == "__main__":
    main()