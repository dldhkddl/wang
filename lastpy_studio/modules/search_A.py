# modules/search_A.py
import ollama
from modules.prompts_A import SEARCH_QUERY_OPTIMIZER, TOPIC_CONFIG

def run(tavily_client, topic, question_ko): # [수정] translation 인자 삭제
    """
    [A버전 - 한글 최적화 검색]
    1. 검색어 최적화: LLM이 한국어 주제를 바탕으로 팩트 체크용 최적 검색어 생성
    2. 데이터 수집: Tavily를 통해 2026년 최신 데이터(BTS, 두쫀쿠 등) 확보
    3. 결과 정리: 핵심 정보만 요약하여 스크립트 재료 생성
    """

    # [STEP 1] 검색어 최적화 (영어 번역 단계 없이 한글 맥락 유지)
    # prompts_A.py에 정의된 SEARCH_QUERY_OPTIMIZER를 사용합니다.
    opt_prompt = SEARCH_QUERY_OPTIMIZER.format(category=topic, user_input=question_ko)
    
    res = ollama.chat(
        model="gemma3:latest", 
        messages=[{"role": "user", "content": opt_prompt}]
    )
    optimized_query = res["message"]["content"].strip()
    
    # [STEP 2] 최적화된 검색어로 Tavily 실행
    search_result = tavily_client.search(query=optimized_query, search_depth="advanced")
    
    # [STEP 3] 결과 청소 및 요약 (시연용 키워드 맞춤형 가이드)
    raw_content = "\n".join([item["content"] for item in search_result.get("results", [])[:5]])
    
    cleaning_prompt = f"""
    아래 검색 데이터에서 "{question_ko}"에 대한 핵심 정의, 특징, 그리고 2026년 최신 사실만 추출하세요.
    
    [시연 키워드 특화 규칙]
    1. '시고르자브종'인 경우: 절대 '음식/요리/맛' 관련 내용을 포함하지 마세요. (생명 존중 강조)
    2. 'BTS'인 경우: 2026년 기준의 최신 공식 활동 정보에만 집중하세요.
    3. '두쫀쿠'인 경우: 신조어의 뜻(두바이 쫀득 쿠키)과 2026년 유행 배경을 정확히 정리하세요.
    
    [검색 데이터]:
    {raw_content}
    """
    
    response = ollama.chat(
        model="gemma3:latest", 
        messages=[{"role": "user", "content": cleaning_prompt}]
    )
    
    return response["message"]["content"]