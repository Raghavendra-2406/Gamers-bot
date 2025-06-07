
# Gamers bot

This script allows users to fetch the buy and sell prices of video games from three popular Indian game marketplaces: **GameNation, GameLoot, and CEX**.

## Features
- **Buy & Sell Prices**: Retrieve current buy and sell prices for a given game and platform.
- **Automated Web Scraping**: Uses Selenium and BeautifulSoup to scrape accurate pricing data.
- **Headless Browser Execution**: Ensures smooth operation without opening a browser window.

## Requirements
### Python Packages:
Make sure you have the following Python packages installed:

```bash
pip install selenium webdriver-manager beautifulsoup4 requests
```

### Browser Driver:
This script uses Google Chrome with ChromeDriver for Selenium-based scraping.

## Usage
Run the script and provide the necessary inputs:

```bash
python script.py
```

### User Inputs
You will be prompted for:

Game Name (e.g., "Elden Ring")

 Platform (e.g., "PS5", "PS4", "Xbox")

Mode (choose "buy", "sell", or "both")

### Example Output
```
 Prices for: Elden Ring PS5

 BUY PRICES:
  GameNation: ₹2,999
  GameLoot:   ₹2,799
  CEX:        ₹3,200

 SELL PRICES:
  GameNation: ₹1,500
  GameLoot:   ₹1,700
  CEX:        ₹1,600
```

## Supported Platforms
- PlayStation (PS4, PS5)
- Xbox (Xbox One, Xbox Series X|S)
- Nintendo Switch

## Dependencies & Modules
- selenium - Automates web interaction
- webdriver_manager - Manages browser drivers
- beautifulsoup4 - Parses HTML content
- requests - Fetches web pages
- urllib.parse - Handles URL encoding
- re - Processes text with regex
- time - Handles sleep delays

## Notes
- Since the script relies on web scraping, prices may change based on website updates.
- Use a stable internet connection for best results.
- Ensure that Google Chrome and ChromeDriver are installed and updated.
