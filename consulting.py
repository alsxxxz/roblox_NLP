
import torch
from transformers import pipeline, PreTrainedTokenizerFast, BartForConditionalGeneration, TextClassificationPipeline, BertForSequenceClassification, AutoTokenizer
from sentence_transformers import SentenceTransformer
import kss

class SentimentAnalyzer:
    def __init__(self):
        model_name = 'hun3359/klue-bert-base-sentiment'
        self.analyzer = pipeline('sentiment-analysis', model=model_name, return_all_scores=True)

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