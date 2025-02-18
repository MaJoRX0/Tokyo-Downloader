import threading
import queue
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from lxml import etree
import typer
import inquirer
from datetime import datetime

links = []
dlinks = []
dlinks_queue = queue.Queue()  # Thread-safe queue for storing download links
HEADERS = ({
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
})

def convert_size(size_str):
    """Convert file size from MB/GB format to a float (in MB)."""
    size_str = size_str.upper().strip()
    if 'GB' in size_str:
        return float(size_str.replace('GB', '').strip()) * 1024  # Convert GB to MB
    elif 'MB' in size_str:
        return float(size_str.replace('MB', '').strip())
    return 0  # Default if no recognizable size format

def convert_date(date_str):
    """Convert date string from 'MM/DD/YY' to a sortable datetime object."""
    try:
        return datetime.strptime(date_str, "%m/%d/%y")  # Convert to datetime
    except ValueError:
        return datetime.min  # If date is invalid, return the oldest date possible

def save_links_to_file(links, filename="links.txt"):
    """Writes a list of links to a text file, each on a new line."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for link in links:
                file.write(link[0] + "\n")
        print(f"✅ Links successfully saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving links: {e}")

def process_link(choice, link):
    """Processes a single download link to extract the largest/latest download link."""
    try:
        #print(f"Processing: {link}")
        webpage = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        dom = etree.HTML(str(soup))
        c_h2_divs = dom.xpath('//div[@class="c_h2"]')

        if not c_h2_divs:
            return

        # Sort based on user's choice
        if choice == "Biggest Size":
            c_h2_divs.sort(key=lambda div: convert_size(div.xpath('.//b/text()')[1]) if len(div.xpath('.//b/text()')) > 1 else 0)
        elif choice == "Most Downloaded":
            c_h2_divs.sort(key=lambda div: int(div.xpath('.//b/text()')[2]) if len(div.xpath('.//b/text()')) > 2 else 0)
        else:
            c_h2_divs.sort(key=lambda div: convert_date(div.xpath('.//b/text()')[4]) if len(div.xpath('.//b/text()')) > 4 else datetime.min)

        # Extract best download link
        selected_div = c_h2_divs[-1]  # Get last element after sorting
        b_elements = selected_div.xpath('.//b/text()')
        download_link = selected_div.xpath('.//a/@href')[1]
        epn = link.split('/')[-1]
        dstatus = "Success"
        if "tokyoinsider" not in download_link: download_link = f"No valid link found EP: {epn}"; dstatus = "Faild no valid link"
        b_elements[0] = "EP: "+epn
        b_elements.append(dstatus)
        # Get the first valid download link

        print(b_elements)
        dlinks_queue.put([download_link,epn])  # Store in thread-safe queue

    except Exception as e:
        print(f"❌ Error processing {link}: {e}")

def fetch_download(choice, links):
    """Fetch downloads using multi-threading."""
    with ThreadPoolExecutor(max_workers=5) as executor:  # Use 5 threads
        executor.map(lambda link: process_link(choice, link), links)

    # Move queue data to the global list
    while not dlinks_queue.empty():
        dlinks.append(dlinks_queue.get())

    dlinks.sort(key=lambda li: int(li[1]))
    save_links_to_file(dlinks)  # Save to file after all threads complete

def okay(URL):
    """Extracts episode links from the main page."""
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))

    eps = dom.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "download-link", " " ))]')
    eps = [e for e in eps if "episode" in e.xpath('.//em/text()')]
    print(f"Anime name: {eps[3].text}")

    rangee = typer.prompt(f"{len(eps)} Episodes found select a range to download", default="1-10").split('-')

    for i in range(int(rangee[0]), int(rangee[1]) + 1):
        links.append("https://www.tokyoinsider.com" + eps[i * -1].xpath('./@href')[0])

    selected = inquirer.list_input("Select the download type",choices=["Biggest Size", "Most Downloaded", "Latest"])
    fetch_download(selected, links)  # Run multi-threaded download fetcher

def main(url: str = typer.Option('https://www.tokyoinsider.com/anime/B/Bleach_(TV)', prompt=True)):
    okay(url)

if __name__ == '__main__':
    typer.run(main)
