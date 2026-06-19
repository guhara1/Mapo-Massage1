# 바로GO — 마포구 출장마사지·홈타이 안내 사이트

서울 마포구 전지역 방문 관리(출장마사지·홈타이) 안내용 정적 사이트입니다.
상호: **바로GO** · 전화예약: **0508-202-4719**

## 구조

- 정적 HTML 사이트 — 어느 호스팅(GitHub Pages, Netlify, 일반 웹서버)에서든 그대로 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함

```
build.py            # 빌드 스크립트 (레이아웃·글자수 검사·sitemap 생성)
content/
  site.py           # 상호·전화·텔레그램·BASE_URL·메뉴 구조
  main.py           # 메인 페이지 (+ Organization/WebPage/BreadcrumbList/FAQPage JSON-LD)
  areas.py          # 지역별: 마포구 허브 + 대표 행정동 14개
  stations.py       # 역세권별: 허브 + 역 14개 (가좌역 인접 생활권 포함)
  districts.py      # 생활권별: 허브 + 생활권 10개
  info.py           # 예약 안내·이용 전 확인사항·홈타이 가이드·고객센터·약관
  about.py          # 사이트 소개·운영 기준 (E-E-A-T)
  pricing.py        # 공용 요금 블록
assets/             # CSS(프리미엄 토큰 + 컴포넌트 오버레이), 모바일 내비 JS
```

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수 리포트가 출력됩니다.

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 고유 글자수(공용 요금 블록 제외)가 기준치 미만이면 자동 `noindex` + sitemap 제외
- 지역은 대표 행정동 14개만 — 망원1·2동→망원동, 성산1·2동→성산동으로 통합, 번호 동 개별 페이지 없음
- 법정동(창전·하중·당인·노고산·동교 등)은 대표 동 본문에서 보조 설명, 단독 페이지 없음
- 역은 역 1개당 페이지 1개 — 환승역(홍대입구·합정·공덕·디지털미디어시티)도 URL 하나, 노선별/출구별 페이지 없음
- 가좌역은 서대문·마포 경계 성격이라 연남·성산 인접 생활권으로 처리
- 모든 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음)
- 메타 디스크립션은 80자 이내

## 브랜딩·문의

- 상호 바로GO, 전화예약 0508-202-4719 (`content/site.py`)
- 푸터의 **웹사이트 제작문의 / 제휴문의** 오렌지 버튼은 텔레그램으로 연결
  (`TELEGRAM_BUILD`, `TELEGRAM_PARTNER` 값을 실제 채널로 변경)

## 색인(인덱싱) 자동화

빌드 시 색인용 파일이 자동 생성됩니다.

- `sitemap.xml` — `lastmod`·`changefreq`·`priority` 포함 (메인 1.0 / 그 외 0.8)
- `rss.xml` — 색인 대상 페이지 피드 (빠른 발견용, `<head>`에 alternate 링크)
- `robots.txt` — 전체 허용 + 구글봇·네이버 Yeti·빙봇 명시 + 사이트맵
- `{INDEXNOW_KEY}.txt` — IndexNow 소유 확인 키 파일 (루트)

### IndexNow — 빙·네이버 즉시 통보 (글 올릴 때마다)

IndexNow는 빙·네이버·Yandex가 참여합니다(구글은 미참여).
표준 라이브러리만 쓰므로 설치가 필요 없습니다.

```bash
# 전체 일괄 통보 (최초 1회 / 사이트맵 기준)
python3 tools/indexnow.py

# 새 글·수정 글만 즉시 통보
python3 tools/indexnow.py /seoul/mapo/sangam-dong-chuljangmassage/

# 미리보기
python3 tools/indexnow.py --dry-run
```

> 통보가 인증되려면 배포된 사이트 루트에 `{INDEXNOW_KEY}.txt`가 떠 있어야 합니다.
> 키 변경 시 `content/site.py`의 `INDEXNOW_KEY`만 바꾸고 다시 빌드하세요.

### 구글 — 정식 경로

구글 일반 페이지 색인의 정식 경로는 **Search Console 등록 + `sitemap.xml` 제출**입니다.
(구글 Indexing API는 공식적으로 JobPosting/BroadcastEvent 전용이며, 일반 페이지 통보는
`tools/google_indexing.py`로 시도할 수 있으나 보조 수단입니다. `pip install -r tools/requirements.txt` 필요.)

> 참고: 과거의 `google.com/ping?sitemap=`, 빙 ping 엔드포인트는 2023년 폐지되어 동작하지 않습니다.
> 그래서 빙·네이버는 IndexNow, 구글은 Search Console 경로를 사용합니다.

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경 (현재 `https://mapo-massage1.pages.dev`)
2. `content/site.py`의 텔레그램 링크를 실제 채널 주소로 변경
3. `python3 build.py` 재실행 (canonical·sitemap·rss·robots·IndexNow 키에 반영됨)
4. **네이버 서치어드바이저**: 메인페이지 메타 태그로 소유확인 → 사이트 등록 → `sitemap.xml` 제출
5. **구글 Search Console**: 사이트 등록 → `sitemap.xml` 제출
6. 배포 후 `python3 tools/indexnow.py` 1회 실행 → 빙·네이버 일괄 통보
