import re

# 혜택 점수 계산 함수
def calculate_score(benefit, keyword):
    if pd.isna(benefit):
        return 0
    # 키워드가 혜택에 포함되어 있는 경우만 점수 계산
    if keyword not in benefit:
        return 0

    # 숫자 기반 점수 계산 (예: "10% 할인" → 10점)
    match = re.search(r'(\d+)', benefit)
    if match:
        return int(match.group(1))

    # 텍스트 기반 점수 계산
    if "적립" in benefit:
        return 5
    if "할인" in benefit:
        return 7
    return 1

# 복합 키워드 지원 및 최적 카드 추천 함수
def search_card(df, keywords):
    card_scores = {}

    # 각 키워드에 대해 모든 카드 점수 계산
    for keyword in keywords:
        for index, row in df.iterrows():
            card_name = row["카드명"]
            if card_name not in card_scores:
                card_scores[card_name] = 0  # 초기 점수 설정

            # 모든 열(카테고리)에서 점수를 합산
            for column in df.columns[1:]:  # '카드명' 제외
                card_scores[card_name] += calculate_score(row[column], keyword)

    # 점수가 0이 아닌 카드만 필터링
    filtered_cards = {card: score for card, score in card_scores.items() if score > 0}

    # 점수가 가장 높은 카드 정렬
    sorted_cards = sorted(filtered_cards.items(), key=lambda x: x[1], reverse=True)

    return sorted_cards
