"""
Reset 기능 모듈
스트림릿 세션 상태를 초기화하여 새로운 스크립트 생성을 가능하게 합니다.
"""

import streamlit as st

def reset_session():
    """
    세션 상태를 초기화하여 처음 상태로 되돌립니다.
    """
    # 모든 세션 상태 초기화
    st.session_state["script"] = ""
    st.session_state["titles"] = []
    st.session_state["translation"] = ""
    
    # 추가 세션 상태가 있다면 함께 초기화
    if "title_map" in st.session_state:
        st.session_state["title_map"] = {}
    if "trends" in st.session_state:
        st.session_state["trends"] = ""
    
    return True

def get_reset_button_style():
    """
    Reset 버튼의 커스텀 스타일을 반환합니다.
    """
    return """
    <style>
    div[data-testid="stButton"] button[kind="secondary"] {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border: none;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    </style>
    """
