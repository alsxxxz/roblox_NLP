import time
from consulting import KoBARTSummarizer

# 임의의 텍스트 입력 리스트 (총 30개)
texts = [
"지난 주말에는 친구들과 함께 해변으로 여행을 다녀왔어요. 날씨가 맑아서 바다에서 수영을 즐겼고, 저녁에는 맛있는 해산물을 먹으며 시간을 보냈어요. 해변가에서의 여유로운 시간이 너무 좋았습니다.",
    "최근에 새로운 취미를 시작했어요. 바로 요리입니다. 요리를 시작하게 된 계기는 가정에서 좋은 음식을 먹이고 싶어서예요. 매주 특정 요일에는 새로운 레시피를 시도해 보고 있어요. 이전에는 요리에 대해 거의 모른 상태였지만, 요리하는 과정에서 재미를 느끼고 있어요.",
    "오늘은 친구들과 함께 공원에서 피크닉을 즐겼어요. 준비한 음식들을 나누어 가며 맛있는 점심을 즐기고, 그 후에는 서로 다양한 주제로 대화를 나누었습니다. 즐거운 시간이었어요.",
    "최근에 읽은 책에서 깊은 인상을 받은 구절이 있어요. '삶의 질을 높이는 데에는 항상 새로운 것을 배우는 것이 중요하다'는 문구예요. 이 문구를 통해 일상에서 새로운 도전을 받아들이고, 지식을 쌓는 것이 왜 중요한지 깨닫게 되었어요.",
    "가족들과 함께 계획한 여름 휴가가 아주 즐거웠어요. 목적지에서는 다양한 활동을 즐기며 시간을 보내고, 저녁에는 함께 맛있는 음식을 먹으며 이야기를 나누었어요. 여행을 통해 가족들과 더 가까워질 수 있는 소중한 시간이었습니다.",
    "최근에 관심을 가지게 된 분야가 있어요. 바로 사회복지입니다. 사람들의 삶을 더 나아지게 할 수 있는 방법 중 하나로 사회복지가 중요하다는 생각이 들어서요. 앞으로 사회복지 관련 분야에서 공부를 하고 싶다는 계획을 세우고 있어요."
    ]

summarizer = KoBARTSummarizer()
execution_times = []

for i in range(30):
    # 임의의 텍스트 선택
    text = texts[i % len(texts)]
    
    start_time = time.time()
    summary = summarizer.summarize(text)
    end_time = time.time()

    execution_time = end_time - start_time
    execution_times.append(execution_time)

    print(f"실행 {i+1}: 요약 결과:\n{summary}")
    print(f"실행 시간: {execution_time:.4f} 초\n")

average_time = sum(execution_times) / len(execution_times)
print(f"\n평균 실행 시간: {average_time:.4f} 초")
