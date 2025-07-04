from consulting import ToxicityChecker
import argparse
import sys
sys.stdout.reconfigure(encoding='utf-8')

parser = argparse.ArgumentParser()
toxicity_checker = ToxicityChecker()
parser.add_argument('--text', required=True, help='혐오표현을 감지할 텍스트를 입력해주세요.')
c = parser.parse_args()

toxicity_result = toxicity_checker.check(c.text)
print(f"Toxicity Check: {toxicity_result}")