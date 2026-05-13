import ollama

def run(question_ko):
    # 한국어 질문을 받아 영어 검색 키워드로 변환
    prompt = f"Generate English search keywords for '{question_ko}'. Output: keywords only, no explanation."
    res = ollama.chat(model="gemma3:latest", messages=[{"role": "user", "content": prompt}])
    return res["message"]["content"]