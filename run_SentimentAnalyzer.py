from consulting import SentimentAnalyzer
import argparse
import sys

def output_modify(text):
    if text == '분노':
        output = '분노하는'
    elif text == '슬픔':
        output = '슬퍼하는'
    elif text == '불안':
        output = '불안한'
    elif text == '당황':
        output = '당황한'
    elif text == '상처':
        output = '상처받은'
    # elif text == '열등감':
    #     output = '열등한'
    elif text == '기쁨':
        output = '기뻐하는'
    elif text == '흥분':
        output = '흥분한'
    elif text == '느긋':
        output = '느긋한'
    elif text == '안도':
        output = '안도하는'
    else:
        output = text

    return output

sys.stdout.reconfigure(encoding='utf-8')

parser = argparse.ArgumentParser()
sentiment_analyzer = SentimentAnalyzer()
parser.add_argument('--text', required=True,help='감성 분석을 진행할 텍스트를 입력하세요.')
c = parser.parse_args()
top_3_sentiments = sentiment_analyzer.analyze(c.text)
# print("상위 3개의 감정 결과:")
for idx in range(len(top_3_sentiments)):
    if idx == 0:
        output = f"당신이 가장 많이 느낀 것은 '{output_modify(top_3_sentiments[idx]['label'])}' 감정이시군요."
    elif idx == 1:
        output = f"그 다음으로 많이 느낀 것은 '{output_modify(top_3_sentiments[idx]['label'])}' 감정이시네요."
    elif idx == 2:
        output = f"또한, '{output_modify(top_3_sentiments[idx]['label'])}' 감정도 느끼셨네요."

    print(output)

    # print(f"감정: {top_3_sentiments[idx]['label']}, 점수: {top_3_sentiments[idx]['score']:.4f}")