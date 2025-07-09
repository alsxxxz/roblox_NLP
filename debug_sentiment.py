from consulting import SentimentAnalyzer
import sys
import argparse

sys.stdout.reconfigure(encoding='utf-8')

parser = argparse.ArgumentParser()
parser.add_argument('--text', required=True, help='감성 분석을 진행할 텍스트를 입력하세요.')
args = parser.parse_args()

sentiment_analyzer = SentimentAnalyzer()

# 디버깅 정보 출력
print(f"입력 텍스트: {args.text}")
print()

# 소분류 상위 3개 및 0.5 이상인 것들 확인
top3_small = sentiment_analyzer.debug_analyze(args.text)

print()
print("=== 기존 방식 결과 (대분류 합산 후 상위 3개) ===")
original_result = sentiment_analyzer.analyze(args.text)
for i, result in enumerate(original_result, 1):
    print(f"{i}. 대분류: {result['label']} | 점수: {result['score']:.4f}")

print()
print("=== 새로운 방식 결과 (소분류 0.5 이상 → 대분류 변환) ===")
filtered_result = sentiment_analyzer.analyze_filtered(args.text)
if filtered_result:
    for i, result in enumerate(filtered_result, 1):
        print(f"{i}. 대분류: {result['label']} | 점수: {result['score']:.4f}")
else:
    print("0.5 이상인 감정이 없습니다.")

# 사용법 예시:
# python debug_sentiment.py --text "취준때문에 막막해"