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
    print("--- 商品エリア狙い撃ち版で開始 ---")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    res = requests.get(TARGET_URL, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    current_items = []
    
    # 1. 「新商品」という見出しがあるブロック(id="index_new_item")の中だけを探す
    new_item_section = soup.find('div', id='index_new_item')
    
    if new_item_section:
        # その中の商品名(class="item_name")を取得
        items = new_item_section.find_all(class_='item_name')
        for item in items:
            name = item.get_text(strip=True)
            if name:
                current_items.append(name)
    
    # 2. もし上記で見つからない場合の予備（「おすすめ商品」エリアも念のため）
    if not current_items:
        recommend_section = soup.find('div', id='index_recommend_item')
        if recommend_section:
            items = recommend_section.find_all(class_='item_name')
            for item in items:
                name = item.get_text(strip=True)
                current_items.append(name)

    # 「お知らせ」によく含まれるキーワードを除外（念のためのフィルター）
    exclude_keywords = ["お知らせ", "について", "変更", "発行"]
    current_items = [i for i in current_items if not any(k in i for k in exclude_keywords)]

    print(f"見つかった本物の商品数: {len(current_items)}")

    if not current_items:
        print("商品が見つかりませんでした。")
        return

    # 重複除去
    current_items = list(dict.fromkeys(current_items))
    
    # 通知（まずは最新5件）
    msg = "【二木トレカ新着】\n" + "\n".join(current_items[:5])
    response = send_line(msg)
    print(f"LINE送信結果: {response.status_code}")

if __name__ == "__main__":
    main()
