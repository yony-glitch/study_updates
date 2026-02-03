import feedparser
import requests
import json
import os
import time

# RSS 피드 리스트
RSS_FEEDS = {
    "https://brunch.co.kr/rss/@@eZqg": "Cherry",
    "https://design-tra.tistory.com/rss": "Voyage: 사용자에게로 향하는 여정",
    "https://brunch.co.kr/rss/@@a2Ed": "Nono",
    "https://brunch.co.kr/rss/@@7pqA": "김영욱",
    "https://brunch.co.kr/rss/@@eDYE": "florent"
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
    is_first_run = not os.path.exists(DB_FILE)

    if not is_first_run:
        with open(DB_FILE, 'r') as f:
            last_posts = json.load(f)
    else:
        last_posts = {}

    new_last_posts = last_posts.copy()

    for rss_url, owner in RSS_FEEDS.items():
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            continue

        entries = feed.entries

        # ✅ 최초 실행: 모든 글 전송
        if is_first_run:
            print(f"[초기 동기화] {owner}의 글 {len(entries)}개 전송 시작")

            for entry in reversed(entries):
                link = entry.link
                if "blog.naver.com" in link:
                    link = link.split('?')[0]

                if entry.get('published_parsed'):
                    published_date = time.strftime(
                        '%Y-%m-%dT%H:%M:%S.000Z',
                        entry.published_parsed
                    )
                else:
                    published_date = time.strftime(
                        '%Y-%m-%dT%H:%M:%S.000Z',
                        time.gmtime()
                    )

                add_to_notion(
                    entry.title,
                    link,
                    owner,
                    published_date
                )

            # 가장 최신 글만 기록
            latest_entry = entries[0]
            new_last_posts[rss_url] = latest_entry.link

        # ✅ 이후 실행: 새 글 1개만
        else:
            latest_entry = entries[0]
            latest_link = latest_entry.link

            if "blog.naver.com" in latest_link:
                latest_link = latest_link.split('?')[0]

            if latest_entry.get('published_parsed'):
                published_date = time.strftime(
                    '%Y-%m-%dT%H:%M:%S.000Z',
                    latest_entry.published_parsed
                )
            else:
                published_date = time.strftime(
                    '%Y-%m-%dT%H:%M:%S.000Z',
                    time.gmtime()
                )

            if last_posts.get(rss_url) != latest_link:
                print(f"새 글 발견: {latest_entry.title} ({owner})")
                status = add_to_notion(
                    latest_entry.title,
                    latest_link,
                    owner,
                    published_date
                )
                if status == 200:
                    new_last_posts[rss_url] = latest_link

    with open(DB_FILE, 'w') as f:
        json.dump(new_last_posts, f, indent=4)
    check_feeds()
