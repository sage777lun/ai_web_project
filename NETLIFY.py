import requests

# 你的 Netlify API 設定
NETLIFY_API_URL = "https://api.netlify.com/api/v1/sites/cozy-sprite-e97492/deploys"
NETLIFY_TOKEN = "nfp_MSQXfZERjXNXEWFTKwWGNHaXMjB8JTeT8e14"

# AI 生成的網頁內容
web_content = "<html><head><title>AI 網頁</title></head><body><h1>這是 AI 自動生成的網頁！</h1></body></html>"

# 儲存為本地文件（可選）
file_path = "index.html"
with open(file_path, "w", encoding="utf-8") as file:
    file.write(web_content)

# 讀取網頁內容並準備上傳
with open(file_path, "rb") as file:
    files = {"file": file}

headers = {"Authorization": f"Bearer {NETLIFY_TOKEN}"}

# 觸發 Netlify 部署
response = requests.post(NETLIFY_API_URL, headers=headers, files=files)

if response.status_code == 200:
    print("✅ 網頁已成功部署！網址：", response.json().get("url", "未知"))
else:
    print(f"❌ 部署失敗: {response.text}")