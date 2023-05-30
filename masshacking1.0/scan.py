import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_domain(domain):
    url = f"https://{domain}/search?q=test"
    try:
        response = requests.get(url)
        if response.status_code == 200 and "text/html" in response.headers.get("Content-Type", ""):
            if "test" in response.text:
                print(url)
    except requests.RequestException:
        pass

def process_domains_file(file_path):
    with open(file_path, "r") as file:
        domains = file.read().splitlines()

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(process_domain, domain) for domain in domains]

        for future in as_completed(futures):
            future.result()

process_domains_file("domains.txt")
