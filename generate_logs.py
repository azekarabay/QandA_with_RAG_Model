import random
from datetime import datetime, timedelta
import ipaddress

def generate_random_ip():
    return str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))

def generate_random_url():
    pages = ["/home", "/about", "/products", "/contact", "/blog", "/services"]
    return random.choice(pages)

def generate_random_status():
    return random.choice([200, 301, 404, 500])

def generate_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    ]
    return random.choice(user_agents)

def generate_log_entry():
    ip = generate_random_ip()
    timestamp = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%d/%b/%Y:%H:%M:%S +0000")
    method = random.choice(["GET", "POST"])
    url = generate_random_url()
    status = generate_random_status()
    size = random.randint(1000, 10000)
    user_agent = generate_random_user_agent()
    
    return f'{ip} - - [{timestamp}] "{method} {url} HTTP/1.1" {status} {size} "-" "{user_agent}"'

def generate_logs(num_entries):
    logs = [generate_log_entry() for _ in range(num_entries)]
    return "\n".join(logs)

if __name__ == "__main__":
    num_entries = 1000
    logs = generate_logs(num_entries)
    
    with open("web_traffic.log", "w") as f:
        f.write(logs)
    
    print(f"{num_entries} log entries have been generated and saved to web_traffic.log")