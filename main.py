import feedparser
import requests
import json
import os
import time

# RSS 피드 리스트
RSS_FEEDS = {
    "https://brunch.co.kr/rss/@@eZqg": "Cherry",
    "https://design-tra.tistory.com/rss": "Voyage: 사용자에게로 향하는 여정",
}

NOTION_TOKEN = os.environ['NOTION_TOKEN']
DATABASE_ID = os.environ['NOTION_DATABASE_ID']
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
    
    if response.status_code != 200:
        print(f"노션 전송 실패: {response.text}")
        
    return response.status_code

def check_feeds():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            last_posts = json.load(f)
    else:
        last_posts = {}
  
    new_last_posts = last_posts.copy()

    for rss_url, owner in RSS_FEEDS.items():
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            continue
        
        latest_entry = feed.entries[0]
        latest_link = latest_entry.link

        # 네이버 블로그 링크 정리
        if "blog.naver.com" in latest_link:
            latest_link = latest_link.split('?')[0]

        # [수정됨] 날짜 정보 처리: owner_name을 owner로 변경하고 안정성 강화
        if latest_entry.get('published_parsed'):
            published_date = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', latest_entry.published_parsed)
        else:
            published_date = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
            print(f"공지: '{owner}'의 최신 글 날짜를 읽을 수 없어 현재 시간으로 기록합니다.")

        # 새 글 여부 확인 및 노션 전송
        if rss_url not in last_posts or last_posts[rss_url] != latest_link:
            print(f"새 글 발견: {latest_entry.title} (작성자: {owner})")
            
            # 여기서 owner 변수를 사용하여 노션에 전송합니다.
            status = add_to_notion(latest_entry.title, latest_link, owner, published_date)
            
            if status == 200:
                new_last_posts[rss_url] = latest_link

    with open(DB_FILE, 'w') as f:
        json.dump(new_last_posts, f, indent=4)

if __name__ == "__main__":
    check_feeds()
