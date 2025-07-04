# 프로젝트 

한국어 자연어 처리(NLP)에 유용한 모듈과 실행 스크립트를 모아둔 저장소입니다. 주요 기능은 다음과 같습니다:

* 감성 분석: KLUE-BERT 기반 모델로 텍스트 감정 점수 확인
* 문장 유사도 계산: SBERT 기반 벡터 유사도 산출
* KoBART 요약: BART 모델을 사용해 긴 문장 간략화
* 독성 검사: 혐오 표현 여부 판단
* 욕설 마스킹: 지정된 단어 리스트로 부적절한 표현 가리기
* 실행 시간 측정: 각 기능별 처리 속도 확인

---

## 설치 및 실행

1. **Python 3.8+** 버전을 준비합니다.
2. 저장소를 클론하고 프로젝트 디렉터리로 이동합니다:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
3. 가상환경을 생성하고 활성화합니다:

   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate       # Windows
   ```
4. 의존 패키지를 설치합니다:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 주요 파일 구성

```plaintext
consulting.py            - NLP 기능을 모듈화한 클래스 모음
requirements.txt         - 필요한 패키지 목록
run_SentimentAnalyzer.py - 감성 분석 실행 스크립트
run_KobartSummarizer.py  - 텍스트 요약 실행 스크립트
run_ToxicityChecker.py   - 독성(혐오 표현) 검사 스크립트
run_checkbadword.py      - 욕설 마스킹 스크립트
Kobart_checktime.py      - 요약 처리 시간 측정 스크립트
sentiment_Checktime.py   - 감성 분석 처리 시간 측정 스크립트
```

---

## 사용 예시

### 1. 감성 분석

```bash
python run_SentimentAnalyzer.py --text "오늘 기분이 정말 좋네요!"
```

* 상위 3개 감정과 확률을 확인할 수 있습니다.

### 2. 텍스트 요약

```bash
python run_KobartSummarizer.py --text "여기에 긴 텍스트를 입력하세요."
```

* 입력된 텍스트 요약본을 출력합니다.

### 3. 독성 검사

```bash
python run_ToxicityChecker.py --text "이 문장에 혐오 표현이 포함되나요?"
```

* 정상/위험 등의 분류 결과를 제공합니다.

### 4. 욕설 마스킹

1. `badwords_list.xlsx` 파일 경로를 확인 및 수정합니다.
2. 다음 명령을 실행합니다:

   ```bash
   python run_checkbadword.py --text "예시 욕설 문장"
   ```

* 욕설이 `*` 등으로 가려진 문장을 출력합니다.

### 5. 성능 측정

```bash
python Kobart_checktime.py
python sentiment_Checktime.py
```

* 각 스크립트를 30회 실행한 후 평균 처리 시간을 확인합니다.

---

## 주의사항

* `run_checkbadword.py` 내 엑셀 파일 경로를 환경에 맞게 수정해야 합니다.
* 모델 로딩 시 메모리 사용량이 높으므로 GPU 환경을 권장합니다.

---

## 라이선스

MIT 라이선스를 따릅니다.

---

## 작성자

박민주 (Park Minjoo)
