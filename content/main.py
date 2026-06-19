# 메인 페이지 — 허브 역할. 모든 키워드를 밀어 넣지 않고 상세 페이지로 연결한다.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY
from .pricing import PRICING

_OG = f"{BASE_URL.rstrip('/')}/assets/og-image.png"

# 네이버 서치어드바이저 사이트 소유 확인 — 메인페이지에만 출력
_NAVER_VERIFY = '<meta name="naver-site-verification" content="39e28f0359ad150d262d5f11cf62f534f741ed1e" />\n'

_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{BRAND}",
  "url": "{BASE_URL}/",
  "telephone": "{PHONE}",
  "image": {{
    "@type": "ImageObject",
    "url": "{_OG}",
    "width": 1200,
    "height": 630
  }},
  "logo": "{BASE_URL.rstrip('/')}/assets/icon-512.png",
  "description": "마포구 출장마사지·홈타이 방문 관리 지역 안내",
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "서울특별시 마포구"
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "마포구 출장마사지·홈타이 지역별 예약 안내",
  "url": "{BASE_URL}/",
  "description": "마포구 출장마사지·홈타이 예약 전 홍대, 합정, 공덕, 상암 생활권을 확인하세요.",
  "primaryImageOfPage": {{
    "@type": "ImageObject",
    "url": "{_OG}",
    "width": 1200,
    "height": 630
  }},
  "inLanguage": "ko-KR",
  "isPartOf": {{ "@type": "WebSite", "name": "{BRAND}", "url": "{BASE_URL}/" }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "홈", "item": "{BASE_URL}/" }},
    {{ "@type": "ListItem", "position": 2, "name": "마포구 출장마사지", "item": "{BASE_URL}/" }}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "마포구 전지역 방문이 가능한가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "예약 시간과 정확한 위치, 배정 상황에 따라 가능 여부가 달라집니다. 지역별 안내에서 공덕동, 서교동, 합정동, 망원동, 연남동, 성산동, 상암동 등 대표 행정동 기준으로 확인할 수 있습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "망원1동·망원2동은 왜 따로 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "망원1동과 망원2동은 망원동 대표 페이지로, 성산1동과 성산2동은 성산동 대표 페이지로 통합해 안내합니다. 같은 생활권을 잘게 쪼개 비슷한 내용을 반복하지 않기 위함입니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "홍대입구역·합정역 같은 환승역도 안내하나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "환승역도 역명 기준 1개 페이지만 운영하며 본문에서 환승 특징을 설명합니다. 노선별로 페이지를 나누지 않습니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "홈타이와 출장마사지는 어떻게 다른가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "홈타이는 집에서 받는 타이마사지를 가리키는 방문형 관리의 한 형태입니다. 차이와 이용 기준은 홈타이 이용 가이드에서 확인할 수 있습니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 마포구 전지역</p>
    <h1>마포구 출장마사지·홈타이<br>지역별 예약 안내</h1>
    <p class="hero-lead">홍대·합정·공덕·상암까지, 계신 곳으로 찾아가는 방문형 관리.<br>현재 위치 기준으로 대표 행정동과 역세권, 예약 전 확인사항을 먼저 확인하세요.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/seoul/mapo/">지역별 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>14곳</strong><span>대표 행정동</span></li>
      <li><strong>14곳</strong><span>역세권 안내</span></li>
      <li><strong>10곳</strong><span>생활권 안내</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="standard">
<h2>마포구에서 출장마사지를 찾을 때 먼저 확인할 기준</h2>
<p>마포구 출장마사지를 찾는 분들은 보통 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 마포구는 서울 서북권과 도심을 연결하는 지역으로, 홍대입구역을 중심으로 한 상권, 합정역과 상수역 주변의 생활권, 공덕역과 마포역 주변의 업무지구, 상암DMC와 월드컵경기장 주변의 업무·문화 생활권이 함께 있습니다. 그래서 마포구 안내는 단순히 "마포 전지역 가능"만 적기보다 대표 행정동과 역세권, 생활권을 나누어 설명하는 구조가 정확합니다. 이 페이지는 마포구 전체를 설명하는 허브 역할을 하며, 자세한 내용은 지역별·역세권·생활권 안내 페이지에서 확인하실 수 있습니다. {BRAND}는 예약 확인부터 방문 관리까지 정해진 절차에 따라 진행하며, 처음 이용하시는 분도 어렵지 않게 예약할 수 있도록 각 단계를 명확하게 안내해 드립니다.</p>
</section>

