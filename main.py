import requests
from bs4 import BeautifulSoup

# --- 設定（書き換えてください） ---
LINE_TOKEN = 'v+CfQHk/KICjaZxzeGCtXcH4BYY92i3bldQzatq4WyDw0Jc9/hFK/DBjqpI+6Vz+dpvxA+h2dDq87g8ttk5+X6CEHO+LjlD/e4aZz/6kZYAHdtCcXPsFJY3tM7DJHLr+/ip8VHHHPRqVu8JsLwAtcwdB04t89/1O/w1cDnyilFU='
USER_ID = 'Uf60cac61f9835c5f258df0ff2e1f5db4'
TARGET_URL = 'https://www.target.co.jp/'
# --------------------------------------------

def send_line(message):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {LINE_TOKEN}'}
    payload = {'to': USER_ID, 'messages': [{'type': 'text', 'text': message}]}
    return requests.post(url, headers=headers, json=payload)

def main():
    print("--- 最終構造解析モードで開始 ---")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        res = requests.get(TARGET_URL, headers=headers, timeout=30)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        current_items = []
        
        # 二木さんのサイトの「商品名」が確実に入っているクラスを指定
        items = soup.find_all(class_='item_name')
        
        # 除外したいサイドメニューなどのワード
        exclude_keywords = ["プロ野球カード", "Jリーグカード", "サッカー", "NBA", "MLB", "NFL", "NHL", "テニス", "大相撲", "バレー", "ラグビー", "B.LEAGUE", "P★LEAGUE", "ホース", "体操", "ゴルフ", "プロレス"]

        for item in items:
            name = item.get_text(strip=True)
            
            # 条件1: 15文字以上（「2026年プロ野球カード」は13文字なので、商品名はこれより長い）
            # 条件2: 除外キーワードに完全一致しない（サイドメニュー対策）
            if name and len(name) >= 15:
                if name not in exclude_keywords:
                    current_items.append(name)

        # 重複を削除
        current_items = list(dict.fromkeys(current_items))
        
        print(f"抽出された本物の商品数: {len(current_items)}")

        if not current_items:
            print("まだ0件です。タグを 'a' タグに変更して再試行します...")
            # 予備：aタグの中から「予約」や「BOX」を含むものを探す
            for a in soup.find_all('a'):
                t = a.get_text(strip=True)
                if len(t) > 20 and any(k in t for k in ["予約", "BOX", "202", "カード"]):
                    current_items.append(t)
            current_items = list(dict.fromkeys(current_items))

        if not current_items:
            print("最終手段でも見つかりませんでした。")
            return

        print(f"送信内容例: {current_items[0]}")
        # LINEには最新の10件を送る
        msg = "【ターゲット新着入荷！】\n" + "\n".join(current_items[:10])
        response = send_line(msg)
        print(f"LINE送信結果: {response.status_code}")

    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    main()
