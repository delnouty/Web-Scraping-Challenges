import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# URL of the random quote page
url = "https://quotes.toscrape.com/random"

# Create a session to reuse TCP connections
session = requests.Session()

# Dictionary to store unique quotes
quotes_dict = {}

# Function to fetch a random quote
def get_random_quote():
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        quote = soup.find('span', class_='text').get_text()
        author = soup.find('small', class_='author').get_text()
        return quote, author
    return None, None

# Function to collect unique quotes concurrently
def collect_quotes_concurrently(target_count=100, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        # Keep submitting tasks as long as we haven't reached the target number of unique quotes
        while len(quotes_dict) < target_count:
            futures.append(executor.submit(get_random_quote))
            
            # Check results as tasks complete
            for future in as_completed(futures):
                quote, author = future.result()
                if quote and quote not in quotes_dict:
                    quotes_dict[quote] = author
                    print(f"Collected {len(quotes_dict)} unique quotes so far.")
                
                # Break out once we've reached the target number of quotes
                if len(quotes_dict) >= target_count:
                    break

# Start the timer
start_time = time.time()

# Collect quotes with 10 threads
collect_quotes_concurrently(target_count=100, max_workers=10)

# End the timer
end_time = time.time()
elapsed_time = end_time - start_time

print(f"Collected 100 unique quotes in {elapsed_time:.2f} seconds!")
