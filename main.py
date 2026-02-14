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
    print("--- 最終・価格連動フィルタ版で開始 ---")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    res = requests.get(TARGET_URL, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    current_items = []
    
    # 手法：商品価格（￥）が含まれるエリアを特定し、その上の商品名を取得する
    # 二木さんのサイト構造： <dt class="item_name">商品名</dt> <dd class="item_price">￥6,200</dd>
    
    # すべての価格表示を探す
    price_tags = soup.find_all(class_='item_price')
    
    for price in price_tags:
        # 価格タグの直前にある「商品名タグ(dt)」を探す
        name_tag = price.find_previous('dt', class_='item_name')
        if name_tag:
            name = name_tag.get_text(strip=True)
            # 「○○年プロ野球カード」というメニュー名を除外するための条件
            if name and "カード" in name and len(name) > 15:
                current_items.append(name)

    # 重複を削除
    current_items = list(dict.fromkeys(current_items))
    
    print(f"抽出された本物の商品数: {len(current_items)}")

    if not current_items:
        print("商品が見つかりませんでした。")
        return

    # 送信内容を作成
    print(f"送信内容例: {current_items[0]}")
    msg = "【本物の新着入荷！】\n" + "\n".join(current_items[:10]) # 多めに10件
    response = send_line(msg)
    print(f"LINE送信結果: {response.status_code}")

if __name__ == "__main__":
    main()
