# Web Traffic Log Analysis with RAG Model

This project implements a Retrieval-Augmented Generation (RAG) model for analyzing web traffic logs. It includes components for generating synthetic log data, processing logs, and creating a question-answering system based on the log analysis.

## Features

- Generate synthetic web traffic log data
- Process and vectorize log entries
- Create a FAISS index for efficient similarity search
- Implement a RAG model for answering questions about log data
- Interactive command-line interface for querying the model

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/web-traffic-log-analysis.git
cd web-traffic-log-analysis
pip install -r requirements.txt
```

## Usage
1. Generate synthetic log data:
 
```bash
python generate_log.py
```

This will create a web_traffic.log file with 1000 random log entries.

2. Process the logs and create the FAISS index:
   
```bash
python process_logs.py
```
This step will create log_vectors.index and log_data.npy files.

3. Run the main program to interact with the RAG model:
   
```bash
python main.py
```
You can then enter questions about the log data, and the model will provide answers based on its analysis.

## Components
- generate_log.py:
This script generates synthetic web traffic log data. It creates random IP addresses, timestamps, HTTP methods, URLs, status codes, and user agents to simulate realistic web server logs.

- process_logs.py:
This script processes the generated log file. It parses each log entry, vectorizes the log data using a sentence transformer model, and creates a FAISS index for efficient similarity search.

- rag_model.py:
This file implements the RAG (Retrieval-Augmented Generation) model. It combines:


    - A FAISS index for retrieving relevant log entries

    - A log analysis component to generate statistics about the retrieved logs

    - A language model (FLAN-T5) to generate human-readable answers based on the log analysis

- main.py
The main script that provides an interactive interface for users to ask questions about the log data. It uses the RAG model to retrieve relevant information and generate answers.

## How it Works
1. The system first retrieves relevant log entries based on the user's query using FAISS.
2. It then analyzes these logs to generate statistics like most common URLs, HTTP methods, and status codes.
3. The analysis is combined with the user's query and fed into a language model.
4. The language model generates a human-readable answer based on the log analysis and the query.

## Customization
You can customize various aspects of the system:

- Modify generate_log.py to change the characteristics of the synthetic log data.

- Adjust the number of retrieved logs or the analysis metrics in rag_model.py.

- Experiment with different pre-trained models for encoding or generation in rag_model.py.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
