import feedparser
import requests
import json
import os
import time
import html 

# RSS 피드 리스트
RSS_FEEDS = {
    "https://brunch.co.kr/rss/@@eZqg": "Cherry",
    "https://design-tra.tistory.com/rss": "Voyage: 사용자에게로 향하는 여정",
    "https://brunch.co.kr/rss/@@a2Ed": "Nono",
    "https://brunch.co.kr/rss/@@7pqA": "김영욱",
    "https://brunch.co.kr/rss/@@eDYE": "florent"
}

NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')
DB_FILE = 'last_posts.json'

def add_to_notion(title, link, owner_name, published_date):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "제목": { "title": [{ "text": { "content": title } }] },
            "URL": { "url": link },
            "작성자": { "select": { "name": owner_name } },
            "업로드 일시": { "date": { "start": published_date } }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code

def check_feeds():
    # 1. Load existing posts
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure we are working with a list even if the file is a dict
            last_posts = data if isinstance(data, list) else list(data.keys())
    else:
        last_posts = []

    new_last_posts = last_posts.copy()

    for rss_url, owner in RSS_FEEDS.items():
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            continue
        
        for entry in reversed(feed.entries):
            link = entry.link
            
            # ... (your title cleaning logic) ...

            if link not in last_posts:
                # ... (your Notion sending logic) ...
                
                if status == 200:
                    new_last_posts.append(link) # This will now work because it's a list
    # 업데이트된 전송 목록 저장
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_last_posts, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    check_feeds()
