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
    print("サイトにアクセス中...") # 進行状況を表示
    res = requests.get(TARGET_URL)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    current_items = []
    items = soup.find_all('dt', class_='item_name')
    print(f"見つかった商品数: {len(items)}") # 何件見つかったか表示

    for dt in items:
        name = dt.get_text(strip=True)
        if name: current_items.append(name)

    if not current_items:
        print("商品名が見つかりませんでした。サイトの構造が変わった可能性があります。")
        return

    print(f"送信する商品例: {current_items[0]}") # 1件目を表示
    msg = "【テスト通知】\n" + "\n".join(current_items[:5])
    
    # LINE送信の結果を表示
    response = send_line(msg)
    print(f"LINE送信結果ステータス: {response.status_code}")
    print(f"LINE送信レスポンス: {response.text}")

if __name__ == "__main__":
    main()
