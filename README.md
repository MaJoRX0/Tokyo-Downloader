Since im rarely on github you can contact me on discord if anything needed. Username: x5oc

# Tokyo Downloader
## 📌 Overview

Tokyo Downloader is a Python-based tool that fetches download links for anime Episodes/OVAs/Movies/Specials from **Tokyo Insider**. The extracted links are saved in a text file for easy bulk downloading using any download manager such as **Internet Download Manager (IDM)**, **wget**, and **yt-dlp**.

## 🚀 Features

- Fetches Episode/OVA/Movies/Special episode download links automatically.
- Allows users to select a range of episodes.
- Supports sorting options:
  - **Biggest Size**: Selects the largest file.
  - **Most Downloaded**: Picks the most downloaded file.
  - **Latest**: Chooses the most recent file.
- Uses **multi-threading** for faster processing.
- Saves links as a linebreak separated list in `links.txt` for use with download managers (e.g. IDM).
- Available as both an **executable file** and an **open-source Python script**.

## 📥 Installation

You can either download the standalone executable (no installation required) or use the open-source Python version.

### Option 1: Download the Executable for Windows (No Installation Needed)

- Download the `.exe` version from [here](https://github.com/MaJoRX0/Tokyo-Downloader/releases).
- Run the executable file.
- Follow the on-screen prompts.

### Option 2: Use the Python Version (Supports Windows and Linux)

Ensure **Python 3.8+** is installed, then create and activate a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Run the script with:

```sh
python main.py
```

## 🔧 Usage

### Steps:

1. Enter the anime URL (e.g., *Solo Leveling* page on Tokyo Insider).
2. Select the range of episodes/OVAs/movies/speiclas (0 For none) to download. It is required to input a range (ie. `1-1`) if not `0`.
3. Choose sorting criteria (**Biggest Size**, **Most Downloaded**, **Latest**).
4. The script fetches and saves links in `links.txt`.

### Example Output:

```sh
Url [https://www.tokyoinsider.com/anime/B/Bleach_(TV)]:
>>> extracting links from main page...
Anime name:
> Bleach <
406 Episodes found - select a range to download (0: None) [1-406]: 1-2
3 OVAs found - select a range to download (0: None) [1-3]: 1-3
6 Specials found - select a range to download (0: None) [1-6]: 0
4 Movies found - select a range to download (0: None) [1-4]: 1-1
[?] Select the download type:
   Biggest Size
 > Most Downloaded
   Latest

>>> fetching...
>>> ['ova: 10', '14.10 MB', '473', 'bleachfanclarkey', '02/11/12', 'Success']
>>> ['ova: 2', '200.02 MB', '382', 'sifsif', '09/13/11', 'Success']
>>> ['ova: 1', '198.00 MB', '318', 'sifsif', '09/20/11', 'Success']
>>> ['movie: 1', '598.49 MB', '806', 'andrai', '11/15/10', 'Success']
>>> ['episode: 2', '175.39 MB', '4409', 'Anonymous', '05/03/10', 'Faild no valid link']
>>> ['episode: 1', '130.82 MB', '11457', 'Anonymous', '05/03/10', 'Success']
✅ Links successfully saved to links.txt
```

## 📂 Downloading Episodes from Links

### IDM

1. Open **Internet Download Manager (IDM)**.
2. Click **Tasks** (top-left menu) > **Import** > **From text file**.
3. Select `links.txt` and start downloading episodes in bulk!

### wget and yt-dlp

While in the same folder as the `links.txt`, run the command for your preferred tool:

```sh
wget --read-timeout 60 -i links.txt
```

```sh
yt-dlp -a links.txt
```

If you chose to use custom names for the files, use one of the scripts in `download-scripts` instead.

It is suggested to move the `links.txt` into the folder you want the videos to be downloaded to before running the command.

## 📜 License

This script is for **educational purposes only**. Use responsibly and follow copyright laws.

## 🤝 Contributions

Feel free to report issues or suggest improvements!

