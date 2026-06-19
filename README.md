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

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경
2. `content/site.py`의 텔레그램 링크를 실제 채널 주소로 변경
3. `python3 build.py` 재실행 (canonical·sitemap·robots.txt에 반영됨)
4. Google Search Console에 `sitemap.xml` 제출
