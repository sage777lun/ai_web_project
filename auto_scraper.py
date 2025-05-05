import requests
from bs4 import BeautifulSoup
import json
import concurrent.futures
import time

def fetch_dialogues(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ 無法訪問網站：{url}, 錯誤訊息：{e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    dialogues = [p.text.strip() for p in soup.find_all("p") if p.text.strip()]

    # **過濾無用內容**
    filtered_dialogues = [d for d in dialogues if len(d.split()) > 5 and "cookie" not in d.lower()]

    return filtered_dialogues

def auto_update_training_data():
    urls = [
        "https://www.reddit.com/r/technology",
        "https://news.ycombinator.com/",
        "https://www.quora.com/",
        "https://www.producthunt.com/"
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_dialogues, urls))

    all_dialogues = [d for res in results for d in res]

    if not all_dialogues:
        print("❌ 沒有找到新數據，請更換來源！")
        return

    try:
        with open("dialogue_data.json", "r", encoding="utf-8") as file:
            existing_data = json.load(file)
        existing_inputs = {entry["input"] for entry in existing_data}
    except FileNotFoundError:
        existing_inputs = set()

    new_entries = [{"input": d, "output": "這是一條新的訓練數據"} for d in all_dialogues if d not in existing_inputs]
    existing_data.extend(new_entries)

    with open("dialogue_data.json", "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

    print(f"✅ 訓練數據已更新，共新增 {len(new_entries)} 條對話！")

while True:
    auto_update_training_data()
    time.sleep(600)  # **每 10 分鐘爬取一次**