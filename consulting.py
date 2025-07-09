import torch
from transformers import pipeline, PreTrainedTokenizerFast, BartForConditionalGeneration, TextClassificationPipeline, BertForSequenceClassification, AutoTokenizer
from sentence_transformers import SentenceTransformer
import kss
#2025.07.08 SentimentAnalyzer(감정 분석) Outout 60 to 30 
groups = {
    "분노하는": ["분노","악의적인","노여워하는"],

    "화나는": ["툴툴대는","짜증내는","구역질 나는", "환멸을 느끼는"],

    "다소 성가신" : ["성가신"],

    "방어적인" : ["방어적인"],

    "억울한": ["억울한"],

    "낙담스러운": ["좌절한","낙담한"],

    "슬픈": ["슬픔","비통한","마비된","염세적인","눈물이 나는"],

    "실망스러운":["실망한"],

    "후회되는" :["후회되는"],
    
    "우울한":["우울한"],

    "불안한": ["불안","취약한","회의적인"],

    "두려운" : ["두려운"], 

    "다소 조심스러운" : ["조심스러운"],

    "스트레스 받는" : ["스트레스 받는"],

    "초조한" : ["초조한", "안달하는"],
    
    "걱정스러운" : ["걱정스러운"],

    "상처받은": ["상처"],

    "억울한": ["억울한"],

    "마음이 불편하거나 괴로운" : ["질투하는","배신당한","고립된","충격 받은","가난한 불우한",
                    "희생된","괴로워하는","남의 시선을 의식하는","열등감","혐오스러운","한심한"],

    "당황스러운" : ["혼란스러운(당황한)","당혹스러운","혼란스러운"],

    "외로운": ["고립된(당황한)","외로운","버려진"],

    "부끄러운" : ["부끄러운"],

    "죄책감이 드는" : ["죄책감의"],

    "기쁜": ["기쁨","신뢰하는"],

    "신나는": ["신이 난", "흥분"],
    
    "자신있는": ["자신하는"],

    "여유로운": ["느긋"],

    "감사하는" : ["감사하는"],

    "편안한": ["편안한"],

    "만족스러운":["만족스러운"],

    "안도하는": ["안도"]

    }
# ── 2) 소분류→대분류 역매핑 생성
small2big = {}
for big, small_list in groups.items():
    for small in small_list:
        small2big[small] = big


class SentimentAnalyzer:
    def __init__(self):
        model_name = 'hun3359/klue-bert-base-sentiment'
        device = 0 if torch.cuda.is_available() else -1
        #1. 토크나이저 로드
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = BertForSequenceClassification.from_pretrained(model_name)

        #3. 파이프라인 생성
        self.analyzer = TextClassificationPipeline(
            model=model,
            tokenizer=tokenizer,
            return_all_scores=True,
            device = device,
            function_to_apply='softmax'
        )

    def analyze(self, text):
        #1. 60개 소분류 예측
        raw = self.analyzer(text)[0]  
        #    [{'label':'분노','score':0.42}, ... ]

        #2. 그룹별 점수 합산
        big_scores = {}
        for r in raw:
            small = r['label']
            score = r['score']
            big   = small2big.get(small, "기타")  
            big_scores[big] = big_scores.get(big, 0.0) + score

        #3. 상위 3개 반환 (필터링 없이)
        top3 = sorted(big_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        return [{"label": grp, "score": sc} for grp, sc in top3]

    def analyze_filtered(self, text):
        """소분류 기준으로 0.5 이상인 것만 필터링하고 대분류로 변환"""
        #1. 60개 소분류 예측
        raw = self.analyzer(text)[0]  
        #    [{'label':'분노','score':0.42}, ... ]

        #2. 0.5 이상인 소분류만 필터링
        filtered_raw = [r for r in raw if r['score'] >= 0.09]
        
        if not filtered_raw:
            return []
        
        #3. 필터링된 소분류를 대분류로 변환
        big_scores = {}
        for r in filtered_raw:
            small = r['label']
            score = r['score']
            big = small2big.get(small, "기타")  
            # 같은 대분류에 여러 소분류가 있을 경우 최대값 사용 (또는 합산)
            if big in big_scores:
                big_scores[big] = max(big_scores[big], score)  # 최대값 사용
                # big_scores[big] += score  # 합산을 원한다면 이 줄 사용
            else:
                big_scores[big] = score
        
        #4. 점수 기준으로 정렬하여 반환 (최대 3개)
        sorted_results = sorted(big_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        return [{"label": grp, "score": sc} for grp, sc in sorted_results]

    def debug_analyze(self, text):
        """디버깅용: 소분류 감정 점수 상위 3개 확인"""
        #1. 60개 소분류 예측
        raw = self.analyzer(text)[0]  
        #    [{'label':'분노','score':0.42}, ... ]

        #2. 점수 기준으로 정렬하여 상위 3개 반환
        top3_small = sorted(raw, key=lambda x: x['score'], reverse=True)[:3]
        
        print("=== 소분류 감정 점수 상위 3개 (디버깅) ===")
        for i, result in enumerate(top3_small, 1):
            small_label = result['label']
            score = result['score']
            big_label = small2big.get(small_label, "기타")
            print(f"{i}. 소분류: {small_label} → 대분류: {big_label} | 점수: {score:.4f}")
        
        print("\n=== 0.06 이상인 소분류 감정들 ===")
        filtered_raw = [r for r in raw if r['score'] >= 0.09]
        if filtered_raw:
            for result in filtered_raw:
                small_label = result['label']
                score = result['score']
                big_label = small2big.get(small_label, "기타")
                print(f"소분류: {small_label} → 대분류: {big_label} | 점수: {score:.4f}")
        else:
            print("0.09 이상인 소분류 감정이 없습니다.")
        
        return top3_small