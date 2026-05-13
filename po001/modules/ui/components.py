import streamlit as st
import re
from utils.seo_tools import render_copy_button

def render_main_header():
    st.markdown("""
        <div class="playful-container">
            <h1 style="font-size: 3rem; margin: 0;">YouTube Shorts Script Generator</h1>
            <p style="font-size: 1.1rem; font-weight: 700; color: #92400e;">AI Script & SEO Analyzer v3.0.0</p>
        </div>
    """, unsafe_allow_html=True)

def render_seo_dashboard(seo_score, search_vol, rewatch_rate):
    """
    [추가] SEO 분석 결과 대시보드 (3D 스타일)
    스크립트 편집기 바로 위에 위치하여 실시간 지표를 시각화합니다.
    """
    import streamlit.components.v1 as components_v1
    
    # 점수에 따른 테마 색상 결정
    score_color = "#4ade80" if seo_score >= 90 else "#fbbf24" if seo_score >= 70 else "#ef4444"
    
    html_code = f"""
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@700&family=Nunito:wght@700;800&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
    
    <style>
        body {{ background-color: transparent; font-family: 'Nunito', sans-serif; margin: 0; padding: 0; }}
        .playful-container {{
            background: #fffbeb; 
            border: 2px solid #fef08a;
            border-radius: 1.5rem;
            padding: 1.2rem 1.8rem;
            box-shadow: 0 8px 12px -3px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
        }}
        .progress-bg {{ background: #fefce8; border-radius: 99px; height: 10px; width: 100%; overflow: hidden; }}
        .progress-bar {{ 
            background: {score_color}; 
            height: 100%; 
            width: 0%; 
            transition: width 1.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}
        .stat-card {{
            background: #fff;
            border: 2px solid #fef08a;
            border-radius: 1.2rem;
            padding: 0.8rem 1.2rem;
        }}
        .font-fredoka {{ font-family: 'Fredoka', sans-serif; }}
    </style>

    <div class="space-y-3" style="margin-bottom: 20px;">
        <div class="playful-container">
            <div class="flex justify-between items-center mb-3">
                <div class="flex items-center gap-3">
                    <span class="material-symbols-outlined text-[#92400e]" style="font-size: 2.5rem;">analytics</span>
                    <h4 class="text-s font-black text-[#92400e] uppercase tracking-wider">SEO Quality Analyzer</h4>
                </div>
                <div class="flex items-baseline gap-1">
                    <span id="seo-num" class="text-4xl font-black text-[{score_color}] font-fredoka">0</span>
                    <span class="text-sm font-black text-gray-300">/ 100</span>
                </div>
            </div>
            <div class="progress-bg"><div id="seo-bar" class="progress-bar"></div></div>
        </div>

        <div class="grid grid-cols-2 gap-3">
            <div class="stat-card flex justify-between items-center">
                <span class="text-[12px] font-black text-[#92400e] uppercase">Search Volume</span>
                <span class="text-xl font-black text-[#FF0000] font-fredoka">{search_vol}</span>
            </div>
            <div class="stat-card flex justify-between items-center border-[#fbbf24]">
                <span class="text-[12px] font-black text-[#92400e] uppercase">Rewatch Rate</span>
                <span id="rewatch-num" class="text-xl font-black text-[#fbbf24] font-fredoka">0%</span>
            </div>
        </div>
    </div>

    <script>
        window.onload = () => {{
            setTimeout(() => {{
                // 게이지 바 애니메이션
                document.getElementById('seo-bar').style.width = '{seo_score}%';
                
                // SEO 점수 카운팅
                let s_curr = 0;
                const s_timer = setInterval(() => {{
                    if(s_curr >= {seo_score}) {{
                        document.getElementById('seo-num').innerText = {seo_score};
                        clearInterval(s_timer);
                    }} else {{
                        document.getElementById('seo-num').innerText = ++s_curr;
                    }}
                }}, 20);
                
                // Rewatch Rate 카운팅
                let r_curr = 0;
                const r_timer = setInterval(() => {{
                    if(r_curr >= {rewatch_rate}) {{
                        document.getElementById('rewatch-num').innerText = {rewatch_rate} + "%";
                        clearInterval(r_timer);
                    }} else {{
                        document.getElementById('rewatch-num').innerText = (++r_curr) + "%";
                    }}
                }}, 20);
            }}, 200);
        }};
    </script>
    """
    return components_v1.html(html_code, height=190)


