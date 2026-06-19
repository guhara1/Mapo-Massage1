#!/usr/bin/env python3
"""(선택) 구글 Indexing API 통보 — urlNotifications.publish.

⚠️ 중요: 구글 Indexing API 는 공식적으로 JobPosting / BroadcastEvent 구조화
데이터가 있는 페이지만 지원합니다. 일반 안내 페이지는 이 API 대신
Google Search Console 에 사이트를 등록하고 sitemap.xml 을 제출하는 것이
정식 경로입니다. (빙·네이버는 tools/indexnow.py 로 즉시 통보됩니다.)

그래도 구글에 변경을 빠르게 알리고 싶을 때 쓸 수 있도록 스크립트를 둡니다.

사전 준비
---------
1) Google Cloud 프로젝트에서 "Indexing API" 활성화
2) 서비스 계정 생성 → JSON 키 다운로드
3) Search Console 속성에 그 서비스 계정 이메일을 "소유자"로 추가
4) 의존성 설치:  pip install -r tools/requirements.txt
5) 실행:
     export GOOGLE_APPLICATION_CREDENTIALS=/path/service_account.json
     python tools/google_indexing.py            # sitemap 전체
     python tools/google_indexing.py /seoul/mapo/sangam-dong-chuljangmassage/
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = BASE_URL.rstrip("/")
SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


def urls_from_sitemap():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python build.py` 를 실행하세요.")
    return re.findall(r"<loc>(.*?)</loc>", open(path, encoding="utf-8").read())


def normalize(arg):
    if arg.startswith("http"):
        return arg
    return BASE + "/" + arg.lstrip("/")


def main():
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("의존성 필요:  pip install -r tools/requirements.txt")

    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path or not os.path.exists(cred_path):
        sys.exit("GOOGLE_APPLICATION_CREDENTIALS 환경변수에 서비스 계정 JSON 경로를 지정하세요.")

    args = sys.argv[1:]
    urls = [normalize(a) for a in args] if args else urls_from_sitemap()

    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    session = AuthorizedSession(creds)

    ok = 0
    for u in urls:
        r = session.post(ENDPOINT, json={"url": u, "type": "URL_UPDATED"}, timeout=30)
        mark = "OK" if r.status_code == 200 else "!!"
        print(f"[{mark}] {u} -> {r.status_code} {r.text[:160]}")
        if r.status_code == 200:
            ok += 1
    print(f"\n완료: {ok}/{len(urls)} 통보. (구글 일반 색인은 Search Console + sitemap 이 정식 경로)")


if __name__ == "__main__":
    main()
