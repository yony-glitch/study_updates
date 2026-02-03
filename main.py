# import feedparser
# import requests
# import json
# import os
# import time
# import html
# import re  # HTML 태그 제거를 위해 추가

# # RSS 피드 리스트
# RSS_FEEDS = {
#     "https://brunch.co.kr/rss/@@eZqg": "Cherry",
#     "https://design-tra.tistory.com/rss": "Voyage: 사용자에게로 향하는 여정",
#     "https://brunch.co.kr/rss/@@a2Ed": "Nono",
#     "https://brunch.co.kr/rss/@@7pqA": "김영욱",
#     "https://brunch.co.kr/rss/@@eDYE": "florent",
#     "https://brunch.co.kr/rss/@@31zt": "tami",
#     "https://brunch.co.kr/rss/@@a1Ap": "이성긍",
#     "https://brunch.co.kr/rss/@@fcZn": "비이크",
#     "https://brunch.co.kr/rss/@@3wuQ": "kaily",
#     "https://brunch.co.kr/rss/@@eCrw": "세기말 서비스기획자들",
#     "https://brunch.co.kr/rss/@@2Y6c": "회사원숭 소피",
#     "https://brunch.co.kr/rss/@@4zJ": "서점직원",
#     "https://brunch.co.kr/rss/@@7aZb": "타비",
#     "https://brunch.co.kr/rss/@@3A7": "밤열두시",
#     "https://brunch.co.kr/rss/@@10mY": "이선주",
#     "https://brunch.co.kr/rss/@@PAH": "박세호",
#     "https://brunch.co.kr/rss/@@6C10": "김경환",
#     "https://brunch.co.kr/rss/@@GGz": "Jinhee Park",
#     "https://brunch.co.kr/rss/@@2hV3": "우디",
#     "https://brunch.co.kr/rss/@@6Lbn": "김현준",
# }

# NOTION_TOKEN = os.environ.get('NOTION_TOKEN')
# DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')
# DB_FILE = 'last_posts.json'

# def add_to_notion(title, link, owner_name, published_date, description):
#     url = "https://api.notion.com/v1/pages"
#     headers = {
#         "Authorization": f"Bearer {NOTION_TOKEN}",
#         "Content-Type": "application/json",
#         "Notion-Version": "2022-06-28"
#     }
    
#     # 노션 API 데이터 구조
#     data = {
#         "parent": { "database_id": DATABASE_ID },
#         "properties": {
#             "제목": { "title": [{ "text": { "content": title } }] },
#             "URL": { "url": link },
#             "작성자": { "select": { "name": owner_name } },
#             "업로드 일시": { "date": { "start": published_date } },
#             "도입부": { "rich_text": [{ "text": { "content": description[:2000] } }] } # 노션 글자수 제한 고려
#         }
#     }
#     response = requests.post(url, headers=headers, json=data)
#     return response.status_code

# def check_feeds():
#     if os.path.exists(DB_FILE):
#         with open(DB_FILE, 'r', encoding='utf-8') as f:
#             try:
#                 data = json.load(f)
#                 last_posts = data if isinstance(data, list) else []
#             except json.JSONDecodeError:
#                 last_posts = []
#     else:
#         last_posts = []

#     new_last_posts = last_posts.copy()

#     for rss_url, owner in RSS_FEEDS.items():
#         feed = feedparser.parse(rss_url)
#         if not feed.entries:
#             continue
        
#         for entry in reversed(feed.entries):
#             link = entry.link
            
#             # 1. 제목 처리
#             raw_title = entry.get('title', '제목 없음')
#             clean_title = html.unescape(raw_title)

#             # 2. 도입부(description) 처리: HTML 태그 제거 및 unescape
#             raw_desc = entry.get('description', '')
#             # <...태그...> 제거 정규식
#             clean_desc = re.sub(r'<[^>]+>', '', raw_desc)
#             clean_desc = html.unescape(clean_desc).strip()
#             # 너무 길면 노션 API에서 오류가 날 수 있으므로 슬라이싱 (공백 포함 안전하게)
#             clean_desc = (clean_desc[:1900] + '...') if len(clean_desc) > 1900 else clean_desc

#             if "blog.naver.com" in link:
#                 link = link.split('?')[0]

#             if link not in last_posts:
#                 print(f"새로운 글 전송 중: {clean_title} (작성자: {owner})")
                
