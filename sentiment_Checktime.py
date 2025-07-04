import time
from consulting import SentimentAnalyzer

# 임의의 텍스트 입력 리스트 (총 30개)
texts = [
     "이 제품은 정말 훌륭해요!",
    "정말 최악의 서비스였습니다.",
    "보통이에요. 다시 이용할지 잘 모르겠네요.",
    "너무 행복해요! 기대 이상이에요.",
    "기분이 좋지 않아요. 별로였어요.",
    "이 영화는 내 인생 최고의 영화였습니다!",
    "식사 맛이 형편없었어요. 다시는 가고 싶지 않네요.",
    "평범한 경험이었어요. 특별한 건 없었어요.",
    "친절한 직원 덕분에 좋은 시간을 보냈어요.",
    "기대 이하였어요. 실망스러웠습니다.",
    "정말 즐거운 시간이었어요. 다시 오고 싶어요.",
    "서비스가 개선이 필요해 보여요.",
    "이보다 더 나쁠 수는 없을 거예요."
]

sentiment_analyzer = SentimentAnalyzer()
execution_times = []

for i in range(30):
    text = texts[i % len(texts)]
    start_time = time.time()
    top_3_sentiments = sentiment_analyzer.analyze(text)
    end_time = time.time()
    execution_time = end_time - start_time
    execution_times.append(execution_time)
    print(f"실행 시간: {execution_time:.4f} 초\n")

average_time = sum(execution_times) / len(execution_times)
print(f"\n평균 실행 시간: {average_time:.4f} 초")
