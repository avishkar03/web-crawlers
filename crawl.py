import requests
import pymongo
import nltk

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')

from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

seed_links = [
    {"url": "https://en.wikipedia.org/wiki/Python_(programming_language)", "depth": 1, "rank": 5},
    {"url": "https://realpython.com/", "depth": 1, "rank": 5},
    {"url": "https://docs.python.org/3/", "depth": 1, "rank": 5},
]

nltk_stopwords = set(stopwords.words("english"))

def extract_keywords(text):
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]
    keywords = [word for word in words if word not in nltk_stopwords]
    keyword_counter = Counter(keywords)
    return [keyword for keyword, count in keyword_counter.most_common(5)]

def crawl(url, depth, rank, web_pages):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error accessing {url}: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.text if soup.title else "No Title"
    text = ' '.join(p.get_text() for p in soup.find_all('p'))
    keywords = extract_keywords(text)

    web_pages.insert_one({
        "url": url,
        "depth": depth,
        "rank": rank,
        "title": title,
        "text": text,
        "keywords": keywords
    })

    print(f"Crawled: {url}, Depth: {depth}, Rank: {rank}, Title: {title}")

def main():
    client = pymongo.MongoClient("mongodb+srv://avishkarmore2:avishkar@cluster0.5jbn5xc.mongodb.net/?retryWrites=true&w=majority")
    db = client["web_crawler"]
    web_pages = db["web_pages"]

    for seed_link in seed_links:
        crawl(seed_link["url"], seed_link["depth"], seed_link["rank"], web_pages)

    print("Crawling and data extraction completed successfully.")

if __name__ == "__main__":
    main()
