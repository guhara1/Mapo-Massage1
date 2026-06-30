# 이용 후기 + 집계 평점 데이터.
# 화면 표시(visible)와 구조화 데이터(schema.org AggregateRating·Review)에 함께 쓰인다.
#
# ⚠️ 중요: 아래 후기는 페이지 구성을 위한 "대표 예시"입니다.
#    about 페이지의 '허위 후기·가짜 체험담 미사용' 운영 기준과 구글 구조화 데이터
#    가이드라인(실제 수집한 후기만 마크업)을 지키려면, 반드시 실제로 받은 후기로
#    교체해 운영하세요. 실제 후기가 없다면 REVIEWS 를 비우면 후기 섹션과
#    AggregateRating·Review 스키마가 모두 자동으로 출력되지 않습니다.

# 집계 평점 — 실제 수집 데이터로 갱신하세요.
RATING_VALUE = "4.9"
RATING_BEST = "5"
RATING_WORST = "1"

# 대표 후기(예시). 실제 후기로 교체 운영.
REVIEWS = [
    {
        "author": "김○○",
        "rating": 5,
        "date": "2026-05-18",
        "body": "예약한 시간에 정확히 도착했고 응대가 친절했습니다. 집으로 방문받는 게 처음이라 걱정했는데 준비물 안내까지 꼼꼼해서 편하게 받았어요.",
    },
    {
        "author": "이○○",
        "rating": 5,
        "date": "2026-04-30",
        "body": "비용을 예약 때 총액으로 먼저 알려줘서 추가 요금 걱정이 없었습니다. 90분 코스 받았는데 어깨가 한결 가벼워졌어요.",
    },
    {
        "author": "박○○",
        "rating": 5,
        "date": "2026-04-11",
        "body": "야근 끝나고 늦은 시간에 연락했는데 가능한 시간대를 바로 확인해줘서 좋았습니다. 오피스텔 출입 안내도 미리 챙겨주셨어요.",
    },
    {
        "author": "최○○",
        "rating": 4,
        "date": "2026-03-22",
        "body": "주말이라 도착까지 조금 기다렸지만 미리 예상 시간을 알려줘서 괜찮았습니다. 관리 자체는 만족스러웠어요.",
    },
    {
        "author": "정○○",
        "rating": 5,
        "date": "2026-03-05",
        "body": "부모님 댁으로 예약해드렸는데 시간 맞춰 방문하고 정중하게 응대해주셔서 감사했습니다. 다음에 또 이용할게요.",
    },
]

# 표시용 집계 개수 — 실제 후기 수에 맞춰 갱신하세요.
RATING_COUNT = len(REVIEWS)


def _stars(n: int) -> str:
    n = max(0, min(5, int(round(n))))
    return "★" * n + "☆" * (5 - n)


def reviews_section() -> str:
    """페이지 본문에 들어갈 '이용 후기' 섹션(HTML). 후기가 없으면 빈 문자열."""
    if not REVIEWS:
        return ""
    cards = []
    for r in REVIEWS:
        cards.append(
            '<li class="review-card">'
            '<div class="review-head">'
            f'<span class="review-author">{r["author"]}</span>'
            f'<span class="review-stars" aria-label="별점 {r["rating"]}점">{_stars(r["rating"])}</span>'
            '</div>'
            f'<p class="review-body">{r["body"]}</p>'
            f'<time class="review-date" datetime="{r["date"]}">{r["date"]}</time>'
            '</li>'
        )
    return (
        '<section id="reviews" class="reviews">'
        '<h2>이용 후기</h2>'
        '<p class="reviews-summary">'
        f'<span class="reviews-score">{RATING_VALUE}</span>'
        f'<span class="reviews-stars" aria-hidden="true">{_stars(float(RATING_VALUE))}</span>'
        f'<span class="reviews-count">고객 후기 {RATING_COUNT}건 기준</span>'
        '</p>'
        '<ul class="review-list">' + "".join(cards) + '</ul>'
        '<p class="reviews-note">후기는 실제 이용 고객의 동의를 받아 게시하며, 개인정보 보호를 위해 이름은 일부만 표기합니다.</p>'
        '</section>'
    )
