from bs4 import BeautifulSoup, NavigableString, Comment
import requests
import urllib.parse
import os
import re
import argparse

def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_links(soup, base_url):
    for link in soup.find_all('a'):  # find all link tags
        href = link.get('href')
        # if href attribute is not none, is a relative link, does not contain #, and does not start with mailto:
        if href and not urllib.parse.urlparse(href).netloc and '#' not in href and not href.startswith('mailto:'):
            yield urllib.parse.urljoin(base_url, href)

def save_text(url):
    soup = get_soup(url)
    # remove code, pre, and script tags
    for tag in soup.find_all(['code', 'pre', 'script']):
        tag.decompose()

    # Remove all comments
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

    text = soup.get_text('\n')  # get all the text from the page

    # post processing the text to ensure sentence completion at end of lines
    lines = text.split('\n')
    for i in range(len(lines)-1):
        line = lines[i].strip()
        if len(line.split()) < 2 or line[-1] not in '.!?':
            lines[i] = line + ' '

    text = '\n'.join(lines)

    filename = re.sub(r'\W+', '_', url) + '.txt'
    # ensure the directory exists
    if not os.path.exists('text_files'):
        os.makedirs('text_files')
    filepath = os.path.join('text_files', filename)  # join the directory with the filename
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Saved text from {url} to {filepath}")

def scrape_site(start_url, limit=100):
    visited = set()
    to_visit = {start_url}
    while to_visit and len(visited) < limit:
        current_url = to_visit.pop()
        save_text(current_url)
        visited.add(current_url)
        soup = get_soup(current_url)
        for link in get_links(soup, current_url):
            if link not in visited and len(visited) < limit:
                to_visit.add(link)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Web Scraper')
    parser.add_argument('start_url', type=str, help='the start URL to scrape')
    args = parser.parse_args()

    start_url = args.start_url
    scrape_site(start_url)

# Example of how to run the script:
# python scrape_url.py https://archive.pinecone.io/learn/langchain-intro
