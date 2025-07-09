from consulting import SentimentAnalyzer
import sys
import argparse
import random

def output_modify(text):
    output = text 
    return output

# 더 자연스럽고 공감적인 표현 패턴
def get_first_response_pattern():
    patterns = [
        "사용자님께서는 현재 {} 감정이 드시는군요.",
        "사용자님께서는 현재 {} 기분이 드시는군요.",
        "사용자님께서는 현재 {} 마음이 드실 것 같아요.",
        "사용자님께서는 지금 {} 상태이시군요."       
    ]
    return random.choice(patterns)

def get_second_single_response_pattern():
    patterns = [
        "그리고 {} 감정까지 느끼셨을 것 같아요.",
        "또한 {} 마음도 드시겠어요.",
        "동시에 {} 기분도 있으시겠어요.",
        "한편으로는 {} 감정도 느끼시는 것 같아요.",
        "더불어 {} 마음도 있으시겠어요."
    ]
    return random.choice(patterns)

def get_combined_response_pattern():
    patterns = [
        "그리고 {}, {} 감정까지 느끼셨을 것 같아요.",
        "또한 {}, {} 마음도 드시겠어요.",
        "동시에 {}, {} 기분도 있으시겠어요.",
        "한편으로는 {} 감정, {} 감정도 느끼시는 것 같아요.",
        "더불어 {}, {} 마음도 있으시겠어요."
    ]
    return random.choice(patterns)

sys.stdout.reconfigure(encoding='utf-8')
parser = argparse.ArgumentParser()
sentiment_analyzer = SentimentAnalyzer()
parser.add_argument('--text', required=True, help='감성 분석을 진행할 텍스트를 입력하세요.')
c = parser.parse_args()

# 소분류 기준으로 필터링된 결과 가져오기
filtered_sentiments = sentiment_analyzer.analyze_filtered(c.text)

# 동적 출력 로직
if len(filtered_sentiments) >= 3:
    # 첫 번째 감정
    first_pattern = get_first_response_pattern()
    first_output = first_pattern.format(output_modify(filtered_sentiments[0]['label']))
    print(first_output)
    
    # 두 번째와 세 번째 감정을 한 문장으로 결합
    combined_pattern = get_combined_response_pattern()
    combined_output = combined_pattern.format(
        output_modify(filtered_sentiments[1]['label']),
        output_modify(filtered_sentiments[2]['label'])
    )
    print(combined_output)
elif len(filtered_sentiments) == 2:
    # 두 감정만 있는 경우
    first_pattern = get_first_response_pattern()
    first_output = first_pattern.format(output_modify(filtered_sentiments[0]['label']))
    print(first_output)
    
    # 두 번째 감정 단독 패턴
    second_pattern = get_second_single_response_pattern()
    second_output = second_pattern.format(output_modify(filtered_sentiments[1]['label']))
    print(second_output)
elif len(filtered_sentiments) == 1:
    # 하나의 감정만 있는 경우
    first_pattern = get_first_response_pattern()
    first_output = first_pattern.format(output_modify(filtered_sentiments[0]['label']))
    print(first_output)
else:
    # 0.5 이상인 감정이 없는 경우
    print("그러셨군요. 사용자님의 이야기를 더 듣고싶어요.")