#                 if entry.get('published_parsed'):
#                     published_date = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', entry.published_parsed)
#                 else:
#                     published_date = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())

#                 # 노션 전송 (인자값에 clean_desc 추가)
#                 status = add_to_notion(clean_title, link, owner, published_date, clean_desc)
                
#                 if status == 200:
#                     new_last_posts.append(link)
#                 else:
#                     print(f"노션 전송 실패: {status}")
                
#                 time.sleep(0.3)

#     with open(DB_FILE, 'w', encoding='utf-8') as f:
#         json.dump(new_last_posts, f, indent=4, ensure_ascii=False)

# if __name__ == "__main__":
#     check_feeds()




import feedparser
import requests
import json
import os
import time
import html
import re

# RSS 피드 리스트 (기존 리스트와 동일)
RSS_FEEDS = {
    "https://brunch.co.kr/rss/@@eZqg": "Cherry",
    "https://design-tra.tistory.com/rss": "Voyage: 사용자에게로 향하는 여정",
    "https://brunch.co.kr/rss/@@a2Ed": "Nono",
    "https://brunch.co.kr/rss/@@7pqA": "김영욱",
    "https://brunch.co.kr/rss/@@eDYE": "florent",
    "https://brunch.co.kr/rss/@@31zt": "tami",
    "https://brunch.co.kr/rss/@@a1Ap": "이성긍",
    "https://brunch.co.kr/rss/@@fcZn": "비이크",
    "https://brunch.co.kr/rss/@@3wuQ": "kaily",
    "https://brunch.co.kr/rss/@@eCrw": "세기말 서비스기획자들",
    "https://brunch.co.kr/rss/@@2Y6c": "회사원숭 소피",
    "https://brunch.co.kr/rss/@@4zJ": "서점직원",
    "https://brunch.co.kr/rss/@@7aZb": "타비",
    "https://brunch.co.kr/rss/@@3A7": "밤열두시",
    "https://brunch.co.kr/rss/@@10mY": "이선주",
    "https://brunch.co.kr/rss/@@PAH": "박세호",
    "https://brunch.co.kr/rss/@@6C10": "김경환",
    "https://brunch.co.kr/rss/@@GGz": "Jinhee Park",
    "https://brunch.co.kr/rss/@@2hV3": "우디",
    "https://brunch.co.kr/rss/@@6Lbn": "김현준",
}

# 구글 앱스 스크립트 배포 URL (1단계에서 복사한 URL을 환경 변수에 넣으세요)
GOOGLE_SHEET_URL = os.environ.get('GOOGLE_SHEET_URL') 
DB_FILE = 'last_posts.json'

def add_to_google_sheet(title, link, owner_name, published_date, description):
    # 구글 시트로 보낼 데이터 포맷
    data = {
        "title": title,
        "link": link,
        "owner": owner_name,
        "date": published_date,
        "description": description
    }
    
    # GAS 웹 앱으로 POST 요청
    response = requests.post(GOOGLE_SHEET_URL, json=data)
    return response.status_code

def check_feeds():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                last_posts = data if isinstance(data, list) else []
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
            
            raw_title = entry.get('title', '제목 없음')
            clean_title = html.unescape(raw_title)

            raw_desc = entry.get('description', '')
            clean_desc = re.sub(r'<[^>]+>', '', raw_desc)
            clean_desc = html.unescape(clean_desc).strip()
            # 구글 시트는 글자수 제한이 널널하지만 가독성을 위해 1500자 제한
            clean_desc = (clean_desc[:1500] + '...') if len(clean_desc) > 1500 else clean_desc

            if "blog.naver.com" in link:
                link = link.split('?')[0]

            if link not in last_posts:
                print(f"새로운 글 전송 중: {clean_title} (작성자: {owner})")
                
                if entry.get('published_parsed'):
                    published_date = time.strftime('%Y-%m-%d %H:%M:%S', entry.published_parsed)
                else:
                    published_date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

                # 구글 시트 전송 호출
                status = add_to_google_sheet(clean_title, link, owner, published_date, clean_desc)
                
                if status == 200:
                    new_last_posts.append(link)
                else:
                    print(f"구글 시트 전송 실패: {status}")
                
                time.sleep(0.3)

    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_last_posts, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    check_feeds()
