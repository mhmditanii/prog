from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import csv
import sys

url = ""
json_file_name = "news_scrapped.json"
csv_file_name = "news_scrapped_csv.csv" 
driver = None  # Global driver

def open_website():
    global url
    global driver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //a"))
    )

def scrape_headlines():
    global driver
    scroll_pause_time = 1
    prev_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(20):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        cur_height = driver.execute_script("return document.body.scrollHeight")
        if cur_height == prev_height:
            break
        prev_height = cur_height

    elements = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //a")
    if not elements:
        elements = driver.find_elements(By.CSS_SELECTOR, "h2.media__headline a")
    
    headlines = []
    for elem in elements:
        try:
            text = elem.text.strip()
            if text and len(text.split()) > 5 and not text.isupper() and text not in headlines:
                headlines.append(text)
        except:
            continue
    driver.quit()
    return headlines

def search_website_for_keywords(keywords):
    global driver
    scroll_pause_time = 1
    prev_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(20):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        cur_height = driver.execute_script("return document.body.scrollHeight")
        if cur_height == prev_height:
            break
        prev_height = cur_height

    elements = driver.find_elements(By.XPATH, "//h1 | //h2 | //h3 | //h4 | //h5 | //a")
    if not elements:
        elements = driver.find_elements(By.CSS_SELECTOR, "h2.media__headline a")

    matched = []
    for elem in elements:
        try:
            text = elem.text.strip()
            if (
                text
                and len(text.split()) > 5
                and not text.isupper()
                and any(keyword.lower() in text.lower() for keyword in keywords)
                and text not in matched
            ):
                matched.append(text)
        except:
            continue
    driver.quit()
    return matched

def save_results_json(data):
    try:
        with open(json_file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except:
        print("Unexpected error:", sys.exc_info()[0])

def save_results_csv(headlines):
    try:
        with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            writer.writerow(["Headline"])
            for headline in headlines:
                writer.writerow([headline])
        print(f"Exported {len(headlines)} headlines to {filename}")
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except Exception as e:
        print("Unexpected error:", e)
