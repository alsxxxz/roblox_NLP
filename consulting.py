import torch
from transformers import pipeline, PreTrainedTokenizerFast, BartForConditionalGeneration, TextClassificationPipeline, BertForSequenceClassification, AutoTokenizer
from sentence_transformers import SentenceTransformer
import kss
#2025.07.08 SentimentAnalyzer(감정 분석) Outout 60개 > 39 로 수정
groups = {
    "분노": [
        "분노","툴툴대는","좌절한","짜증내는","방어적인","악의적인","구역질 나는"
        "안달하는","노여워하는","성가신","억울한"
    ],
    "슬픔": [
        "슬픔","실망한","비통한","후회되는","우울한",
        "마비된","염세적인","눈물이 나는","낙담한","환멸을 느끼는"
    ],
    "불안": [
        "불안","두려운","스트레스 받는","취약한","혼란스러운",
        "당혹스러운","회의적인","걱정스러운","조심스러운","초조한"
    ],

    "상처 받은": ["상처"],

    "괴로운" : ["질투하는","배신당한","고립된","충격 받은","가난한 불우한","희생된","억울한","괴로워하는","당황"
        ,"남의 시선을 의식하는",
        "열등감","혐오스러운",
        "한심한","혼란스러운(당황한)"],

    "외로운": ["고립된(당황한)","외로운","버려진"],

    "부끄러운" : ["부끄러운"],

    "죄책감이 드는" : ["죄책감의"],

    "기쁨": [
        "기쁨","감사하는","신뢰하는","편안한","만족스러운",
        "흥분","느긋","안도","신이 난","자신하는"
    ]}
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
            function_to_apply='softmax'
        )

    def analyze(self, text):
        # 1) 60개 소분류 예측
        raw = self.analyzer(text)[0]  
        #    [{'label':'분노','score':0.42}, ... ]

        # 2) 그룹별 점수 합산
        big_scores = {}
        for r in raw:
            small = r['label']
            score = r['score']
            big   = small2big.get(small, "기타")  
            big_scores[big] = big_scores.get(big, 0.0) + score

        # 3) 상위 3개 대분류 리턴
        top3 = sorted(big_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        return [{"label": grp, "score": sc} for grp, sc in top3]




class SimilarityCalculator:
    def __init__(self):
        self.model = SentenceTransformer('bongsoo/kpf-sbert-v1.1')
    def cal_similarity(self, content):
        sen_list = kss.split_sentences(content)
        top_sentences = []
        top_similarities = []
        for i, sen in enumerate(sen_list):
            sen_embedding = self.model.encode(sen, convert_to_tensor=True)
            similarities = []

            for j, other_sen in enumerate(sen_list):
                if i != j:
                    other_sen_embedding = self.model.encode(other_sen, convert_to_tensor=True)
                    cosine_similarity = torch.nn.functional.cosine_similarity(sen_embedding, other_sen_embedding, dim=0)
                    similarities.append(cosine_similarity.item())
            avg_similarity = sum(similarities) / len(similarities) if similarities else 0
            if len(top_sentences) < 3: ## 문장 개수 사용자 임의로 설정 
                top_sentences.append((sen, avg_similarity))
                top_similarities.append(avg_similarity)
            else:
                min_index = top_similarities.index(min(top_similarities)) 
                if avg_similarity > top_similarities[min_index]:
                    top_sentences[min_index] = (sen, avg_similarity)
                    top_similarities[min_index] = avg_similarity

        top_sentences.sort(key=lambda x: x[1], reverse=True)
        return [sentence for sentence, similarity in top_sentences]
    
class KoBARTSummarizer:
    def __init__(self):
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
        self.model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

    def summarize(self, input_text):
        input_text = input_text.replace('\n', ' ')
        raw_input_ids = self.tokenizer.encode(input_text)
        input_ids = [self.tokenizer.bos_token_id] + raw_input_ids + [self.tokenizer.eos_token_id]
        summary_ids = self.model.generate(torch.tensor([input_ids]), num_beams=6, min_length=0, max_length=52, eos_token_id=1)
        summary = self.tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)
        return summary

class ToxicityChecker:
    def __init__(self):
        model_name = 'smilegate-ai/kor_unsmile'
        model = BertForSequenceClassification.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.pipe = TextClassificationPipeline(
            model=model,
            tokenizer=tokenizer,
            device=-1,  # cpu: -1, gpu: gpu number
            return_all_scores=True,
            function_to_apply='sigmoid'
        )

    def check(self, text):
        results = self.pipe(text)[0]
        max_score = max(result['score'] for result in results)
        if max_score > 0.6:
            return "혐오표현입니다."
        else:
            return "정상 단어입니다."