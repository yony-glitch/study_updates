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

# RSS 피드 리스트
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
    "https://prime-career.tistory.com/rss": "프라임 커리어",
    "https://dabinlee.tistory.com/rss": "다람이의 공부방",
    "https://soosunnaa.tistory.com/rss": "SOOSUNNAA",
    "https://germweapon.tistory.com/rss": "세균무기",
    "https://brunch.co.kr/rss/@@4vT": "조영수",
    "https://brunch.co.kr/rss/@@1bJx": "Sunny Lee",
    "https://brunch.co.kr/rss/@@79HT": "Yuni",
    "https://brunch.co.kr/rss/@@7wf4": "꿈꾸는밍",
    "https://brunch.co.kr/rss/@@hZdl": "비니",
    "https://brunch.co.kr/rss/@@92ovg": "디자이너강",
    "https://brunch.co.kr/rss/@@9zTH": "이동석",
    "https://brunch.co.kr/rss/@@aseH": "MODAY",
    "https://brunch.co.kr/rss/@@ca1X": "bom",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCxRnfrmJAkRLarzeBJETB5g": "Madia Designer",
}

# 구글 앱스 스크립트 배포 URL (환경 변수)
GOOGLE_SHEET_URL = os.environ.get('GOOGLE_SHEET_URL') 
DB_FILE = 'last_posts.json'

def add_to_google_sheet(title, link, owner_name, published_date, description):
    data = {
        "title": title,
        "link": link,
        "owner": owner_name,
        "date": published_date,
        "description": description
    }
    try:
        response = requests.post(GOOGLE_SHEET_URL, json=data)
        return response.status_code
    except:
        return 500

def check_feeds():
    # 1. 마지막 전송 정보 불러오기 (딕셔너리 구조: { "RSS_URL": "LAST_LINK" })
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try:
                last_posts = json.load(f)
                if not isinstance(last_posts, dict):
                    last_posts = {}
            except json.JSONDecodeError:
                last_posts = {}
    else:
        last_posts = {}

    for rss_url, owner in RSS_FEEDS.items():
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            continue
        
        # 해당 블로그에서 마지막으로 확인했던 글의 링크
        last_link = last_posts.get(rss_url)
        
        # 새 글들만 필터링 (최신순이므로 뒤집어서 오래된 글부터 처리)
        new_entries = []
        for entry in feed.entries:
            if entry.link == last_link:
                break
            new_entries.append(entry)
        
        # 전송 처리 (오래된 순서대로 전송)
        for entry in reversed(new_entries):
            link = entry.link
            
            raw_title = entry.get('title', '제목 없음')
            clean_title = html.unescape(raw_title)

            raw_desc = entry.get('description', '')
            clean_desc = re.sub(r'<[^>]+>', '', raw_desc)
            clean_desc = html.unescape(clean_desc).strip()
            clean_desc = (clean_desc[:1500] + '...') if len(clean_desc) > 1500 else clean_desc

            if "blog.naver.com" in link:
                link = link.split('?')[0]

            print(f"새로운 글 전송 중: {clean_title} (작성자: {owner})")
            
            if entry.get('published_parsed'):
                published_date = time.strftime('%Y-%m-%d %H:%M:%S', entry.published_parsed)
            else:
                published_date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())

            status = add_to_google_sheet(clean_title, link, owner, published_date, clean_desc)
            
            if status == 200:
                # 전송 성공 시, 해당 블로그의 최신 링크를 업데이트
                last_posts[rss_url] = link
            else:
                print(f"전송 실패: {status}")
            
            time.sleep(0.3)

        # 만약 해당 블로그에 처음 접근한 경우라면, 현재의 최신 글을 마지막 글로 저장 (다음 실행부터 체크)
        if rss_url not in last_posts and feed.entries:
            last_posts[rss_url] = feed.entries[0].link

    # 2. 업데이트된 마지막 전송 정보 저장
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(last_posts, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    check_feeds()
