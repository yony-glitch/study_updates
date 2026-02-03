import feedparser
import requests
import json
import os
import time
import html  # html.unescape를 위해 추가

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
    # 이미 전송한 링크 목록 불러오기
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # last_posts가 리스트인지 확인하여 안전하게 불러오기
                if isinstance(data, list):
                    last_posts = data
                else:
                    last_posts = []
            except json.JSONDecodeError:
                last_posts = []
    else:
        last_posts = []

    new_last_posts = last_posts.copy()

    for rss_url, owner in RSS_FEEDS.items():
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            continue
        
        for entry in reversed(feed.entries):
            link = entry.link
            
            # 제목의 특수 문자열 치환
            raw_title = entry.get('title', '제목 없음')
            clean_title = html.unescape(raw_title)

            if "blog.naver.com" in link:
                link = link.split('?')[0]

            if link not in last_posts:
                print(f"새로운 글 전송 중: {clean_title} (작성자: {owner})")
                
                if entry.get('published_parsed'):
                    published_date = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', entry.published_parsed)
                else:
                    published_date = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())

                # 노션 전송 (status 정의)
                status = add_to_notion(clean_title, link, owner, published_date)
                
                # status 체크를 if link not in last_posts 안으로 이동
                if status == 200:
                    new_last_posts.append(link)
                else:
                    print(f"노션 전송 실패: {status}")
                
                time.sleep(0.3)

    # 업데이트된 전송 목록 저장
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_last_posts, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    check_feeds()
