import requests
from bs4 import BeautifulSoup

# --- 設定（ここはそのまま！） ---
LINE_TOKEN = 'v+CfQHk/KICjaZxzeGCtXcH4BYY92i3bldQzatq4WyDw0Jc9/hFK/DBjqpI+6Vz+dpvxA+h2dDq87g8ttk5+X6CEHO+LjlD/e4aZz/6kZYAHdtCcXPsFJY3tM7DJHLr+/ip8VHHHPRqVu8JsLwAtcwdB04t89/1O/w1cDnyilFU='
USER_ID = 'Uf60cac61f9835c5f258df0ff2e1f5db4'
TARGET_URL = 'https://www.target.co.jp/'
# --------------------------------------------

def send_line(message):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {LINE_TOKEN}'}
    payload = {'to': USER_ID, 'messages': [{'type': 'text', 'text': message}]}
    res = requests.post(url, headers=headers, json=payload)
    return res

def main():
    print("--- 高精度フィルター版で開始 ---")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    res = requests.get(TARGET_URL, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    current_items = []
    
    # 手法：すべての「商品名が含まれそうなタグ」をスキャン
    # 二木さんのサイトでは dt や a タグに商品名が入ります
    potential_items = soup.find_all(['dt', 'a'])

    # 除外したい「お知らせ」系のキーワード
    exclude_keywords = ["お知らせ", "について", "変更", "発行", "ポイント", "ガイド", "表記", "ポリシー", "お問い合わせ", "ログイン", "マイページ", "カート"]

    for item in potential_items:
        name = item.get_text(strip=True)
        
        # フィルター条件：
        # 1. 文字が空でない
        # 2. 10文字以上（商品名は長いため）
        # 3. 除外キーワードが含まれていない
        # 4. 「予約」や「BOX」、「カード」などのトレカ特有の言葉が含まれている（精度アップ）
        if name and len(name) >= 10:
            if not any(k in name for k in exclude_keywords):
                # トレカらしいキーワードが含まれているか、または特定のクラスを持っている場合
                if any(k in name for k in ["予約", "BOX", "カード", "202", "BBM", "MLB", "NBA"]):
                    current_items.append(name)

    # 重複を削除
    current_items = list(dict.fromkeys(current_items))
    
    print(f"抽出された商品数: {len(current_items)}")

    if not current_items:
        print("商品が見つかりませんでした。別のタグを探します。")
        # 最終手段：特定のクラス名(item_name)をもう一度フラットに探す
        items = soup.find_all(class_='item_name')
        current_items = [i.get_text(strip=True) for i in items if i.get_text(strip=True)]

    if not current_items:
        return

    # 最新の5件を表示
    print(f"送信内容例: {current_items[0]}")
    msg = "【二木トレカ新着】\n" + "\n".join(current_items[:5])
    response = send_line(msg)
    print(f"LINE送信結果: {response.status_code}")

if __name__ == "__main__":
    main()
