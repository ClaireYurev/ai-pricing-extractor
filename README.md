# PriceScraperAI

             ,----------------,              ,---------,
        ,-----------------------,          ,"        ,"|
      ,"                      ,"|        ,"        ,"  |
     +-----------------------+  |      ,"        ,"    |
     |  .-----------------.  |  |     +---------+      |
     |  |                 |  |  |     | -======-|      |
     |  | PriceScraperAI  |  |  |     |         |      |
     |  |  Fetching Data  |  |  |/----|     ---=|      |
     |  |                 |  |  |   ,/|==== ooo |      ;
     |  |                 |  |  |  // |    [486]|    ,"
     |  `-----------------'  |," .;'| |         |  ,"
     +-----------------------+  ;;  | |         |,"
        /_)______________(_/  //'   | +---------+
   ___________________________/___  `,
  /  oooooooooooooooo  .o.  oooo /,   \,"-----------
 / ==ooooooooooooooo==.o.  ooo= //   ,`           ,"
/_==__==========__==_ooo__ooo=_/'   /___________,"
`-----------------------------'

## Overview
PriceScraperAI is a Python tool designed to scrape pricing information from competitor websites, intelligently extract structured data using AI, and present the results in a clean, tabular format. It is built using modern libraries like Beautiful Soup, Firecrawl, Jina AI, and OpenAI's GPT API for robust data extraction and comparison.

## Features
- **Scraping**: Fetch data from multiple competitor websites.
- **AI-Powered Extraction**: Use OpenAI's GPT API to intelligently extract structured pricing data (plans, prices, features, etc.).
- **Flexible Preprocessing**: Automatically clean and preprocess scraped data for better results.
- **Easy Comparison**: Present data in a readable table format or save it as JSON for further analysis.

## Tech Stack
- **Python**
- **Beautiful Soup** - For static web scraping.
- **Firecrawl** - For advanced scraping of dynamic content.
- **Jina AI** - API-based scraping capabilities.
- **OpenAI GPT API** - For intelligent data extraction.
- **PrettyTable** - For tabular display of extracted data.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/PriceScraperAI.git
   cd PriceScraperAI

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Usage
   - Add your OpenAI and Mendable API keys.
   - Update the competitor_sites list with target websites and URLs.
   - Run the script:
   ```bash
   python main.py

4. Example Output
   Extracted Content Table
   ```lua
   +---------------+----------------+----------------------------------------------------+
   |      Site     | Provider Name  |                 Extracted Content                  |
   +---------------+----------------+----------------------------------------------------+
   | LeetCode      | Beautiful Soup | {"pricing_tiers": [{"plan": "Free", "price": ...} |
   | GeeksForGeeks | Jina AI        | {"pricing_tiers": [{"plan": "Student", "price...} |
   +---------------+----------------+----------------------------------------------------+

5. Customization
   - Modify the competitor_sites variable to target additional websites.
   - Adjust preprocess_content for content-specific truncation or cleaning.
