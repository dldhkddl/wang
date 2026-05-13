# modules/seo.py
import re
from utils.seo_analyzer import analyze_seo_score

def run(script):
    # 1. 원본 분석기 실행 (영문 결과 반환)
    report = analyze_seo_score(script)
    
    # 2. 점수 추출 (정규식으로 [숫자/100] 패턴 찾기)
    #의 점수 형식을 기반으로 숫자만 추출합니다.
    scores = re.findall(r'\[\s*(\d+)\s*/\s*100\s*\]', report)
    
    # 안전하게 점수 할당 (실패 시 기본값 설정)
    overall_score = int(scores[0]) if len(scores) > 0 else 85
    rewatch_rate = int(scores[2]) if len(scores) > 2 else 70
    
    # 3. 한글 번역 매핑
    translation_map = {
        "SEO Score Analysis": "상세 SEO 분석 리포트",
        "Overall Score": "종합 점수",
        "Watch Time Retention": "시청 지속 시간",
        "Rewatch Rate": "재시청률",
        "Search Intent Alignment": "검색 의도 부합도",
        "GEO Semantic Structure": "구조적 완성도",
        "Hook Power": "초반 후킹 강도",
        "User Engagement": "사용자 참여 유도",
        "AI Slop Filter": "AI 부자연스러움 필터"
    }
    
    korean_report = report
    for eng, kor in translation_map.items():
        korean_report = korean_report.replace(eng, kor)
    
    # 리포트, 종합점수, 재시청률을 각각 반환
    return korean_report, overall_score, rewatch_rate