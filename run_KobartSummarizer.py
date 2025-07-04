import argparse
from consulting import KoBARTSummarizer,SimilarityCalculator

import sys
sys.stdout.reconfigure(encoding='utf-8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', required=True, help='요약 분석을 진행할 텍스트를 입력하세요.')
    args = parser.parse_args()

    # Summarize the text
    summarizer = KoBARTSummarizer()
    summary = summarizer.summarize(args.text)
    # print("Summary:")
    print(summary)
    # Calculate similarity 같은 내용이 반복될 경우 해당 모듈 적용 
    # similarity_calculator = SimilarityCalculator()
    # top_sentences = similarity_calculator.cal_similarity(summary)

    # print("\nTop 3 Similar Sentences:")
    # for sentence in top_sentences:
    #     print(sentence)
