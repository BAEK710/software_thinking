import pandas as pd
import openai
import spacy

openai.api_key = "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"

nlp = spacy.load("ko_core_news_sm")


def load_card_data(file_path):
    try:
        df = pd.read_excel("card_data.xlsx")
        return df
    except Exception as e:
        print(f"데이터를 읽는 중 오류가 발생했습니다: {e}")
        return None


def extract_keywords(user_input):
    doc = nlp(user_input)
    keywords = [token.text for token in doc if token.pos_ in ("NOUN", "PROPN")]
    return keywords


def search_card(df, keywords):
    matched_cards = []
    for keyword in keywords:
        for index, row in df.iterrows():
            for column in df.columns[1:]:
                if pd.notna(row[column]) and keyword in str(row[column]):
                    matched_cards.append((row["카드명"], column, row[column]))
                    break
    return matched_cards


def chat_with_gpt(file_path):
    print("안녕하세요! 카드 추천 챗봇입니다. 종료하려면 '종료'라고 입력하세요.\n")

    df = load_card_data(file_path)
    if df is None:
        print("데이터를 로드하지 못했습니다. 프로그램을 종료합니다.")
        return

    while True:
        user_input = input("사용자: ")

        if user_input.lower() in ["종료", "exit", "quit"]:
            print("챗봇: 대화를 종료합니다. 좋은 하루 되세요!")
            break

        keywords = extract_keywords(user_input)
        if not keywords:
            print("챗봇: 관련된 키워드를 찾을 수 없습니다. 더 구체적으로 말씀해주세요.")
            continue

        matched_cards = search_card(df, keywords)

        if matched_cards:
            card_info = "\n".join(
                [f"- {card[0]} ({card[1]}): {card[2]}" for card in matched_cards]
            )
            additional_context = f"다음은 '{', '.join(keywords)}' 관련 혜택을 가진 카드입니다:\n{card_info}"
        else:
            additional_context = f"'{', '.join(keywords)}'와 관련된 카드를 찾지 못했습니다. 다른 질문을 해주세요."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 카드 추천 전문가입니다."},
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": additional_context},
                ],
                temperature=0.7,
            )

            bot_reply = response["choices"][0]["message"]["content"]
            print(f"챗봇: {bot_reply}")

        except Exception as e:
            print(f"오류가 발생했습니다: {e}")
            break


# 프로그램 실행
if __name__ == "__main__":
    file_path = "card_data.xlsx"
    chat_with_gpt(file_path)
