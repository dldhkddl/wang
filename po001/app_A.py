# app_A.py
import streamlit as st
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from tavily import TavilyClient 
import ollama

# 모듈 경로 설정 (A버전용 모듈 임포트)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# [A버전용 모듈 임포트] 
# 실제 파일 생성 시 명칭 뒤에 _A를 붙여 관리하세요.
try:
    from modules.ui import styles, sidebar, components, styles_light, styles_dark 
    import modules.prompts_A as prompts_A
    import modules.search_A as search_A
    import modules.draft_A as draft_A
    import modules.seo as seo
    import modules.prompts_kr_A as prompts_kr_A
    import modules.reset as reset
except ImportError:
    # 경로 예외 발생 시 기본 모듈에서 로드 (테스트용)
    from modules.ui import styles, sidebar, components, styles_light, styles_dark 
    import modules.prompts as prompts_A
    import modules.search as search_A
    import modules.draft as draft_A
    import modules.seo as seo
    import modules.prompts_kr as prompts_kr_A
    import modules.reset as reset

# 환경 변수 설정
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

# 페이지 설정
st.set_page_config(page_title="Last.py Studio - A Version", page_icon="⚡", layout="wide")

# 🎨 UI 스타일 적용
styles.apply_custom_css()

with st.sidebar:
    mode = st.selectbox("🌗 화면 모드 선택", ["Yellow Mode", "Dark Mode"], key="mode_select")
    # A버전 페르소나 렌더링 (귀염 1020, 긍정 5060 반영)
    selected_persona_key = sidebar.render_sidebar()

if mode == "Dark Mode":
    styles_dark.apply_dark_css()
else:
    styles_light.apply_light_css()

# ⚙️ 세션 상태 초기화
if "script" not in st.session_state: st.session_state["script"] = ""
if "titles" not in st.session_state: st.session_state["titles"] = []

# 헤더 렌더링
components.render_main_header()

# ⌨️ 입력 섹션
input_col, btn_col = st.columns([4, 1])
with input_col:
    cat_col, text_col = st.columns([1, 2])
    with cat_col:
        # A버전용 카테고리 구성 로드
        selected_topic = st.selectbox("카테고리", options=list(prompts_A.TOPIC_CONFIG.keys()), label_visibility="collapsed")
    with text_col:
        placeholder_text = prompts_A.TOPIC_CONFIG[selected_topic]["placeholder"]
        question_ko = st.text_input("주제 입력", placeholder=placeholder_text, key="input_topic", label_visibility="collapsed")

with btn_col:
    gen_btn, reset_btn = st.columns(2)
    with gen_btn:
        start_trigger = st.button("✨ Generate", type="primary", use_container_width=True)
    with reset_btn:
        if st.button("🔄 Reset", type="secondary", use_container_width=True):
            reset.reset_session()
            st.rerun()

# 🚀 메인 로직 (A버전: 한글 직행)
if start_trigger:
    reset.reset_session()
    
    if not question_ko.strip():
        st.warning("주제를 입력해주세요!")
    else:
        with st.spinner(f"🔍 '{question_ko}'에 대한 최신 데이터를 분석 중입니다..."):
            tavily_client = TavilyClient(api_key=api_key)
            
            # 1. 최신 데이터 검색 (2026년 BTS 활동, 시고르자브종 특징 등)
            # A버전은 검색어 최적화 단계에서부터 신조어 사전을 참고함
            trend_data = search_A.run(tavily_client, selected_topic, question_ko)
            st.session_state["trends"] = trend_data

            # 2. 한글 제목 즉시 생성 (영문 번역 단계 생략)
            # 페르소나(귀염/긍정)가 즉시 반영된 제목 3개 추출
            titles_ko = draft_A.generate_titles_A(selected_persona_key, trend_data, question_ko)
            st.session_state["titles"] = titles_ko

# 제목 선택 UI
selected_titles = components.render_title_selector(st.session_state.get("titles"))

# 3단계: 스크립트 생성 (한글 100% 보장)
if selected_titles:
    with st.spinner("✍️ 최신 팩트를 기반으로 한글 스크립트 제작 중..."):
        # 검색된 최신 정보와 선택된 제목을 조합하여 스크립트 생성
        # prompts_kr_A의 강력한 한글 100% 규칙 적용
        final_prompt = prompts_kr_A.get_translation_prompt_A(
            selected_persona_key, 
            {"titles": selected_titles, "trends": st.session_state["trends"], "topic": question_ko}
        )
        
        res = ollama.chat(
            model="gemma3:latest", 
            messages=[{"role": "user", "content": final_prompt}],
            options={"temperature": 0.3} # 일관성을 위해 낮은 창의성 설정
        )
        st.session_state["script"] = res["message"]["content"]
        st.rerun()

# --- [하단] 워크스페이스 ---
if st.session_state["script"]:
    st.markdown("---")
    with st.spinner("AI SEO 분석 중..."):
        analysis_report, actual_score, actual_rewatch = seo.run(st.session_state["script"])

    seo_display_data = {"score": actual_score, "volume": "High", "rewatch": actual_rewatch}

    updated_content = components.render_action_buttons(
        st.session_state["script"], 
        seo_data=seo_display_data
    )
    
    if updated_content:
        st.session_state["script"] = updated_content

    with st.expander("🔍 상세 SEO 분석 리포트 확인"):
        st.markdown(analysis_report)

st.markdown('<div style="text-align: center; padding: 2rem; opacity: 0.3;">© 2026 LAST.PY_STUDIO_A</div>', unsafe_allow_html=True)