import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

def web_crawler(seed_urls, max_depth=2):
    visited = set()
    queue = deque([(seed_url, 0) for seed_url in seed_urls])

    while queue:
        current_url, depth = queue.popleft()

        if current_url not in visited and depth <= max_depth:
            try:
                response = requests.get(current_url)
                if response.status_code == 200:
                    # Parse the HTML content of the page
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Your code to process the page content goes here
                    # For example, printing the title of the page
                    title = soup.title.text if soup.title else "No Title"
                    print(f"Depth: {depth}, URL: {current_url}, Title: {title}")

                    # Mark the current URL as visited
                    visited.add(current_url)

                    # Enqueue links on the page for the next depth level
                    links = [link.get('href') for link in soup.find_all('a', href=True)]
                    for link in links:
                        absolute_url = urljoin(current_url, link)
                        queue.append((absolute_url, depth + 1))

            except Exception as e:
                print(f"Error accessing {current_url}: {e}")
if __name__ == "__main__":
    seed_urls = ["https://realpython.com/"]
    max_depth = 2
    web_crawler(seed_urls, max_depth)
