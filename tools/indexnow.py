#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보 — 빙(Bing)·네이버(Naver)·Yandex 등.

IndexNow는 한 곳에 제출하면 참여 검색엔진끼리 공유하지만, 확실하게 하려고
빙·네이버 엔드포인트에 함께 통보한다. (구글은 IndexNow 미참여 → tools/google_indexing.py 참고)

사용법
------
  # 전체 일괄 통보 (sitemap.xml 기준)
  python tools/indexnow.py

  # 새 글/수정 글만 즉시 통보
  python tools/indexnow.py https://mapo-massage1.netlify.app/seoul/mapo/sangam-dong-chuljangmassage/
  python tools/indexnow.py /seoul/mapo/sangam-dong-chuljangmassage/   # 경로만 줘도 됨

  # 미리보기(실제 전송 안 함)
  python tools/indexnow.py --dry-run

표준 라이브러리만 사용하므로 별도 설치가 필요 없다.
빌드 후 루트의 "{KEY}.txt" 파일이 배포돼 있어야 통보가 인증된다.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = BASE_URL.rstrip("/")
HOST = re.sub(r"^https?://", "", BASE).split("/")[0]
KEY_LOCATION = f"{BASE}/{INDEXNOW_KEY}.txt"

# IndexNow 참여 엔드포인트 (서로 공유되지만 명시적으로 함께 통보)
ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://searchadvisor.naver.com/indexnow",
    "https://yandex.com/indexnow",
]


def urls_from_sitemap():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python build.py` 를 실행하세요.")
    xml = open(path, encoding="utf-8").read()
    return re.findall(r"<loc>(.*?)</loc>", xml)


def normalize(arg):
    if arg.startswith("http://") or arg.startswith("https://"):
        return arg
    return BASE + "/" + arg.lstrip("/")


def submit(endpoint, url_list):
    payload = json.dumps({
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": url_list,
    }).encode("utf-8")
    req = urllib.request.Request(
        endpoint, data=payload, method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read(200).decode("utf-8", "ignore").strip()
    except urllib.error.HTTPError as e:
        return e.code, e.read(200).decode("utf-8", "ignore").strip()
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv

    urls = [normalize(a) for a in args] if args else urls_from_sitemap()
    if not urls:
        sys.exit("통보할 URL 이 없습니다.")

    print(f"호스트     : {HOST}")
    print(f"키 위치    : {KEY_LOCATION}")
    print(f"URL 개수   : {len(urls)}")
    for u in urls[:8]:
        print(f"  - {u}")
    if len(urls) > 8:
        print(f"  … 외 {len(urls) - 8}건")

    if dry:
        print("\n[--dry-run] 실제 전송하지 않았습니다.")
        return

    print()
    ok = 0
    for ep in ENDPOINTS:
        status, body = submit(ep, urls)
        # 200/202 = 정상 접수, 4xx 는 메시지 확인
        mark = "OK" if status in (200, 202) else "!!"
        print(f"[{mark}] {ep} -> {status} {body}")
        if status in (200, 202):
            ok += 1
    print(f"\n완료: {ok}/{len(ENDPOINTS)} 엔드포인트 접수.")


if __name__ == "__main__":
    main()
