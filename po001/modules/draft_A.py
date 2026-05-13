# modules/draft_A.py
import ollama
import re
from modules.prompts_A import PERSONA_PROMPTS

def generate_titles_A(persona_key, trend_info, question_ko):
    # .get()을 사용하여 키가 없을 경우 기본값(3040)을 반환하게 하여 에러 방지
    target_persona = PERSONA_PROMPTS.get(persona_key, PERSONA_PROMPTS["3040 (핵심요약/효율)"])
    
    prompt = f"""
    당신은 유튜브 쇼츠 전략가입니다.
    # 페르소나: {target_persona}
    # 최신 정보: {trend_info}
    # 주제: {question_ko}
    
    위 정보를 바탕으로 시청자가 클릭하고 싶게 만드는 [강렬한 한글 제목] 3개를 만드세요.
    
    [출력 규칙]
    1. 제목만 출력하세요. (서론, ##, ** 기호 절대 금지)
    2. 번호(1., 2.)를 붙이지 마세요.
    3. 한 줄에 하나씩 딱 3줄만 작성하세요.
    """
    
    res = ollama.chat(
        model="gemma3:latest", 
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw_content = res["message"]["content"].strip()
    lines = raw_content.split('\n')
    
    clean_titles = []
    for line in lines:
        # 정규식으로 앞부분의 ##, 숫자인 1., 특수문자 등을 제거
        clean_line = re.sub(r'^[\d\.\-\*\•\)\s#]+', '', line).strip()
        clean_line = clean_line.strip('"\'') # 따옴표 제거
        
        # AI의 불필요한 서론 필터링
        if clean_line and not any(ex in clean_line.lower() for ex in ["여기", "제안", "sure", "title"]):
            clean_titles.append(clean_line)
    
    return clean_titles[:3] if clean_titles else [l.strip() for l in lines[:3]]