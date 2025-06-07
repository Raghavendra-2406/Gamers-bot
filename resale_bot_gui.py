from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import time

# ------------------------ GameNation ------------------------
def get_gamenation_price(game, platform, mode="buy"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)

    search_term = f"{game} {platform}"
    search_url = f"https://gamenation.in/Search?term={urllib.parse.quote_plus(search_term)}"

    try:
        driver.get(search_url)
        first_product = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.product-card-1")))
        product_url = first_product.get_attribute("href")
        driver.get(product_url)

        if mode == "buy":
            try:
                buy_price = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-price strong span#ProductPrice"))
                ).text.strip()
            except Exception:
                buy_price = "Not found"
            return f"₹{buy_price}" if buy_price != "Not found" else buy_price

        elif mode == "sell":
            try:
                sell_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-sell")))
                sell_btn.click()
                time.sleep(1)
                sell_price_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn-cash span.btn-content"))
                )
                sell_price_text = sell_price_element.text.strip()
                match = re.search(r'₹\s*(\d+)', sell_price_text)
                sell_price = match.group(1) if match else "Not found"
            except Exception:
                sell_price = "Not found"
            return f"₹{sell_price}" if sell_price != "Not found" else sell_price

    except Exception:
        return "Not found"
    finally:
        driver.quit()

# ------------------------ GameLoot ------------------------
def slugify(game_name):
    stopwords = {'of'}
    game_name = game_name.lower()
    game_name = re.sub(r'[^a-z0-9\s]', '', game_name)
    words = game_name.split()
    filtered_words = [word for word in words if word not in stopwords]
    return '-'.join(filtered_words)

def get_gameloot_prices(game_name):
    slug = slugify(game_name)
    buy_url = f"https://gameloot.in/shop/{slug}-pre-owned/"
    sell_url = f"https://sell.gameloot.in/shop/{slug}/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res_buy = requests.get(buy_url, headers=headers, timeout=10)
        soup_buy = BeautifulSoup(res_buy.text, "html.parser")
        price_el = soup_buy.select_one(".pricebox ins span.amount")
        buy_price = "₹" + price_el.text.strip() if price_el else "Not found"
    except Exception:
        buy_price = "Not found"

    try:
        res_sell = requests.get(sell_url, headers=headers, timeout=10)
        soup_sell = BeautifulSoup(res_sell.text, "html.parser")
        sell_el = soup_sell.select_one("p.product_price span.amount")
        sell_price = "₹" + sell_el.text.strip() if sell_el else "Not found"
    except Exception:
        sell_price = "Not found"

    return buy_price, sell_price

# ------------------------ CEX ------------------------
def get_cex_sell_price(driver):
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.text-sm.md-text-base.w-100"))
        )
        price_elements = driver.find_elements(By.CSS_SELECTOR, "p.text-sm.md-text-base.w-100")
        for p in price_elements:
            spans = p.find_elements(By.TAG_NAME, "span")
            if len(spans) >= 2:
                label = spans[1].text.strip().lower()
                if "trade-in for cash" in label:
                    return spans[0].text.strip()
    except Exception:
        pass
    return "Not found"

def get_cex_price(game_name, platform, mode="buy"):
    query = f"{game_name} {platform}".replace(" ", "+")
    search_url = f"https://in.webuy.com/search?stext={query}"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    price = "Not found"
    try:
        driver.get(search_url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href^="/product-detail"]'))
        )
        first_product = driver.find_element(By.CSS_SELECTOR, 'a[href^="/product-detail"]')
        detail_url = first_product.get_attribute("href")
        driver.get(detail_url)

        if mode == "sell":
            price = get_cex_sell_price(driver)
        else:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.sell-price"))
            )
            price_element = driver.find_element(By.CSS_SELECTOR, "span.sell-price")
            price = price_element.text.strip() if price_element.text.strip() else "Not found"

    except TimeoutException:
        price = "Not found"
    except Exception:
        price = "Not found"
    finally:
        driver.quit()

    return price

# ------------------------ MAIN ------------------------
def main():
    game = input("🎮 Enter game name: ").strip()
    platform = input("🕹️ Enter platform (e.g., PS5, PS4): ").strip().upper()
    mode = input("💬 Type 'buy', 'sell', or 'both': ").strip().lower()

    full_game_name = f"{game} {platform}"
    print(f"\n📊 Prices for: {full_game_name}\n")

    if mode in ["buy", "both"]:
        print("💸 BUY PRICES:")
        print(f"  GameNation: {get_gamenation_price(game, platform, 'buy')}")
        print(f"  GameLoot:   {get_gameloot_prices(full_game_name)[0]}")
        print(f"  CEX:        {get_cex_price(game, platform, 'buy')}")

    if mode in ["sell", "both"]:
        print("\n💰 SELL PRICES:")
        print(f"  GameNation: {get_gamenation_price(game, platform, 'sell')}")
        print(f"  GameLoot:   {get_gameloot_prices(full_game_name)[1]}")
        print(f"  CEX:        {get_cex_price(game, platform, 'sell')}")

if __name__ == "__main__":
    main()
