from typing import List, Dict, Any
from prettytable import PrettyTable, ALL  # Use ALL constant instead of enums
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import json
import getpass
import firecrawl


# Initialize OpenAI client with a dynamic API key
openai_api_key = getpass.getpass("Enter your OpenAI API Key: ")
client = OpenAI(api_key=openai_api_key)

# Initialize Firecrawl API
FIRECRAWL_API_KEY = getpass.getpass("Enter your Firecrawl API Key: ")

# Competitor sites
competitor_sites = [
    {"name": "NeetCode", "url": "https://neetcode.io/pro"},
    {"name": "GeeksForGeeks", "url": "https://www.geeksforgeeks.org/geeksforgeeks-premium-subscription"},
    {"name": "LeetCode", "url": "https://leetcode.com/subscribe/"},
    {"name": "HackerRank", "url": "https://www.hackerrank.com/work/pricing"}
]

# Token counting and cost calculation
import tiktoken

def count_tokens(input_string: str) -> int:
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(input_string)
    return len(tokens)

def calculate_cost(input_string: str, cost_per_million_tokens: float = 5) -> float:
    num_tokens = count_tokens(input_string)
    total_cost = (num_tokens / 1_000_000) * cost_per_million_tokens
    return total_cost

# Scrapers
def beautiful_soup_scrape_url(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return str(soup)

def scrape_jina_ai(url: str) -> str:
    response = requests.get(f"https://r.jina.ai/{url}")
    return response.text

def scrape_firecrawl(url: str) -> str:
    app = firecrawl.FirecrawlApp(api_key=FIRECRAWL_API_KEY)
    return app.scrape_url(url).get("markdown", "")

list_of_scraper_functions = [
    {"name": "Beautiful Soup", "function": beautiful_soup_scrape_url},
    {"name": "Firecrawl", "function": scrape_firecrawl},
    {"name": "Jina AI", "function": scrape_jina_ai}
]

# Preprocessing and helpers
def preprocess_content(content: str, max_length: int = 2000) -> str:
    return content[:max_length]

def format_json(content: str) -> str:
    try:
        return json.dumps(json.loads(content), indent=2)
    except json.JSONDecodeError:
        return content

def truncate_message(message: str, max_length: int = 100) -> str:
    return message if len(message) <= max_length else message[:max_length] + "..."

# Extraction
def extract(content: str) -> str:
    if not content.strip():
        return "No relevant content to process."
    try:
        messages = [
            {"role": "system", "content": "Extract all pricing tiers from this content. For each tier, include the name, price, billing cycle (e.g., monthly, yearly), and features (if available). Return the result as a JSON array."},
            {"role": "user", "content": preprocess_content(content)}
        ]
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Parallel processing for scraping and extraction
def process_site(site: Dict[str, str], scraper: Dict[str, Any]) -> Dict[str, Any]:
    try:
        content = scraper["function"](site["url"])
        extracted = extract(content)
        formatted = format_json(extracted)
        return {"provider": site["name"], "scraper": scraper["name"], "content": formatted}
    except Exception as e:
        return {"provider": site["name"], "scraper": scraper["name"], "content": f"Error: {str(e)}"}

# Display results in a table
def display_extracted_content(results: List[Dict[str, Any]], max_results: int = 10):
    table = PrettyTable()
    table.field_names = ["Site", "Provider Name", "Extracted Content"]
    for result in tqdm(results[:max_results], desc="Processing results"):
        table.add_row([
            result["provider"],
            result["scraper"],
            truncate_message(result["content"], max_length=500)
        ])
    table.max_width = 50
    table.hrules = ALL  # Use ALL constant for horizontal rules
    print("Extracted Content Table:")
    print(table)

# Run scrapers and extract content
results = []
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(process_site, site, scraper)
        for site in competitor_sites
        for scraper in list_of_scraper_functions
    ]
    for future in as_completed(futures):
        results.append(future.result())

# Display results
display_extracted_content(results, max_results=12)
