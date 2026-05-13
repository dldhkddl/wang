"""
SEO 도구 모듈 - 다운로드 및 복사 기능
"""
import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
from datetime import datetime


def create_download_content(question_ko, translation, current_date, trends, script):
    """
    다운로드용 텍스트 내용 생성
    
    Args:
        question_ko (str): 사용자가 입력한 주제
        translation (str): 번역된 키워드
        current_date (str): 현재 날짜
        trends (str): 트렌드 정보
        script (str): 생성된 스크립트
    
    Returns:
        str: 다운로드할 파일 내용
    """
    return f"""주제: {question_ko}
검색 키워드: {translation}
날짜: {current_date}

=== Current Trends ===
{trends}

=== 60-Second Video Script ===
{script}
"""


def render_download_button(content, filename_prefix="video_script"):
    """
    다운로드 버튼 렌더링
    
    Args:
        content (str): 다운로드할 내용
        filename_prefix (str): 파일명 접두사
    """
    st.download_button(
        label="📥 텍스트 파일로 다운로드",
        data=content,
        file_name=f"{filename_prefix}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
    )


def render_copy_button(content, button_label="📋 스크립트 COPY"):
    """
    복사 버튼 렌더링
    
    Args:
        content (str): 복사할 내용
        button_label (str): 버튼 라벨
    """
    st_copy_to_clipboard(content, button_label)
