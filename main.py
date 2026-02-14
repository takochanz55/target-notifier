import requests
from bs4 import BeautifulSoup
import sys

# --- 設定（必ず確認してください！） ---
LINE_TOKEN = 'v+CfQHk/KICjaZxzeGCtXcH4BYY92i3bldQzatq4WyDw0Jc9/hFK/DBjqpI+6Vz+dpvxA+h2dDq87g8ttk5+X6CEHO+LjlD/e4aZz/6kZYAHdtCcXPsFJY3tM7DJHLr+/ip8VHHHPRqVu8JsLwAtcwdB04t89/1O/w1cDnyilFU='
USER_ID = 'Uf60cac61f9835c5f258df0ff2e1f5db4'
TARGET_URL = 'https://www.target.co.jp/'
# --------------------------------------------

def send_line(message):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_TOKEN}'
    }
    payload = {
        'to': USER_ID,
        'messages': [{'type': 'text', 'text': message}]
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        print(f"LINE送信ステータス: {res.status_code}")
        print(f"LINEレスポンス: {res.text}")
        return res
    except Exception as e:
        print(f"LINE送信中にエラー発生: {e}")

def main():
    print("--- 処理開始 ---")
    try:
        print(f"サイトにアクセス中: {TARGET_URL}")
        res = requests.get(TARGET_URL, timeout=30)
        res.encoding = 'utf-8'
        print(f"サイトアクセス成功 (ステータス: {res.status_code})")
        
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.find_all('dt', class_='item_name')
        print(f"見つかった商品数: {len(items)}")

        current_items = []
        for dt in items:
            name = dt.get_text(strip=True)
            if name:
                current_items.append(name)

        if not current_items:
            print("商品リストが空です。HTMLの構造を再確認する必要があります。")
            return

        print(f"送信内容 (先頭): {current_items[0]}")
        msg = "【ターゲット新着テスト】\n" + "\n".join(current_items[:5])
        send_line(msg)
        
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    main()
