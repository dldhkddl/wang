import streamlit as st

def apply_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&family=Nunito:wght@400;600;700;800&display=swap');

        .stApp {
            background: linear-gradient(135deg, #facc15 0%, #fbbf24 100%);
            font-family: 'Nunito', sans-serif;
        }

        .playful-container {
            background-color: #fefce8;
            border-radius: 2rem;
            padding: 2.5rem;
            border: 1px solid white;
            box-shadow: 0 8px 0 rgba(0,0,0,0.05), 0 20px 25px -5px rgba(0,0,0,0.1);
            color: #451a03;
            margin-bottom: 2rem;
        }

        h1, h2, h3, .playful-font {
            font-family: 'Fredoka', sans-serif !important;
            font-weight: 900 !important;
        }

        .stButton > button {
            background-color: #3bc771 !important;
            color: white !important;
            border-radius: 2rem !important;
            border: none !important;
            padding: 16px 24px !important;
            box-shadow: 0 5px 0 #2d9a58 !important;
            transition: all 0.1s !important;
            width: 100%;
        }

        .stButton > button p {
            font-family: 'Nunito', sans-serif !important;
            font-weight: 800 !important;
            font-size: 1.2rem !important;
        }

        .stButton > button:active {
            transform: translateY(5px) !important;
            box-shadow: none !important;
        }
        
        .stButton > button:hover {
            background-color: #45d67d !important;
        }

        .result-box {
            background: #fffbeb;
            padding: 1.5rem; 
            border-radius: 1rem; 
            border-left: 5px solid #ef4444;
            margin-top: 1rem;
            white-space: pre-wrap;
            line-height: 1.6;
        }

        .stSelectbox label p, .stRadio label p, .stTextInput label p {
            font-family: 'Fredoka', sans-serif !important;
            font-weight: 800 !important;
            color: #451a03 !important;
        }

        /* 여기에 새로 드린 탭 디자인 코드를 추가하세요! */
        .stTabs [data-baseweb="tab-list"] button {
            font-family: 'Fredoka', sans-serif !important;
            font-weight: 700 !important;
            color: #451a03 !important;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: #2d9a58 !important;
            border-bottom-color: #2d9a58 !important;
        }

        .stTabs [data-baseweb="tab-highlight-checks"] {
            background-color: #2d9a58 !important;
        }
        
        /* [이동됨] Generate 버튼 및 컬럼 정렬 전용 CSS */
        div.stButton > button {
            height: 42px !important;
            min-height: 42px !important;
            line-height: 42px !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            font-size: 0.95rem !important;
            margin-top: 1px !important;
        }
        div[data-testid="column"] { display: flex; align-items: center; }
        </style>
        """,
        unsafe_allow_html=True,
    )