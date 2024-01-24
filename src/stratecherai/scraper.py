import requests
from bs4 import BeautifulSoup

import pdb

# URL of the page to scrape
URL_PREFIX = "https://stratechery.com/category/articles/page/"
# URL_PREFIX = "https://stratechery.com/2024/the-apple-vision-pros-missing-apps/"
TARGET_DOMAIN = "https://stratechery.com"


def get_stratechery_article_links(
    url: str = URL_PREFIX, domain: str = TARGET_DOMAIN
) -> list[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    anchor_tags = soup.find_all("a")
    return [
        tag.get("href")
        for tag in anchor_tags
        if tag.get("href").startswith(domain)
        and tag.get("href")[len(domain) :].startswith("/20")
    ]


def get_stratechery_article_body(url: str) -> list[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    content_divs = soup.find_all("div", class_="entry-content")
    parsed_content = []
    for div in content_divs:
        paragraphs = div.find_all("p")
        for paragraph in paragraphs:
            to_add = paragraph.get_text(" ", strip=True)
            if "footnote" in to_add:
                continue
            parsed_content.append(to_add)
    return parsed_content


print(get_stratechery_article_links())

print(get_stratechery_article_body(get_stratechery_article_links()[0]))
