import pandas as pd
import argparse
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')


file_path = r'C:\Users\retail\Desktop\Sentence\badwords_list.xlsx'
badwords_df = pd.read_excel(file_path, usecols=[0], skiprows=2)
badwords_list = badwords_df.iloc[:, 0].tolist()

parser = argparse.ArgumentParser()
parser.add_argument('--text', required=True,help='문장을 입력하세요')
c = parser.parse_args()

user_input = c.text

detected = []

for badword in badwords_list:
    #badwords가 몇글자이든 전부 공백으로 출력
    if badword in user_input:
        pattern = re.compile(re.escape(badword), re.IGNORECASE)
        replacement = ' ' * len(badword)
        user_input = pattern.sub(replacement, user_input)  ####0521
        
        
        
        # # 3글자 이하면 1글자 블라인드
        # if len(badword) <= 3: 
        #     user_input = user_input.replace(badword,'X'+badword[1:])
        # # 그외에는 2글자 블라인드
        # else:
        #     user_input = user_input.replace(badword,'XX'+badword[2:])



print(user_input)