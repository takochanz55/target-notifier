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
    print("--- 抽出ロジック強化版で開始 ---")
    # サイトがプログラムからのアクセスを拒否しないよう「ブラウザのふり」をする設定を追加
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    res = requests.get(TARGET_URL, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    current_items = []
    
    # 手法1: class名 "item_name" を持つ全ての要素を探す
    items = soup.find_all(class_='item_name')
    
    # 手法2: もし手法1で見つからなければ、リンクテキストから探す（二木さんのサイト特有の構造対策）
    if not items:
        items = soup.select('dl dt a') # dlタグの中のdtの中のaタグを探す

    for item in items:
        name = item.get_text(strip=True)
        if name and len(name) > 5: # 短すぎるゴミデータを除外
            current_items.append(name)

    print(f"見つかった商品数: {len(current_items)}")

    if not current_items:
        print("まだ商品が見つかりません。HTMLソースを出力して確認します。")
        # print(res.text[:500]) # 予備のデバッグ用
        return

    # 重複を除去して整える
    current_items = list(dict.fromkeys(current_items))
    print(f"送信内容 (先頭): {current_items[0]}")
    
    msg = "【ターゲット新着】\n" + "\n".join(current_items[:5])
    response = send_line(msg)
    print(f"LINE送信結果: {response.status_code}")

if __name__ == "__main__":
    main()
