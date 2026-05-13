import streamlit as st

def apply_dark_css():
    """
    [다크 모드 최종_Fix_v21]
    1. 기존 디자인 100% 유지 (배경 다크 네이비 고정)
    2. 제목 선택 구간(Checklist): 글씨 검정색 고정
    3. VIRAL TIPS(꿀팁 박스): 내부 글씨만 어두운색(#000000)으로 강제 적용
    """
    font_css = """
        @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&display=swap');
        
        /* 텍스트 태그만 폰트 적용 (아이콘 보호) */
        h1, h2, h3, h4, h5, h6, p, a, li, label, input, textarea {
            font-family: 'Fredoka', sans-serif !important;
        }
    """
    st.markdown(f"""
    <style>
        {font_css}
        
        /* [핵심] 모든 버튼 글자 중앙 정렬 */
        .stButton > button {{
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            height: 45px !important;
            padding: 0 1rem !important;
            line-height: 1 !important;
        }}
        .stButton > button div[data-testid="stMarkdownContainer"] p {{
            margin: 0 !important;
            line-height: 1 !important;
        }}

        /* 1. 배경 및 기본 텍스트 설정 (기존 유지) */
        .stApp, header, section[data-testid="stSidebar"] {{ 
            background-color: #111827 !important; 
            background-image: none !important;
            color: #ffffff !important;
        }}

        h1, h2, h3, h4, h5, h6, p, span, div, label {{
            color: #ffffff;
            -webkit-text-fill-color: #ffffff;
        }}

        /* 2. [핵심 수정] VIRAL TIPS (꿀팁 박스) 내부 글씨 블랙 강제 */
        /* 노란 배경색 속성을 가진 박스를 찾아 그 안의 글자만 블랙으로 바꿉니다. */
        div[style*="background: #fefce8"] *,
        div[style*="rgb(254, 252, 232)"] * {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            font-weight: 600 !important;
        }}
        
        div[style*="background: #fefce8"] {{
            background-color: #ffffff !important; /* 배경은 화이트로 통일 */
            border: 2px solid #374151 !important;
            border-radius: 0.8rem !important;
        }}

        /* 3. [기존 유지] 제목 선택 박스 (Checklist) 글씨 블랙 고정 */
        div[style*="border: 2px solid #fef08a"] *,
        div[style*="rgb(254, 240, 138)"] * {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }}
        div[style*="border: 2px solid #fef08a"] {{
            border-color: #ffffff !important;
        }}

        /* 4. 입력창 및 드롭다운 디자인 유지 */
        .stTextInput input, 
        .stTextArea textarea, 
        div[data-baseweb="select"] > div {{
            background-color: #ffffff !important;  
            border: 2px solid #374151 !important;
            border-radius: 0.8rem !important;
        }}

        .stTextInput input, 
        .stTextArea textarea, 
        div[data-baseweb="select"] * {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }}
        
        div[data-baseweb="select"] svg, .stTextInput svg {{
            fill: #000000 !important;
        }}
        
        ul[data-baseweb="menu"] {{ background-color: #ffffff !important; }}
        li[data-baseweb="option"] {{ color: #000000 !important; }}

        /* 5. 블랙 예외 항목 재선언 (우선순위 보호) */
        .hashtag-pill,
        button * {{
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }}
        
        /* 사이드바 및 기타 정리 */
        div[data-testid="stMetricValue"] {{ color: #ffffff !important; }}
        div[data-testid="stMetricLabel"] {{ color: #9ca3af !important; }}
        div[data-testid="stTooltipContent"] {{ display: none !important; }}
        .playful-container {{ background-color: #1f2937 !important; border: 1px solid #374151 !important; }}
        
        button[data-testid="stSidebarCollapseButton"] {{ font-family: sans-serif !important; text-indent: -9999px !important; }}
        button[data-testid="stSidebarCollapseButton"] svg {{ text-indent: 0 !important; fill: #ffffff !important; }}
        div[data-testid="stExpander"] summary {{ font-family: sans-serif !important; }}

    </style>
    """, unsafe_allow_html=True)