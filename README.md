Since im rarely on github you can contact me on discord if anything needed. Username: x5oc

# Tokyo Downloader
## 📌 Overview

Tokyo Downloader is a Python-based tool that fetches download links for anime episodes from **Tokyo Insider**. The extracted links are saved in a text file for easy bulk downloading using **Internet Download Manager (IDM)**.

## 🚀 Features

- Fetches anime episode download links automatically.
- Allows users to select a range of episodes.
- Supports sorting options:
  - **Biggest Size**: Selects the largest file.
  - **Most Downloaded**: Picks the most downloaded file.
  - **Latest**: Chooses the most recent file.
- Uses **multi-threading** for faster processing.
- Saves links in `links.txt` for IDM import.
- Available as both an **executable file** and an **open-source Python script**.

## 📥 Installation

You can either download the standalone executable (no installation required) or use the open-source Python version.

### Option 1: Download the Executable (No Installation Needed)

- Download the `.exe` version from [here](https://github.com/MaJoRX0/Tokyo-Downloader/releases).
- Run the executable file.
- Follow the on-screen prompts.

### Option 2: Use the Python Version

Ensure **Python 3.8+** is installed, then install dependencies:

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
2. Select the range of episodes to download.
3. Choose sorting criteria (**Biggest Size**, **Most Downloaded**, **Latest**).
4. The script fetches and saves links in `links.txt`.

### Example Output:

```sh
Url [https://www.tokyoinsider.com/anime/B/Bleach_(TV)]: https://www.tokyoinsider.com/anime/S/Solo_Leveling_(TV)
Anime name: Solo Leveling
19 Episodes found select a range to download [1-10]:
[?] Select the download type:
   Biggest Size
 > Most Downloaded
   Latest

['EP: 4', '360.25 MB', '138', 'rension23', '01/27/24', 'Success']
['EP: 5', '360.87 MB', '75', 'rension23', '02/03/24', 'Success']
✅ Links successfully saved to links.txt
```

## 📂 Importing Links into IDM

1. Open **Internet Download Manager (IDM)**.
2. Click **Tasks** (top-left menu) > **Import** > **From text file**.
3. Select `links.txt` and start downloading episodes in bulk!

## 📜 License

This script is for **educational purposes only**. Use responsibly and follow copyright laws.

## 🤝 Contributions

Feel free to report issues or suggest improvements!

