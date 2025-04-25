import os
import json
from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)
GMAIL_USER = cfg["email"]
GMAIL_APP_PASSWORD = cfg["app_password"]
RECEIVER_EMAIL = cfg["receiver"]
URL = cfg["novel_url"]
SAVE_FILE = "last_chapter.json"

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = RECEIVER_EMAIL
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)

def has_notified_today():
    today = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists("notified_date.txt"):
        with open("notified_date.txt", "r") as f:
            last = f.read().strip()
            if last == today:
                return True
    return False

def save_notified_today():
    today = datetime.now().strftime("%Y-%m-%d")
    with open("notified_date.txt", "w") as f:
        f.write(today)

def get_latest_chapter_title():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        page.wait_for_timeout(5000)
        title_element = page.query_selector("a[style='color:Gray;']")
        title_text = title_element.inner_text() if title_element else "無法取得章節"
        browser.close()
        return title_text.strip()

def load_last_title():
    if not os.path.exists(SAVE_FILE):
        return ""
    with open(SAVE_FILE, "r") as f:
        return json.load(f).get("title", "")

def save_current_title(title):
    with open(SAVE_FILE, "w") as f:
        json.dump({"title": title}, f)

def main():
    if has_notified_today():
        print("今天已經通知過了，不再重複通知。")
        return

    current_title = get_latest_chapter_title()
    last_title = load_last_title()
    print("目前章節：", current_title)
    if current_title and current_title != last_title and current_title != "無法取得章節":
        body = f"📖 Quantixis 有新章節更新了！\n👉 {current_title}\n🔗 {URL}"
        send_email("Quantixis 新章節通知", body)
        save_current_title(current_title)
        save_notified_today()
        print("✅ 已發送 Email 通知")
    else:
        print("⏳ 尚無更新")

if __name__ == "__main__":
    main()
