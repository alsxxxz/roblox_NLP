# run_SentimentAnalyzer.py

from consulting import SentimentAnalyzer
import sys

def output_modify(text: str) -> str:
    """
    파이프라인이 뱉은 원본 레이블(text)을
    사용자 친화적 표현으로 변경해서 반환.
    """
    if text == '분노':
        return '분노하는'
    elif text == '슬픔':
        return '슬퍼하는'
    elif text == '불안':
        return '불안한'
    elif text == '당황':
        return '당황스러운'
    elif text == '상처':
        return '상처받은'
    # elif text == '열등감':
    #     return '열등한'
    elif text == '기쁨':
        return '기뻐하는'
    elif text == '흥분':
        return '흥분한'
    elif text == '느긋':
        return '느긋한'
    elif text == '안도':
        return '안도하는'
    else:
        return text


def analyze_text(text: str):
    """
    텍스트 한 줄을 받아 SentimentAnalyzer 로 감정 점수 리스트를 리턴.
    """
    sa = SentimentAnalyzer()
    return sa.analyze(text)


def format_results(results: list[dict]) -> list[str]:
    """
    analyze_text() 결과를 받아 사람이 읽기 좋은 문장 리스트로 포맷팅.
    """
    lines = []
    for idx, item in enumerate(results):
        orig  = item['label']
        mod   = output_modify(orig)
        score = item['score']

        if idx == 0:
            tmpl = "당신이 가장 많이 느낀 것은 원본='{orig}', 수정='{mod}' (점수: {score:.4f}) 감정이시군요."
        elif idx == 1:
            tmpl = "그 다음으로 많이 느낀 것은 원본='{orig}', 수정='{mod}' (점수: {score:.4f}) 감정이시네요."
        elif idx == 2:
            tmpl = "또한, 원본='{orig}', 수정='{mod}' (점수: {score:.4f}) 감정도 느끼셨네요."
        else:
            # 상위 3개만 출력
            break

        lines.append(tmpl.format(orig=orig, mod=mod, score=score))
    return lines


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="감정 분석을 진행할 텍스트를 입력하세요."
    )
    parser.add_argument('--text', required=True, help='분석할 텍스트')
    args = parser.parse_args()

    results = analyze_text(args.text)
    for line in format_results(results):
        print(line)


if __name__ == "__main__":
    # 윈도우 cmd/python 한글 깨짐 방지
    sys.stdout.reconfigure(encoding='utf-8')
    main()
