import torch
from transformers import pipeline, PreTrainedTokenizerFast, BartForConditionalGeneration, TextClassificationPipeline, BertForSequenceClassification, AutoTokenizer
from sentence_transformers import SentenceTransformer
import kss
#2025.07.08 SentimentAnalyzer(감정 분석) Outout 60개 > 39 로 수정
labels = [
    "분노",
    "좌절한",
    "짜증내는",
    "방어적인",
     "슬픔",
     "실망한",
     "후회되는",
     "우울한",
     "눈물이 나는",
     "불안",
     "두려운",
     "스트레스 받는",
     "혼란스러운",
     "당혹스러운",
     "걱정스러운",
     "조심스러운",
     "상처",
     "질투하는",
     "충격 받은",
     "억울한",
     "괴로워하는",
     "버려진",
     "당황",
     "남의 시선을 의식하는",
     "외로운",
     "죄책감의",
     "부끄러운",
     "한심한",
     "혼란스러운(당황한)",
     "기쁨",
     "감사하는",
     "신뢰하는",
     "편안한",
     "만족스러운",
     "흥분",
     "느긋",
     "안도",
     "신이 난",
     "자신하는"
]
label2id = {l: i for i, l in enumerate(labels)}
id2label = {i: l for l, i in label2id.items()}
num_labels = len(labels)


class SentimentAnalyzer:
    def __init__(self):
        model_name = 'hun3359/klue-bert-base-sentiment'

        #1. 토크나이저 로드
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        #2.num_labels, id2label, label2id 덮어쓰기
        model = BertForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels,
            id2label=id2label,
            label2id=label2id
        )

        #3. 파이프라인 생성
        self.analyzer = TextClassificationPipeline(
            model=model,
            tokenizer=tokenizer,
            return_all_scores=True,
            function_to_apply='softmax'
        )

    def analyze(self, text):
        results = self.analyzer(text)[0]
        top_3_results = sorted(results, key=lambda x: x['score'], reverse=True)[:3]
        return top_3_results




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