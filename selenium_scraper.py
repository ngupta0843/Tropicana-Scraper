from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from urllib.parse import urlparse

# constants
FILE_DIRECTORY = 'product_info'
OUTPUT_FILE = "tropicanaData.txt"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def normalize_url(url):
    parsed_url = urlparse(url)
    normalized = parsed_url._replace(fragment='').geturl().rstrip('/')
    return normalized

def fetch_links(url, visited):
    try:
        driver.get(url)
        time.sleep(5)
        elements = driver.find_elements(By.TAG_NAME, 'a')
        links = set()
        for element in elements:
            #Uncomment these lines for testing
            # if len(links) >= 5:
            #     break
            href = element.get_attribute('href')
            if href and href.startswith("http") and (href not in visited):
                normalized_url = normalize_url(href)
                parsed_url = urlparse(normalized_url)
                domain = parsed_url.netloc
                if domain == 'www.nakedjuice.com':
                    if normalized_url not in visited:
                        links.add(normalized_url)
        return links
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return set()

def recursive_link_fetch(url, visited):
    # change this line to: 'if url in visited or len(visited) >= 5:' for testing
    if url in visited:
        return set()
    print(f"Visiting {url}")
    save_to_file(OUTPUT_FILE, url)
    visited.add(url)
    links = fetch_links(url, visited)
    all_links = set(links)
    for link in links:
        #Uncomment these line for testing
        # if len(visited) >= 5:
        #     break
        all_links.update(recursive_link_fetch(link, visited))
    return all_links


def fetch_product_info(url):
    try:
        driver.get(url)
        time.sleep(3)
        product_info = driver.find_element(By.TAG_NAME, "body").text
        print(product_info)
        save_to_file(OUTPUT_FILE, product_info)
        return product_info
    except Exception as e:
        print(f"Failed to fetch or no product info on {url}: {e}")
        return None

def save_to_file(filename, content):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content + "\n")

def main():
    url = "https://www.nakedjuice.com/"
    visited = set()
    all_links = recursive_link_fetch(url, visited)

    if not os.path.exists('product_info'):
        os.mkdir('product_info')

    all_content = ""
    for link in all_links:
        #Uncomment these lines for testing
        # if len(all_content.split('\n')) >= 5:
        #     break
        product_info = fetch_product_info(link)
        if product_info:
            all_content += product_info + "\n"
        all_content += "------------------"
    
    # Write all collected contents to tropicanaData.txt
    save_to_file(OUTPUT_FILE, all_content)
    print(f"All data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
    driver.quit()
