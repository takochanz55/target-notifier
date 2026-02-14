import requests
from bs4 import BeautifulSoup

# --- 設定（あなたの情報に書き換えてください） ---
LINE_TOKEN = 'v+CfQHk/KICjaZxzeGCtXcH4BYY92i3bldQzatq4WyDw0Jc9/hFK/DBjqpI+6Vz+dpvxA+h2dDq87g8ttk5+X6CEHO+LjlD/e4aZz/6kZYAHdtCcXPsFJY3tM7DJHLr+/ip8VHHHPRqVu8JsLwAtcwdB04t89/1O/w1cDnyilFU='
USER_ID = 'Uf60cac61f9835c5f258df0ff2e1f5db4'
TARGET_URL = 'https://www.target.co.jp/'
# --------------------------------------------

def send_line(message):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {LINE_TOKEN}'}
    payload = {'to': USER_ID, 'messages': [{'type': 'text', 'text': message}]}
    requests.post(url, headers=headers, json=payload)

def main():
    # サイト読み込み
    res = requests.get(TARGET_URL)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    # 商品名を取得
    current_items = []
    for dt in soup.find_all('dt', class_='item_name'):
        name = dt.get_text(strip=True)
        if name: current_items.append(name)

    if not current_items: return

    # 【重要】今回はGitHubに保存せず、新着の判定だけ行います
    # ※初回実行時は全商品が届きます
    msg = "【ターゲット新着】\n" + "\n".join(current_items[:5]) # 最初は5件だけテスト
    send_line(msg)

if __name__ == "__main__":
    main()
