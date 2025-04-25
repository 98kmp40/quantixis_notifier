# Quantixis 小說新章節 Email 通知器

## 安裝方式

1. 下載或 clone 本專案
2. 安裝 Python 套件：

   ```bash
   pip install -r requirements.txt
   python -m playwright install chromium
3.編輯 config.json，填入你的 Gmail 資訊與密碼

4.執行程式：python main.py

5.（進階）設定 crontab 每天自動執行（Mac/Linux）

請參考「自動化排程」章節說明

功能
自動檢查 Quantixis 網站小說章節是否有新章節

有新章節會自動寄送 Email 通知（每天只寄一次）

進階：自動化排程（可選）
Mac/Linux 使用 crontab 定時自動檢查
開啟終端機輸入

crontab -e
加入以下內容（假設你的 python 路徑與專案資料夾正確）：

swift

*/5 11 * * * /你的/python3/路徑 /你的/專案/路徑/main.py >> /你的/專案/路徑/cronlog.txt 2>&1
這代表每天 11:00~11:59，每 5 分鐘檢查一次（建議專案放在不會被移動的地方）

常見問題
Q: 為什麼要用 Gmail 應用程式密碼？

A: Gmail 不允許直接用帳號密碼發信，必須到 Google 帳號安全性產生「應用程式密碼」。

Q: 程式會重複發信嗎？

A: 不會，每天只要有新章節，通知一次後當天就不會再通知。

有任何問題歡迎到 Issues 留言討論！






