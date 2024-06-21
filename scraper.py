import requests
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return BeautifulSoup(response.text, 'html.parser')

def extract_links(url):
    soup = get_soup(url)
    links = soup.find_all('a', href=True)  # Find all <a> tags with an href attribute
    urls = [link['href'] for link in links if 'http' in link['href']]  # Filter out and collect full URLs
    return urls

def scrape_text(url):
    soup = get_soup(url)
    text = soup.get_text(separator=' ', strip=True)
    return text

def main():
    start_url = 'https://www.nakedjuice.com/'
    links = extract_links(start_url)

    for url in links:
        try:
            text = scrape_text(url)
            filename = f"output_from_{url.split('//')[-1].split('/')[0]}.txt"
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"Saved text from {url} to {filename}")
        except requests.RequestException as e:
            print(f"Failed to scrape {url}: {e}")

    

if __name__ == "__main__":
    main()