#!/usr/bin/env python3
"""바로GO 마포 출장마사지 — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 고유 텍스트(공용 요금 블록 제외)가 기준치 미만이면 robots noindex 처리.
    한글은 음절 밀도가 높아 영문 단어 기준보다 글자수가 적게 잡히므로,
    공용 요금·CTA를 제외한 1,150자를 색인 기준으로 둔다.
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 번호 행정동·역+테마 조합 경로는 생성 자체가 불가능한 구조
"""
import html
import os
import re
import shutil
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.site import (BASE_URL, BRAND, NAV, PHONE, PHONE_DISPLAY,
                         TELEGRAM_BUILD, TELEGRAM_PARTNER, INDEXNOW_KEY)
from content import reviews as REVIEWS_MOD

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 1150
BASE = BASE_URL.rstrip("/")
OG_IMAGE = f"{BASE}/assets/og-image.png"

# 코스별 기본 요금(스키마 Offer 용) — content/pricing.py 의 표시 요금과 일치시킨다.
COURSE_OFFERS = [
    ("60분 코스", "90000"),
    ("90분 코스", "150000"),
    ("120분 코스", "180000"),
]

# 후기·스키마를 넣지 않는 페이지(정책·소개 성격)
NO_REVIEW_PATHS = {"about/", "support/privacy/", "support/terms/"}
# 롱테일 내부링크를 넣지 않는 페이지(법적 고지 성격)
NO_RELATED_PATHS = {"support/privacy/", "support/terms/"}

# 메인·허브에서 밀어주는 인기 지역(롱테일 앵커) — 자기 자신은 렌더 시 제외한다.
POPULAR_LONGTAIL = [
    ("/seoul/mapo/hongik-univ-station-chuljangmassage/", "홍대입구역 출장마사지 24시간 방문 예약"),
    ("/seoul/mapo/gongdeok-dong-chuljangmassage/", "공덕동 출장마사지 업무지구 홈타이"),
    ("/seoul/mapo/hapjeong-dong-chuljangmassage/", "합정동 출장마사지 심야 방문 안내"),
    ("/seoul/mapo/mangwon-dong-chuljangmassage/", "망원동 홈타이 가족 방문 후기"),
    ("/seoul/mapo/yeonnam-dong-chuljangmassage/", "연남동 출장마사지 경의선숲길 생활권"),
    ("/seoul/mapo/sangam-dmc-area-chuljangmassage/", "상암DMC 출장마사지 오피스 방문"),
    ("/seoul/mapo/seogyo-dong-chuljangmassage/", "서교동 홍대 상권 출장마사지 가격"),
    ("/seoul/mapo/mapo-station-chuljangmassage/", "마포역 출장마사지 한강권 홈타이"),
]


def jsonld_escape(text: str) -> str:
    """JSON 문자열 값 안에서 깨지지 않도록 최소 이스케이프."""
    return (
        text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
        .strip()
    )


def page_name(page: dict) -> str:
    """페이지 대표 이름(지역명 등). 브레드크럼 마지막 항목 우선."""
    crumbs = page.get("breadcrumb") or []
    if crumbs:
        return crumbs[-1][0]
    return BRAND


def is_leaf_region(path: str) -> bool:
    return path.startswith("seoul/mapo/") and path.endswith("-chuljangmassage/")


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


def extract_faqs(body: str):
    """본문의 .faq-item 블록에서 (질문, 답변) 쌍을 추출한다."""
    faqs = []
    for block in re.findall(r'<div class="faq-item">(.*?)</div>', body, flags=re.S):
        qm = re.search(r"<h3>(.*?)</h3>", block, flags=re.S)
        am = re.search(r"<p>(.*?)</p>", block, flags=re.S)
        if qm and am:
            q = re.sub(r"<[^>]+>", "", qm.group(1))
            a = re.sub(r"<[^>]+>", "", am.group(1))
            q = html.unescape(re.sub(r"\s+", " ", q)).strip()
            a = html.unescape(re.sub(r"\s+", " ", a)).strip()
            if q and a:
                faqs.append((q, a))
    return faqs


