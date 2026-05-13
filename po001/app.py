import streamlit as st
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from tavily import TavilyClient 
import ollama

# 현재 디렉토리를 경로에 추가하여 modules를 찾을 수 있게 함
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules.draft import AI_OPTIONS

# UI 모듈 및 핵심 로직 임포트
try:
    # [수정] styles_light, styles_dark, reset 추가
    from modules.ui import styles, sidebar, components, styles_light, styles_dark 
    from modules import prompts, trans, search, draft, seo, prompts_kr, reset
    from utils import seo_tools
except ImportError:
    from modules.ui import styles, sidebar, components, styles_light, styles_dark 
    import modules.prompts as prompts
    import modules.trans as trans
    import modules.search as search
    import modules.draft as draft
    import modules.seo as seo
    import modules.prompts_kr as prompts_kr
    import modules.reset as reset
    from utils import seo_tools


# 환경 변수 및 API 키 설정
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

# 페이지 설정
st.set_page_config(page_title="Last.py Studio", page_icon="⚡", layout="wide")

# ==============================================================================
# 🎨 UI 스타일 및 모드 설정 (기존 styles.apply_custom_css 위치)
# ==============================================================================

# 1. 기본 스타일 적용
styles.apply_custom_css()

# 2. 다크모드 스위치 (사이드바)
with st.sidebar:
    mode = st.selectbox("🌗 화면 모드 선택", ["Yellow Mode", "Dark Mode"], key="mode_select")

# 3. 모드별 스타일 덮어쓰기
if mode == "Dark Mode":
    styles_dark.apply_dark_css()
else:
    styles_light.apply_light_css()

# 4. 사이드바 렌더링 (페르소나 선택 등 기존 기능 유지)
selected_persona_key = sidebar.render_sidebar()


# ==============================================================================
# ⚙️ 세션 상태 초기화 & 헤더
# ==============================================================================
if "script" not in st.session_state: st.session_state["script"] = ""
if "titles" not in st.session_state: st.session_state["titles"] = []
if "translation" not in st.session_state: st.session_state["translation"] = ""

# --- [상단] 메인 타이틀 ---
components.render_main_header()


# ==============================================================================
# ⌨️ 입력칸 & 버튼 섹션 (기존 레이아웃 유지 + 리셋 버튼 기능 연결)
# ==============================================================================
input_col, btn_col = st.columns([4, 1])
with input_col:
    cat_col, text_col = st.columns([1, 2])
    with cat_col:
        selected_topic = st.selectbox("카테고리", options=list(prompts.TOPIC_CONFIG.keys()), label_visibility="collapsed")
    with text_col:
        placeholder_text = prompts.TOPIC_CONFIG[selected_topic]["placeholder"]
        question_ko = st.text_input("주제 입력", placeholder=placeholder_text, key="input_topic", label_visibility="collapsed")

with btn_col:
    # 버튼 레이아웃 유지 (Generate / Reset)
    gen_btn, reset_btn = st.columns(2)
    with gen_btn:
        start_trigger = st.button("✨ Generate", type="primary", use_container_width=True)
    with reset_btn:
        reset_trigger = st.button("🔄 Reset", type="secondary", use_container_width=True)

# [Reset 기능] 버튼 클릭 시 모듈 호출하여 초기화 후 리런
if reset_trigger:
    reset.reset_session()
    st.rerun()


# ==============================================================================
# 🚀 메인 로직 (기존 코드 100% 동일)
# ==============================================================================
if start_trigger:
    # [수정] 기존의 긴 초기화 코드 -> reset 모듈 함수로 대체
    reset.reset_session()
    
    if not question_ko.strip():
        st.warning("주제를 입력해주세요!")
    else:
        with st.spinner(":mag: 분석 및 제목 생성 중..."):
            tavily_client = TavilyClient(api_key=api_key)
            translation = trans.run(question_ko)
            st.session_state["translation"] = translation 
            
            trend_data = search.run(tavily_client, selected_topic, question_ko, translation)
            titles_en = draft.generate_titles(selected_persona_key, trend_data, question_ko)
            titles_ko = draft.translate_hooks_to_korean(titles_en, question_ko)

            st.session_state["titles"] = titles_ko
            st.session_state["title_map"] = dict(zip(titles_ko, titles_en))
            st.session_state["trends"] = trend_data

# 제목 선택 UI
selected_titles = components.render_title_selector(st.session_state.get("titles"))

# 2단계: 스크립트 생성 (기존 코드 유지)
if selected_titles:
    titles_en_selected = [st.session_state["title_map"][t] for t in selected_titles]
    with st.spinner("✍️ 1단계: 초안 작성 중..."):
        draft_script_en = draft.generate_script(selected_persona_key, titles_en_selected, st.session_state["trends"])

    with st.spinner("🇰🇷 2단계: 한국어 패치 중..."):
        korean_prompt = prompts_kr.get_translation_prompt(selected_persona_key, draft_script_en)
        res = ollama.chat(
            model="gemma3:latest", 
            messages=[{"role": "user", "content": korean_prompt}],
            options=AI_OPTIONS,
            keep_alive=0
        )
        st.session_state["script"] = res["message"]["content"]
        st.rerun()

# --- [하단] 통합 워크스페이스 (기존 코드 유지) ---
if st.session_state["script"]:
    st.markdown("---")
    
    # AI 분석 실행
    with st.spinner("AI가 SEO 지표를 정밀 분석 중입니다..."):
        analysis_report, actual_score, actual_rewatch = seo.run(st.session_state["script"])

    # 점수 데이터 패키징
    seo_display_data = {
        "score": actual_score,    
        "volume": "High",         
        "rewatch": actual_rewatch 
    }

    # 워크스페이스 렌더링
    updated_content = components.render_action_buttons(
        st.session_state["script"], 
        seo_data=seo_display_data
    )
    
    if updated_content:
        st.session_state["script"] = updated_content

    # 상세 리포트
    with st.expander("🔍 상세 SEO 분석 리포트 전문 확인"):
        st.markdown(analysis_report)
    
    st.markdown("---")

# 푸터
st.markdown('<div style="text-align: center; padding: 2rem; opacity: 0.3;">© 2026 LAST.PY_STUDIO</div>', unsafe_allow_html=True)