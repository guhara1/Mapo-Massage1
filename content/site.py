# 사이트 공통 설정
# 배포 도메인 확정 후 BASE_URL 을 실제 도메인으로 변경하세요.
BASE_URL = "https://mapo-massage1.pages.dev"

BRAND = "바로GO"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 외부 문의 채널 — 텔레그램
TELEGRAM_BUILD = "https://t.me/googleseolab"   # 웹사이트 제작문의
TELEGRAM_PARTNER = "https://t.me/googleseolab"  # 제휴문의

# IndexNow 키 — 빙·네이버 즉시 색인 통보용.
# 빌드 시 루트에 "{INDEXNOW_KEY}.txt" 파일이 생성되며 그 안에 키가 들어간다.
INDEXNOW_KEY = "b1d3ef8652620847220a3db043379c67"

# 상단 메뉴 — 하위 메뉴에는 키워드를 반복하지 않고 지역명·역명만 표시한다.
NAV = [
    ("마포 홈", "/", []),
    ("지역별 안내", "/seoul/mapo/", [
        ("마포구 전체", "/seoul/mapo/"),
        ("아현동", "/seoul/mapo/ahyeon-dong-chuljangmassage/"),
        ("공덕동", "/seoul/mapo/gongdeok-dong-chuljangmassage/"),
        ("도화동", "/seoul/mapo/dohwa-dong-chuljangmassage/"),
        ("용강동", "/seoul/mapo/yonggang-dong-chuljangmassage/"),
        ("대흥동", "/seoul/mapo/daeheung-dong-chuljangmassage/"),
        ("염리동", "/seoul/mapo/yeomni-dong-chuljangmassage/"),
        ("신수동", "/seoul/mapo/sinsu-dong-chuljangmassage/"),
        ("서강동", "/seoul/mapo/seogang-dong-chuljangmassage/"),
        ("서교동", "/seoul/mapo/seogyo-dong-chuljangmassage/"),
        ("합정동", "/seoul/mapo/hapjeong-dong-chuljangmassage/"),
        ("망원동", "/seoul/mapo/mangwon-dong-chuljangmassage/"),
        ("연남동", "/seoul/mapo/yeonnam-dong-chuljangmassage/"),
        ("성산동", "/seoul/mapo/seongsan-dong-chuljangmassage/"),
        ("상암동", "/seoul/mapo/sangam-dong-chuljangmassage/"),
    ]),
    ("역세권 안내", "/seoul/mapo/stations/", [
        ("역 전체", "/seoul/mapo/stations/"),
        ("홍대입구역", "/seoul/mapo/hongik-univ-station-chuljangmassage/"),
        ("합정역", "/seoul/mapo/hapjeong-station-chuljangmassage/"),
        ("공덕역", "/seoul/mapo/gongdeok-station-chuljangmassage/"),
        ("마포역", "/seoul/mapo/mapo-station-chuljangmassage/"),
        ("대흥역", "/seoul/mapo/daeheung-station-chuljangmassage/"),
        ("광흥창역", "/seoul/mapo/gwangheungchang-station-chuljangmassage/"),
        ("상수역", "/seoul/mapo/sangsu-station-chuljangmassage/"),
        ("망원역", "/seoul/mapo/mangwon-station-chuljangmassage/"),
        ("마포구청역", "/seoul/mapo/mapo-gu-office-station-chuljangmassage/"),
        ("월드컵경기장역", "/seoul/mapo/world-cup-stadium-station-chuljangmassage/"),
        ("디지털미디어시티역", "/seoul/mapo/digital-media-city-station-chuljangmassage/"),
        ("서강대역", "/seoul/mapo/sogang-univ-station-chuljangmassage/"),
        ("애오개역", "/seoul/mapo/aeogae-station-chuljangmassage/"),
        ("가좌역 인접", "/seoul/mapo/gajwa-nearby-area-chuljangmassage/"),
    ]),
    ("생활권 안내", "/seoul/mapo/districts/", [
        ("생활권 전체", "/seoul/mapo/districts/"),
        ("홍대입구 상권", "/seoul/mapo/hongdae-area-chuljangmassage/"),
        ("연남동 경의선숲길", "/seoul/mapo/yeonnam-gyeongui-forest-area-chuljangmassage/"),
        ("합정·상수", "/seoul/mapo/hapjeong-sangsu-area-chuljangmassage/"),
        ("공덕·마포 업무지구", "/seoul/mapo/gongdeok-business-area-chuljangmassage/"),
        ("아현·애오개", "/seoul/mapo/ahyeon-aeogae-area-chuljangmassage/"),
        ("대흥·신수", "/seoul/mapo/daeheung-sinsu-area-chuljangmassage/"),
        ("망원시장·망리단길", "/seoul/mapo/mangwon-market-area-chuljangmassage/"),
        ("성산동·마포구청", "/seoul/mapo/seongsan-office-area-chuljangmassage/"),
        ("상암DMC 업무권", "/seoul/mapo/sangam-dmc-area-chuljangmassage/"),
        ("월드컵경기장·하늘공원", "/seoul/mapo/world-cup-park-area-chuljangmassage/"),
    ]),
    ("예약 안내", "/reservation/", [
        ("예약 가능 지역", "/reservation/#place"),
        ("예약 가능 시간", "/reservation/#hours"),
        ("추가 이동비 안내", "/reservation/#move"),
        ("결제 방식 안내", "/reservation/#payment"),
        ("예약 변경 안내", "/reservation/#change"),
        ("취소 기준 안내", "/reservation/#cancel"),
    ]),
    ("이용 전 확인사항", "/checklist/", [
        ("방문 가능 주소 확인", "/checklist/#address"),
        ("자택 이용 전 확인", "/checklist/#home"),
        ("숙소 이용 전 확인", "/checklist/#stay"),
        ("사무실 인근 이용 전 확인", "/checklist/#office"),
        ("개인정보 처리 기준", "/checklist/#privacy"),
        ("고객 안전 안내", "/checklist/#safety"),
    ]),
    ("홈타이 이용 가이드", "/guide/", [
        ("홈타이란?", "/guide/#what"),
        ("출장마사지와 홈타이 차이", "/guide/#diff"),
        ("마포구 홈타이 이용 기준", "/guide/#standard"),
        ("지역별 이동 기준", "/guide/#move"),
        ("추가 비용 확인 기준", "/guide/#cost"),
        ("처음 이용하는 고객 안내", "/guide/#first"),
    ]),
    ("고객센터", "/support/", [
        ("문의하기", "/support/#contact"),
        ("자주 묻는 질문", "/support/#faq"),
        ("운영 기준", "/support/#policy"),
        ("사이트 소개", "/about/"),
        ("개인정보 처리방침", "/support/privacy/"),
        ("이용약관", "/support/terms/"),
    ]),
]
