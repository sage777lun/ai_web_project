from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time

def login_and_fetch_dialogues(url, login_url=None, username=None, password=None):
    """如果需要登入，則先登入，然後爬取對話內容"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 隱藏瀏覽器窗口，提高效率
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # **如果需要登入，則先執行登入**
    if login_url and username and password:
        driver.get(login_url)
        time.sleep(3)  # 等待登入頁面加載

        # **模擬登入（根據實際網頁 ID 調整）**
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(5)  # 等待登入完成

    # **爬取目標頁面**
    driver.get(url)
    time.sleep(10)  # 確保 JavaScript 完全載入

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()  # 關閉瀏覽器，釋放資源

    # **解析 HTML，確保 UTF-8 編碼**
    soup_text = soup.get_text()
    soup_text = soup_text.encode("utf-8", errors="ignore").decode("utf-8")  # 修正編碼錯誤

    # **提取所有 <p> 標籤的對話**
    dialogues = [p.text.strip() for p in soup.find_all("p") if p.text.strip()]

    if not dialogues:
        print("❌ 沒有找到對話內容，可能需要更改爬取策略！")
        return

    # **存入 JSON 訓練數據**
    training_data = [{"text": d, "keywords": d.split(), "sentiment": "中立"} for d in dialogues]

    with open("training_data.json", "w", encoding="utf-8") as file:
        json.dump(training_data, file, ensure_ascii=False, indent=4)

    print("✅ AI 訓練數據已成功更新！")
    print("🔎 抓取的前 5 條對話內容：", dialogues[:5])  # 顯示前 5 條結果，確認抓取是否成功

# **測試爬取對話（如果不需要登入，直接設定 URL 即可）**
login_and_fetch_dialogues(
    url="https://example-site.com/chat",
    login_url="https://example-site.com/login",  # 如果不需要登入，設為 None
    username="your_username",  # 填入帳號
    password="your_password"   # 填入密碼
)