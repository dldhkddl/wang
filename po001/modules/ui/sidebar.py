import streamlit as st
import os

# app.py 설정에 따라 경로 예외 처리
try:
    from modules import prompts
except ImportError:
    import prompts


def render_sidebar():
    """
    사이드바의 로고와 제목 크기를 키우고 완벽하게 중앙에 배치합니다.
    """
    with st.sidebar:
        # 1. 사이드바 여백 제거 및 텍스트/로고 크기 확대를 위한 CSS
        st.markdown(
            """
            <style>
                /* 사이드바 내부 기본 패딩 제거 */
                [data-testid="stSidebarUserContent"] {
                    padding-top: 2rem !important;
                    padding-left: 0px !important;
                    padding-right: 0px !important;
                }
                
                /* 타이틀 텍스트: 크기를 1.8rem으로 확대 및 폰트 굵기 강조 */
                .sidebar-main-title {
                    color: #451a03;
                    font-family: 'Fredoka', sans-serif;
                    font-size: 1.8rem !important; /* 텍스트 크기 확대 */
                    font-weight: 900 !important;
                    text-align: center !important;
                    width: 100% !important;
                    margin-top: 0.8rem !important;
                    letter-spacing: -0.02em;
                }

                /* 페르소나 설정 라벨 폰트 크기 조정 */
                .stRadio label {
                    font-size: 1.1rem !important;
                    font-weight: 700 !important;
                    color: #451a03;
                }
            </style>
        """,
            unsafe_allow_html=True,
        )

        # 2. 로고 영역: 크기를 80px로 확대하고 중앙 배치
        logo_path = "logo.png"

        # 로고가 들어갈 컬럼 비율 조정 (0.4 : 1.2 : 0.4)
        col1, col2, col3 = st.columns([0.4, 1.2, 0.4])

        with col2:
            if os.path.exists(logo_path):
                # 로고 크기를 80px 정도로 큼직하게 설정
                st.image(logo_path, use_container_width=True)
            else:
                # 로고 없을 때 대체 아이콘도 크게 확대
                st.markdown(
                    """
                    <div style="background: #ef4444; width: 80px; height: 80px; border-radius: 1.8rem; 
                                display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                        <span style="color: white; font-size: 2.5rem;">⚡</span>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

        # 3. 타이틀 영역: 확대된 텍스트 출력
        st.markdown(
            '<p class="sidebar-main-title">last.py_studio</p>', unsafe_allow_html=True
        )

        st.write("---")

        # 4. 페르소나 설정 (라디오 버튼)
        persona_list = list(prompts.PERSONA_PROMPTS.keys())
        selected_persona = st.radio(
            "페르소나 설정", options=persona_list, index=1  # 기본값: 3040
        )
        
            

        st.markdown("---")
        st.caption("v3.0.0 Powered by Gemini & Tavily")

    return selected_persona