<section id="lifezone">
<h2>홍대·합정·공덕·상암 생활권 차이</h2>
<p>마포구는 같은 구 안에서도 생활권마다 검색 의도가 뚜렷하게 다릅니다. 홍대입구역과 서교동, 연남동은 상권과 경의선숲길을 중심으로 한 유동 인구 생활권이고, 합정동과 서강동은 합정역·상수역·광흥창역으로 이어지는 카페·주거 혼합 생활권입니다. 공덕동과 도화동은 마포역·공덕역 업무지구의 직장인 생활권이며, 상암동과 성산동은 디지털미디어시티역과 월드컵경기장을 낀 업무·주거 생활권입니다. 망원동은 홍대·합정과 가깝지만 망원시장과 한강공원을 낀 주거 생활권이라 분위기가 또 다릅니다. 본인 위치와 비슷한 생활권을 먼저 고르면 필요한 정보가 더 빨리 보입니다.</p>
</section>

<section id="areas">
<h2>대표 행정동별 방문 가능 지역 안내</h2>
<p>대표 행정동은 아현동, 공덕동, 도화동, 용강동, 대흥동, 염리동, 신수동, 서강동, 서교동, 합정동, 망원동, 연남동, 성산동, 상암동으로 구성합니다. 공덕동과 도화동은 업무지구와 마포역 인접 생활권을, 서교동과 연남동은 홍대입구역과 경의선숲길 생활권을, 합정동과 서강동은 합정역·상수역·광흥창역 생활권을 중심으로 안내합니다. 망원1동·망원2동은 망원동 대표 페이지로, 성산1동·성산2동은 성산동 대표 페이지로 통합합니다.</p>
<ul class="card-grid">
<li><a href="/seoul/mapo/ahyeon-dong-chuljangmassage/">아현동</a></li>
<li><a href="/seoul/mapo/gongdeok-dong-chuljangmassage/">공덕동</a></li>
<li><a href="/seoul/mapo/dohwa-dong-chuljangmassage/">도화동</a></li>
<li><a href="/seoul/mapo/yonggang-dong-chuljangmassage/">용강동</a></li>
<li><a href="/seoul/mapo/daeheung-dong-chuljangmassage/">대흥동</a></li>
<li><a href="/seoul/mapo/yeomni-dong-chuljangmassage/">염리동</a></li>
<li><a href="/seoul/mapo/sinsu-dong-chuljangmassage/">신수동</a></li>
<li><a href="/seoul/mapo/seogang-dong-chuljangmassage/">서강동</a></li>
<li><a href="/seoul/mapo/seogyo-dong-chuljangmassage/">서교동</a></li>
<li><a href="/seoul/mapo/hapjeong-dong-chuljangmassage/">합정동</a></li>
<li><a href="/seoul/mapo/mangwon-dong-chuljangmassage/">망원동</a></li>
<li><a href="/seoul/mapo/yeonnam-dong-chuljangmassage/">연남동</a></li>
<li><a href="/seoul/mapo/seongsan-dong-chuljangmassage/">성산동</a></li>
<li><a href="/seoul/mapo/sangam-dong-chuljangmassage/">상암동</a></li>
</ul>
<p>마포구 전체 구조가 궁금하시면 <a href="/seoul/mapo/">지역별 안내</a>에서 한눈에 확인하실 수 있습니다.</p>
</section>