def render_related(page: dict) -> str:
    """롱테일 주제 내부링크 섹션. 메인 포함 모든 안내 페이지에 출력."""
    path = page["path"]
    if path in NO_RELATED_PATHS:
        return ""
    name = page_name(page) if is_leaf_region(path) else "마포구"
    cur = "/" + path

    # 1) 페이지 이름을 엮은 주제(롱테일) 링크 — 페이지마다 앵커가 달라진다.
    topic = [
        ("/reservation/", f"{name} 출장마사지 예약 방법·가능 시간"),
        ("/guide/#cost", f"{name} 홈타이 추가 비용 확인 기준"),
        ("/checklist/", f"{name} 방문 전 확인사항 체크리스트"),
        ("/guide/", f"{name} 홈타이란? 이용 가이드"),
        ("/reservation/#payment", f"{name} 출장마사지 결제 방식 안내"),
        ("/seoul/mapo/", f"{name} 포함 마포구 전지역 안내"),
    ]
    topic_links = "".join(
        f'<li><a href="{href}">{label}</a></li>'
        for href, label in topic if href != cur
    )

    # 2) 인기 지역 롱테일 바로가기 — 자기 자신 제외, 최대 6개.
    pop = [(h, l) for h, l in POPULAR_LONGTAIL if h != cur][:6]
    pop_links = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in pop)

    return (
        '<section class="related-links" aria-label="함께 보면 좋은 안내">'
        '<h2>함께 많이 찾는 안내</h2>'
        '<div class="related-grid">'
        '<div class="related-col">'
        f'<p class="related-title">{name} 이용 안내</p>'
        f'<ul>{topic_links}</ul>'
        '</div>'
        '<div class="related-col">'
        '<p class="related-title">마포구 인기 지역 바로가기</p>'
        f'<ul>{pop_links}</ul>'
        '</div>'
        '</div>'
        '</section>'
    )


def render_schema(page: dict, canonical: str) -> str:
    """페이지별 구조화 데이터(JSON-LD). 브레드크럼·지역 서비스(평점·후기)·FAQ."""
    path = page["path"]
    name = page_name(page)
    blocks = []

    # BreadcrumbList — 브레드크럼이 있는 페이지(메인 제외)
    crumbs = page.get("breadcrumb") or []
    if crumbs:
        items = [f'{{ "@type": "ListItem", "position": 1, "name": "홈", "item": "{BASE}/" }}']
        pos = 2
        for label, href in crumbs:
            item = (BASE + href) if href else canonical
            items.append(
                f'{{ "@type": "ListItem", "position": {pos}, '
                f'"name": "{jsonld_escape(label)}", "item": "{item}" }}'
            )
            pos += 1
        blocks.append(
            '<script type="application/ld+json">\n'
            '{ "@context": "https://schema.org", "@type": "BreadcrumbList",'
            ' "itemListElement": [' + ", ".join(items) + "] }\n</script>"
        )

    # LocalBusiness (+ 평점·후기 + 코스 Offer)
    show_reviews = path not in NO_REVIEW_PATHS and bool(REVIEWS_MOD.REVIEWS)
    area = "서울특별시 마포구" + (f" {name}" if is_leaf_region(path) else "")
    biz_name = f"{BRAND} — {name} 출장마사지·홈타이" if is_leaf_region(path) else f"{BRAND} 마포구 출장마사지·홈타이"

    offers = ", ".join(
        '{ "@type": "Offer", "name": "%s", "price": "%s", "priceCurrency": "KRW", '
        '"availability": "https://schema.org/InStock" }' % (n, p)
        for n, p in COURSE_OFFERS
    )

    biz = [
        '"@context": "https://schema.org"',
        '"@type": "LocalBusiness"',
        '"@id": "%s#business"' % canonical,
        '"name": "%s"' % jsonld_escape(biz_name),
        '"url": "%s"' % canonical,
        '"telephone": "%s"' % PHONE,
        '"image": "%s"' % OG_IMAGE,
        '"priceRange": "₩₩"',
        '"currenciesAccepted": "KRW"',
        '"openingHours": "Mo-Su 00:00-24:00"',
        '"areaServed": { "@type": "AdministrativeArea", "name": "%s" }' % area,
        '"address": { "@type": "PostalAddress", "addressRegion": "서울특별시", '
        '"addressLocality": "마포구", "addressCountry": "KR" }',
        '"makesOffer": [%s]' % offers,
    ]
    if show_reviews:
        biz.append(
            '"aggregateRating": { "@type": "AggregateRating", '
            '"ratingValue": "%s", "reviewCount": "%s", "bestRating": "%s", "worstRating": "%s" }'
            % (REVIEWS_MOD.RATING_VALUE, REVIEWS_MOD.RATING_COUNT,
               REVIEWS_MOD.RATING_BEST, REVIEWS_MOD.RATING_WORST)
        )
        rev_nodes = []
        for r in REVIEWS_MOD.REVIEWS:
            rev_nodes.append(
                '{ "@type": "Review", '
                '"author": { "@type": "Person", "name": "%s" }, '
                '"datePublished": "%s", '
                '"reviewRating": { "@type": "Rating", "ratingValue": "%s", "bestRating": "5", "worstRating": "1" }, '
                '"reviewBody": "%s" }'
                % (jsonld_escape(r["author"]), r["date"], r["rating"], jsonld_escape(r["body"]))
            )
        biz.append('"review": [%s]' % ", ".join(rev_nodes))
    blocks.append(
        '<script type="application/ld+json">\n{' + ", ".join(biz) + "}\n</script>"
    )

    # FAQPage — 본문 .faq-item 자동 추출(이미 FAQ 스키마가 있는 메인은 추출 결과 없음)
    faqs = extract_faqs(page["body"])
    if faqs:
        q_nodes = ", ".join(
            '{ "@type": "Question", "name": "%s", "acceptedAnswer": '
            '{ "@type": "Answer", "text": "%s" } }'
            % (jsonld_escape(q), jsonld_escape(a))
            for q, a in faqs
        )
        blocks.append(
            '<script type="application/ld+json">\n'
            '{ "@context": "https://schema.org", "@type": "FAQPage", '
            '"mainEntity": [' + q_nodes + "] }\n</script>"
        )

    return "\n".join(blocks) + "\n"


