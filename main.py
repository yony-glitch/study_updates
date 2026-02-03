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

NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')
DB_FILE = 'sent_links.json' # 이름을 좀 더 명확하게 변경

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
            sent_links = json.load(f)
    else:
        sent_links = [] # 처음 실행 시 빈 리스트

    new_sent_links = sent_links.copy()

    for rss_url, owner in RSS_FEEDS.items():
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            continue
        
        # 과거 글부터 처리하기 위해 리스트를 뒤집음 (선택 사항)
        for entry in reversed(feed.entries):
            link = entry.link
            
            # 네이버 블로그 링크 정리
            if "blog.naver.com" in link:
                link = link.split('?')[0]

            # 이미 보낸 링크인지 확인
            if link not in sent_links:
                print(f"새로운 글 전송 중: {entry.title} (작성자: {owner})")
                
                # 날짜 처리
                if entry.get('published_parsed'):
                    published_date = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', entry.published_parsed)
                else:
                    published_date = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())

                status = add_to_notion(entry.title, link, owner, published_date)
                
                if status == 200:
                    new_sent_links.append(link) # 성공 시 저장 목록에 추가
                else:
                    print(f"노션 전송 실패: {entry.title}")
                
                # API 과부하 방지를 위한 짧은 휴식 (선택)
                time.sleep(0.3)

    # 업데이트된 전송 목록 저장
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_sent_links, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    check_feeds()