def render_title_selector(titles):
    """
    [1단계] 제목 추천 섹션
    """
    if not titles:
        return None

    st.markdown("---")
    st.markdown(
        """
        <div style="margin-top: 10px; margin-bottom: 25px; display: flex; align-items: center; gap: 12px;">
            <span class="material-symbols-outlined" 
                  style="color: #ef4444; font-size: 2.2rem; font-weight: 900; line-height: 1; display: inline-block;">
                checklist
            </span>
            <div style="display: flex; flex-direction: column; justify-content: center;">
                <h3 style="font-family: 'Fredoka', sans-serif; font-size: 1.5rem; font-weight: 700; color: #451a03; margin: 0; line-height: 1.1;">
                    CHOOSE TITLE
                </h3>
                <p style="font-family: 'Fredoka', sans-serif; font-size: 0.85rem; font-weight: 600; color: #92400e; margin: 0; line-height: 1;">
                    (최대 3개 선택 가능)
                </p>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    selected = []
    for i, title in enumerate(titles):
        index_label = f"{i+1:02}"
        col_check, col_content = st.columns([0.08, 0.92], gap="small")

        with col_check:
            is_checked = st.checkbox(
                f"cb_{i}", label_visibility="hidden", key=f"title_cb_{i}"
            )

        with col_content:
            is_dark = st.session_state.get("dark_mode", False)
            bg_color = (
                ("#fefce8" if is_checked else "#ffffff")
                if not is_dark
                else ("#2d3748" if is_checked else "#1f2937")
            )

            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 15px; padding: 16px 20px; background-color: {bg_color}; 
                            border: 2px solid #fef08a; border-radius: 1rem; margin-bottom: 12px; margin-left: -15px;">
                    <span style="background-color: #ef4444; color: white; font-weight: 900; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">{index_label}</span>
                    <span style="font-family: 'Fredoka', sans-serif; font-weight: 600; color: {('#451a03' if not is_dark else '#ffffff')}; font-size: 1.1rem;">
                        {title}
                    </span>
                </div>
            """,
                unsafe_allow_html=True,
            )
            if is_checked:
                selected.append(title)

    if selected:
        st.markdown(
            """
            <style>
            div.stButton > button { font-family: 'Fredoka', sans-serif !important; font-weight: 700 !important; }
            </style>
        """,
            unsafe_allow_html=True,
        )
        if st.button(
            "🚀 선택된 제목으로 스크립트 일괄 생성",
            key="btn_batch",
            use_container_width=True,
        ):
            return selected
    return None


def render_action_buttons(script_content, seo_data=None):
    """
    [2단계] 최종 통합 워크스페이스
    - Hashtag Lab & Viral Tips가 상단에 배치되고,
    - 그 아래 SEO Analyzer 대시보드, 
    - 맨 아래에 Editor가 위치합니다.
    """
    if not script_content:
        return

    extracted_tags = re.findall(r"#\w+", script_content)
    display_tags = extracted_tags if extracted_tags else ["#유튜브쇼츠", "#트렌드", "#LastpyStudio"]

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@900&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-25..0');

        div[data-testid="stDownloadButton"] > button {
            background-color: #ef4444 !important;
            color: white !important;
            border-radius: 1.5rem !important;
            padding: 0.6rem 2rem !important;
            font-weight: 900 !important;
            font-family: 'Fredoka', sans-serif !important;
            box-shadow: 0 6px 0 #991b1b, inset 0 -3px 4px rgba(0,0,0,0.1) !important;
            transition: all 0.1s !important;
        }
        div[data-testid="stDownloadButton"] > button:active { transform: translateY(4px) !important; box-shadow: none !important; }

        .hashtag-wrapper { display: flex; flex-wrap: wrap; gap: 8px !important; align-items: center; }
        .hashtag-pill {
            background-color: #fef08a;
            color: #451a03;
            padding: 4px 10px;
            border-radius: 10px;
            font-size: 0.8rem;
            font-weight: 800;
            white-space: nowrap;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid rgba(253, 224, 71, 0.4);
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # 1. 헤더 및 다운로드 버튼
    header_col, download_col = st.columns([0.7, 0.3])
    with header_col:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
                <span class="material-symbols-outlined" style="color: #ef4444; font-size: 2.5rem; font-weight: 900;">verified</span>
                <h3 style="font-size: 1.5rem; font-weight: 900; color: #451a03; margin: 0; font-family: 'Fredoka';">FINAL WORKSPACE</h3>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with download_col:
        st.download_button(
            "📥 전체 저장",
            data=script_content,
            file_name="lastpy_script.txt",
            use_container_width=True,
        )

    # 2. 상단 정보 섹션
    info_col_left, info_col_right = st.columns([0.5, 0.5], gap="medium")
    with info_col_left:
        st.markdown("<p style='font-size: 1rem; font-weight: 900; color: #ef4444; text-transform: uppercase; margin-bottom: 8px; font-family: \"Fredoka\";'>Hashtag Lab</p>", unsafe_allow_html=True)
        st.markdown('<div class="hashtag-wrapper">' + "".join([f'<span class="hashtag-pill">{tag}</span>' for tag in display_tags]) + '</div>', unsafe_allow_html=True)

    with info_col_right:
        st.markdown(
            """
            <div style='background: #fefce8; border: 2px dashed #fde047; border-radius: 1rem; padding: 12px 18px;'>
                <span style='font-size: 1rem; font-weight: 900; color: #92400e; display: block; margin-bottom: 4px;'>VIRAL TIPS</span>
                <p style='font-size: 0.75rem; color: #451a03; font-weight: 600; line-height: 1.4; margin: 0;'>
                    💡 <b>SEO 분석기</b>를 확인하며 <b>EDITOR</b>에서 직접 수정하세요!
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

    # --- [추가] EDITOR 바로 위에 SEO Analyzer 대시보드 배치 ---
    if seo_data:
        render_seo_dashboard(
            seo_score=seo_data.get("score", 0),
            search_vol=seo_data.get("volume", "N/A"),
            rewatch_rate=seo_data.get("rewatch", 0)
        )

    # 3. 하단 Editor
    st.markdown(
        "<p style='font-size: 1.25em; font-weight: 900; color: #92400e; margin-bottom: 8px;'>EDITOR</p>",
        unsafe_allow_html=True,
    )
    edited_script = st.text_area(
        "Editor",
        value=script_content,
        height=500,
        label_visibility="collapsed",
        key="unified_editor",
    )
    render_copy_button(edited_script, "📋 편집 내용 복사")

    return edited_script