def augment_body(page: dict) -> str:
    """본문에 '이용 후기'와 '함께 많이 찾는 안내(롱테일 내부링크)'를 끼워 넣는다.
    공용 요금 블록(pricing) 앞, 없으면 CTA 앞, 그래도 없으면 끝에 붙인다."""
    path = page["path"]
    body = page["body"]
    extra = ""
    if path not in NO_REVIEW_PATHS and REVIEWS_MOD.REVIEWS:
        extra += REVIEWS_MOD.reviews_section()
    extra += render_related(page)
    if not extra:
        return body
    idx = body.find('<section class="pricing">')
    if idx == -1:
        idx = body.find('<section class="cta">')
    if idx == -1:
        return body + extra
    return body[:idx] + extra + body[idx:]


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    crumbs = page.get("breadcrumb") or []
    hero = page.get("hero", "")
    canonical = BASE + "/" + path

    # 후기·롱테일 내부링크 섹션을 본문에 주입(이후 색인 글자수 계산과 일치하도록 mutate).
    page["body"] = augment_body(page)
    body = page["body"]

    # 페이지별 구조화 데이터(JSON-LD)를 head 에 더한다.
    extra_head = page.get("extra_head", "") + render_schema(page, canonical)

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{BRAND} 최신 안내" href="{BASE_URL.rstrip('/')}/rss.xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#100e16">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">바</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 마포구 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">마포구 전지역 방문 출장마사지·홈타이 안내 사이트입니다. 모든 서비스는 안내된 관리 범위와 위생·안전 기준 안에서만 제공됩니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">예약전화</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 서울특별시 마포구 전지역</span>
      </address>
      <div class="footer-cta">
        <a class="footer-btn" href="{TELEGRAM_BUILD}" target="_blank" rel="noopener nofollow">웹사이트 제작문의 ↗</a>
        <a class="footer-btn" href="{TELEGRAM_PARTNER}" target="_blank" rel="noopener nofollow">제휴문의 ↗</a>
      </div>
    </div>
    <nav class="footer-col" aria-label="지역 안내">
      <p class="footer-title">지역 안내</p>
      <ul>
        <li><a href="/seoul/mapo/">지역별 안내</a></li>
        <li><a href="/seoul/mapo/stations/">역세권 안내</a></li>
        <li><a href="/seoul/mapo/districts/">생활권 안내</a></li>
        <li><a href="/seoul/mapo/gongdeok-dong-chuljangmassage/">공덕동 출장마사지</a></li>
        <li><a href="/seoul/mapo/hongik-univ-station-chuljangmassage/">홍대입구역 출장마사지</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약 안내</a></li>
        <li><a href="/checklist/">이용 전 확인사항</a></li>
        <li><a href="/guide/">홈타이 이용 가이드</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/support/#faq">자주 묻는 질문</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/about/">사이트 소개·운영 기준</a></li>
        <li><a href="/support/privacy/">개인정보 처리방침</a></li>
        <li><a href="/support/terms/">이용약관</a></li>
        <li><a href="/checklist/#safety">고객 안전 안내</a></li>
        <li><a href="/support/#biz">제휴·기업 문의</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <div class="footer-made-group">
        <a class="footer-made" href="{TELEGRAM_BUILD}" target="_blank" rel="noopener nofollow">웹사이트 제작문의 ↗</a>
        <a class="footer-made" href="{TELEGRAM_PARTNER}" target="_blank" rel="noopener nofollow">제휴문의 ↗</a>
      </div>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def build() -> None:
    report = []
    indexed = []  # (loc, title, desc)
    base = BASE_URL.rstrip("/")
    now = datetime.now(timezone.utc)
    lastmod = now.strftime("%Y-%m-%d")
    rfc822 = now.strftime("%a, %d %b %Y %H:%M:%S +0000")

    for page in PAGES:
        path = page["path"]  # "" 또는 "seoul/mapo/..." 형태
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            indexed.append((base + "/" + path, page["title"], page["desc"]))
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    # sitemap.xml — 메인 우선순위 1.0, 그 외 0.8, lastmod 포함
    rows = []
    for loc, _, _ in indexed:
        is_home = loc.rstrip("/") == base
        prio = "1.0" if is_home else "0.8"
        freq = "daily" if is_home else "weekly"
        rows.append(
            f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod>"
            f"<changefreq>{freq}</changefreq><priority>{prio}</priority></url>"
        )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n"
        )

    # rss.xml — 색인 대상 페이지 피드(빠른 발견용)
    items = []
    for loc, title, desc in indexed:
        items.append(
            "    <item>\n"
            f"      <title>{html.escape(title)}</title>\n"
            f"      <link>{loc}</link>\n"
            f"      <guid isPermaLink=\"true\">{loc}</guid>\n"
            f"      <description>{html.escape(desc)}</description>\n"
            f"      <pubDate>{rfc822}</pubDate>\n"
            "    </item>"
        )
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "  <channel>\n"
            f"    <title>{html.escape(BRAND)} — 마포구 출장마사지·홈타이 안내</title>\n"
            f"    <link>{base}/</link>\n"
            f"    <atom:link href=\"{base}/rss.xml\" rel=\"self\" type=\"application/rss+xml\" />\n"
            "    <description>마포구 출장마사지·홈타이 지역·역세권·생활권 안내</description>\n"
            "    <language>ko-KR</language>\n"
            f"    <lastBuildDate>{rfc822}</lastBuildDate>\n"
            + "\n".join(items) + "\n"
            "  </channel>\n</rss>\n"
        )

    # robots.txt — 전체 허용 + 주요 봇 명시(구글봇·네이버 Yeti·빙봇·다음) + 사이트맵
    # 빠른 색인을 위해 색인 봇을 막지 않고 사이트맵 위치를 명시한다.
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\nAllow: /\n\n"
            "User-agent: Googlebot\nAllow: /\n\n"
            "User-agent: Googlebot-Image\nAllow: /\n\n"
            "User-agent: Yeti\nAllow: /\n\n"          # 네이버
            "User-agent: Daumoa\nAllow: /\n\n"        # 다음/카카오
            "User-agent: bingbot\nAllow: /\n\n"
            f"Sitemap: {base}/sitemap.xml\n"
        )

    # IndexNow 키 파일 — 빙·네이버 소유 확인용 (루트에 {키}.txt)
    with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY + "\n")

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(indexed)} in sitemap/rss.")
    print(f"IndexNow key file: /{INDEXNOW_KEY}.txt")


if __name__ == "__main__":
    build()
