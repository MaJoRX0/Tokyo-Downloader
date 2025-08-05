import threading
import queue
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from lxml import etree
import typer
import inquirer
from datetime import datetime

# Max number of threads to use for downloading
MAX_WORKERS = 5

dlinks_queue = queue.Queue()  # Thread-safe queue for storing download links
HEADERS = ({
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
})


def convert_size(size_str):
    # Convert file size from MB/GB format to a float (in MB).
    size_str = size_str.replace(",","").upper().strip()
    if 'GB' in size_str:
        return float(size_str.replace('GB', '').strip()) * 1024  # Convert GB to MB
    elif 'MB' in size_str:
        return float(size_str.replace('MB', '').strip())
    return 0  # Default if no recognizable size format


def convert_date(date_str):
    # Convert date string from 'MM/DD/YY' to a sortable datetime object.
    try:
        return datetime.strptime(date_str, "%m/%d/%y")  # Convert to datetime
    except ValueError:
        return datetime.min  # If date is invalid, return the oldest date possible


def save_links_to_file(links, filename="links.txt"):
    # Writes a list of links to a text file, each on a new line.
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for link in links:
                file.write(link[0] + "\n")
        print(f"✅ Links successfully saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving links: {e}")


def process_link(choice, providers:list, link):
    # Processes a single download link to extract the largest/latest download link.
    try:
        #print(f">>> processing: {link}")
        webpage = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        dom = etree.HTML(str(soup))
        c_h2_divs = dom.xpath('//div[contains(@class, "c_h2") or contains(@class, "c_h2b")]')

        if not c_h2_divs:
            return

        # Sort based on user's choice
        if choice == "Biggest Size":
            c_h2_divs.sort(
                key=lambda div: convert_size(div.xpath('.//b/text()')[1]) if len(div.xpath('.//b/text()')) > 1 else 0, reverse=True)
        elif choice == "Most Downloaded":
            c_h2_divs.sort(key=lambda div: int(div.xpath('.//b/text()')[2]) if len(div.xpath('.//b/text()')) > 2 else 0)
        else:
            c_h2_divs.sort(key=lambda div: convert_date(div.xpath('.//b/text()')[4]) if len(
                div.xpath('.//b/text()')) > 4 else datetime.min)

        # Extract best download link, using the providers list, if a link with the first provider is not found, fallback to the next one
        if providers:
            for provider in providers:
                for div in c_h2_divs:
                    link = div.xpath('.//a/@href')[1]
                    if provider in link:
                        selected_div = div
                        break
                else:
                    continue  # If no matching provider found, try next provider
                break  # Exit loop if a provider was found
            else:
                print(f">>> ❌ No matching provider found in {link}, picking according to choice")
                selected_div = c_h2_divs[0]  # Get first element after sorting
        else:
            selected_div = c_h2_divs[0]          
        
        b_elements = selected_div.xpath('.//b/text()')
        download_link = selected_div.xpath('.//a/@href')[1]            
        epn = link.split('/')[-1]
        type = link.split('/')[-2]
        dstatus = "Success"
        if "tokyoinsider" not in download_link: download_link = f"No valid link found {type}: {epn}"; dstatus = "Faild no valid link"
        b_elements[0] = type+ ": " + epn
        b_elements.append(dstatus)
        # Get the first valid download link

        print(f">>> {b_elements}")
        dlinks_queue.put([download_link, epn])  # Store in thread-safe queue

    except Exception as e:
        print(f">>> ❌ Error processing {link}: {e}")


def sort_key(item):
    # Custom sort key function for sorting download links.
    try:
        return int(item[1])
    except ValueError:
        # Return a very large number that sorts appropriately
        return float('inf')  # To put special episodes at the end

def fetch_download(choice, providers, links):
    # Fetch downloads using multi-threading.
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:  # Use 5 threads
        executor.map(lambda link: process_link(choice, providers, link), links)

    dlinks = []
    # Move queue data to the global list
    while not dlinks_queue.empty():
        dlinks.append(dlinks_queue.get())

    dlinks.sort(key=sort_key)
    save_links_to_file(dlinks)  # Save to file after all threads complete


def append_links(epsRange, episodes, links):
    for i in range(int(epsRange[0]), int(epsRange[1]) + 1):
        links.append("https://www.tokyoinsider.com" + episodes[i * -1].xpath('./@href')[0])


def okay(URL):
    print(">>> extracting links from main page...")
    # Extracts episode links from the main page.
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))

    allVideos = dom.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "download-link", " " ))]')

    types = {  # key: relative path; value: output string
        "episode": "Episodes",
        "ova": "OVAs",
        "special": "Specials",
        "movie": "Movies"
    }
    key_of_first_type = list(types.keys())[0]

    linkDict = {}

    for key, val in types.items():
        linkDict[key] = [e for e in allVideos if key in e.xpath('.//em/text()')]

    if (len(linkDict) > 0):
        print(f"Anime name:")
        print(f"> {linkDict[key_of_first_type][3].text.strip()} <")

    links = []

    for key in types.keys():
        val = linkDict[key]
        length = len(val)
        if (length > 0):
            input = typer.prompt(f"{length} {types[key]} found - select a range to download (0: None)",
                                 default=f"1-{length}")
            if (input != "0"):
                append_links(input.split('-'), val, links)

    selected = inquirer.list_input("Select the download type", choices=["Biggest Size", "Most Downloaded", "Latest"])
    # Prompt user to enter providers in order of preference
    providers_input = typer.prompt("Enter providers in order of preference, comma-separated\nexample: 'HorribleSubs, AnimeSakura'", default="AnimeSakura, HorribleSubs, Hatsuyuki")
    providers = [p.strip() for p in providers_input.split(',') if p.strip()]
    print(">>> fetching...")
    fetch_download(selected, providers, links)  # Run multi-threaded download fetcher


def main(url: str = typer.Option('https://www.tokyoinsider.com/anime/B/Bleach_(TV)', prompt=True)):
    okay(url)


if __name__ == '__main__':
    typer.run(main)