<section id="stations">
<h2>홍대입구역·합정역·공덕역·디지털미디어시티역 역세권 안내</h2>
<p>역세권 페이지는 마포구 지역 안내에서 중요한 역할을 합니다. 홍대입구역, 합정역, 공덕역, 마포역, 디지털미디어시티역처럼 실제 검색어와 가까운 기준으로 안내하면 위치 설명이 분명해집니다. 다만 환승역을 노선별로 쪼개면 중복 위험이 커지므로, 홍대입구역·합정역·공덕역·디지털미디어시티역은 역명 기준 1개 페이지만 두고 본문에서 환승 특징을 설명합니다.</p>
<ul class="card-grid">
<li><a href="/seoul/mapo/hongik-univ-station-chuljangmassage/">홍대입구역</a></li>
<li><a href="/seoul/mapo/hapjeong-station-chuljangmassage/">합정역</a></li>
<li><a href="/seoul/mapo/gongdeok-station-chuljangmassage/">공덕역</a></li>
<li><a href="/seoul/mapo/mapo-station-chuljangmassage/">마포역</a></li>
<li><a href="/seoul/mapo/daeheung-station-chuljangmassage/">대흥역</a></li>
<li><a href="/seoul/mapo/gwangheungchang-station-chuljangmassage/">광흥창역</a></li>
<li><a href="/seoul/mapo/sangsu-station-chuljangmassage/">상수역</a></li>
<li><a href="/seoul/mapo/mangwon-station-chuljangmassage/">망원역</a></li>
<li><a href="/seoul/mapo/mapo-gu-office-station-chuljangmassage/">마포구청역</a></li>
<li><a href="/seoul/mapo/world-cup-stadium-station-chuljangmassage/">월드컵경기장역</a></li>
<li><a href="/seoul/mapo/digital-media-city-station-chuljangmassage/">디지털미디어시티역</a></li>
<li><a href="/seoul/mapo/sogang-univ-station-chuljangmassage/">서강대역</a></li>
<li><a href="/seoul/mapo/aeogae-station-chuljangmassage/">애오개역</a></li>
<li><a href="/seoul/mapo/gajwa-nearby-area-chuljangmassage/">가좌역 인접</a></li>
</ul>
<p>생활권 단위로 묶어 보고 싶으시면 <a href="/seoul/mapo/districts/">생활권 안내</a>를 함께 확인해 주세요.</p>
</section>

<section id="check">
<h2>마포구 홈타이 예약 전 확인사항</h2>
<p>마포구 출장마사지 예약 전에는 방문 가능 지역, 예약 가능 시간, 추가 이동비, 결제 방식, 취소 기준, 개인정보 처리 기준을 먼저 확인해야 합니다. 홍대입구역과 합정역처럼 상권 중심 지역은 시간대별 혼잡도가 다를 수 있고, 상암DMC나 공덕 업무지구는 평일 저녁 이동 기준이 달라질 수 있습니다. 마포구 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 확인한 뒤 이용하는 방문형 관리 서비스입니다. 예약 절차는 <a href="/reservation/">예약 안내</a>, 방문 전 준비는 <a href="/checklist/">이용 전 확인사항</a>, 홈타이 자체에 대한 설명은 <a href="/guide/">홈타이 이용 가이드</a>에서 확인하실 수 있습니다.</p>
</section>

<section id="policy">
<h2>마포구 페이지 중복 방지 운영 기준</h2>
<p>이 사이트는 지역명만 바꿔 같은 내용을 반복하는 페이지를 만들지 않습니다. 망원1동·망원2동, 성산1동·성산2동처럼 번호로 나뉜 동은 대표 동 페이지에서 세부 생활권으로 설명하고, 창전동·하중동·당인동 같은 법정동은 서강동 본문에서, 노고산동·동교동 등은 서교동·연남동 본문에서 필요할 때 보조 설명합니다. 환승역은 역명 기준 1개 URL만 만들고, 가좌역은 서대문·마포 경계 성격을 고려해 연남·성산 인접 생활권으로 처리합니다. 페이지 수보다 페이지마다의 정확도를 우선합니다.</p>
</section>

<section id="how">
<h2>마포구 출장마사지 사이트 이용 방법</h2>
<p>이용 방법은 간단합니다. 현재 위치가 행정동으로 익숙하면 <a href="/seoul/mapo/">지역별 안내</a>를, 역 기준이 편하면 <a href="/seoul/mapo/stations/">역세권 안내</a>를, 상권·시장·업무지구처럼 생활권 기준이 익숙하면 <a href="/seoul/mapo/districts/">생활권 안내</a>를 선택하시면 됩니다. 어느 기준으로 들어오셔도 예약 절차와 이용 기준은 동일합니다. 원하는 위치를 고른 뒤 예약 전화로 정확한 주소와 희망 시간을 알려주시면 방문 가능 여부를 바로 확인해 드립니다. 사이트 전체는 정보형 안내 톤을 유지하며, 불법·선정적 표현이나 허위 후기는 사용하지 않습니다.</p>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>마포구 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "마포구 출장마사지｜홍대·합정·공덕·상암 홈타이 지역 안내",
    "desc": "마포구 출장마사지·홈타이 예약 전 홍대, 합정, 공덕, 상암 생활권을 확인하세요.",
    "h1": "마포구 출장마사지 · 마포구 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _NAVER_VERIFY + _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
