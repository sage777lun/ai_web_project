import json
import spacy
from textblob import TextBlob

# NLP 初始化
nlp = spacy.load("zh_core_web_sm")

class SmartResponseAI:
    def __init__(self, memory_file="memory.json", training_file="training_data.json", context_size=5):
        self.memory_file = memory_file
        self.training_file = training_file
        self.context_size = context_size  # 記住最近 5 條訊息
        self.memory = self.load_memory()

        # **批量訓練 AI**
        self.train_from_json()

    def load_memory(self):
        """從 JSON 文件讀取記憶"""
        try:
            with open(self.memory_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_memory(self):
        """將記憶存入 JSON 文件"""
        with open(self.memory_file, "w", encoding="utf-8") as file:
            json.dump(self.memory, file, ensure_ascii=False, indent=4)

    def analyze_message(self, user_message):
        """解析語言並提取關鍵詞"""
        doc = nlp(user_message)
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
        return keywords

    def analyze_sentiment(self, user_message):
        """判斷語句情緒"""
        blob = TextBlob(user_message)
        sentiment = blob.sentiment.polarity
        return "正面" if sentiment > 0.3 else "負面" if sentiment < -0.3 else "中立"

    def detect_question(self, user_message):
        """判斷是否為疑問句"""
        question_words = ["什麼", "哪裡", "為什麼", "如何", "怎麼"]
        return any(word in user_message for word in question_words)

    def train_from_json(self):
        """從 JSON 訓練文件載入數據，讓 AI 一次性學習大量內容"""
        try:
            with open(self.training_file, "r", encoding="utf-8") as file:
                training_data = json.load(file)
                self.memory.extend(training_data)

            self.save_memory()
            print("✅ AI 已成功從 JSON 訓練數據學習！")

        except FileNotFoundError:
            print("❌ 訓練文件未找到！請確認 `training_data.json` 存在！")

    def learn(self, user_message):
        """記住最近的訊息，並移除舊訊息"""
        analyzed = {
            "text": user_message,
            "keywords": self.analyze_message(user_message),
            "sentiment": self.analyze_sentiment(user_message),
            "is_question": self.detect_question(user_message)
        }
        self.memory.append(analyzed)

        # **只保留最近的 context_size 條訊息**
        if len(self.memory) > self.context_size:
            self.memory.pop(0)

        self.save_memory()

    def respond(self, user_message):
        """AI 根據上下文提供最合理的回應"""
        user_keywords = self.analyze_message(user_message)
        user_sentiment = self.analyze_sentiment(user_message)
        is_question = self.detect_question(user_message)

        relevant_responses = sorted(
            self.memory,
            key=lambda mem: sum(1 for kw in user_keywords if kw in mem["keywords"]),
            reverse=True
        )

        if is_question:
            return "這是一個問題，我會試著找到最好的答案！" if relevant_responses else "我目前沒有相關答案，但會記住你的問題！"
        elif relevant_responses:
            return f"你提到 {', '.join(user_keywords)}，最近的相關訊息是: {relevant_responses[0]['text']}"
        else:
            return "你好！這是新的話題，我會好好記住！"

# 測試 AI
ai = SmartResponseAI()
print(ai.respond("最近有什麼好看的科幻電影推薦？"))