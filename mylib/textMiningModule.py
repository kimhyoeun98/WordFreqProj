import streamlit as st
import pandas as pd
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter


def load_corpus_from_csv(filename, column):
    """
    CSV 파일에서 특정 컬럼의 텍스트 데이터를 로드하고 전처리합니다.
    :param filename: 읽어올 CSV 파일 경로
    :param column: 분석할 텍스트가 들어있는 컬럼명
    :return: (말뭉치 리스트, 전체 데이터프레임)
    """
    data_df = pd.read_csv(filename)
    corpus = None
    
    # 해당 컬럼이 데이터프레임에 존재하는지 확인
    if column in data_df.columns:
        # 해당 컬럼에 비어있는 값(NaN)이 있다면 해당 행을 삭제
        if data_df[column].isnull().sum():
            data_df.dropna(subset=[column], inplace=True)
        # 텍스트 데이터를 리스트 형태로 변환하여 저장
        corpus = list(data_df[column])
    
    return corpus, data_df  # 분석을 위한 corpus와 표 출력을 위한 data_df를 함께 반환


def tokenize_corpus(corpus):
    """
    한국어 형태소 분석기(Okt)를 사용하여 텍스트를 토큰화하고 필터링합니다.
    """
    okt = Okt()
    
    # 분석 대상 품사 설정: 명사와 형용사만 추출 (의미 전달이 뚜렷한 품사 위주)
    target_tags = ['Noun', 'Adjective']
    
    # 분석에서 제외할 불용어(Stopwords) 정의
    stopwords = [
        '정말', '진짜', '그냥', '너무', '좀', '것', '수', '엄청',
        '나', '내', '들', '더', '이', '그', '저', '잘', '못',
        '도', '는', '을', '를', '이', '가', '에', '의', '너무'
    ]
    
    result_tokens = []

    for text in corpus:
        # okt.pos()를 통해 형태소 분석 및 품사 태깅 수행
        # 조건: 1) 대상 품사인가? 2) 불용어가 아닌가? 3) 글자 수가 2글자 이상인가?
        tokens = [
            word for word, tag in okt.pos(text)
            if tag in target_tags
            and word not in stopwords
            and len(word) > 1  # '나', '그', '것' 등 의미 없는 한 글자 단어 제외
        ]
        result_tokens.extend(tokens)
    
    return result_tokens


# Streamlit의 캐싱 기능을 활용하여 동일한 연산 반복 시 속도를 향상시킵니다.
# (데이터가 바뀌지 않았다면 이전에 계산한 값을 그대로 사용함)
@st.cache_data
def analyze_word_freq(corpus):
    """토큰화 후 단어별 빈도수를 계산합니다."""
    tokens = tokenize_corpus(corpus)
    counter = Counter(tokens)
    return counter


def generate_wordcloud(counter, num_words, font_path):
    """
    전달받은 빈도수 데이터를 바탕으로 워드클라우드 이미지를 생성합니다.
    """
    wc = WordCloud(
        font_path=font_path,      # 한글 깨짐 방지를 위한 폰트 경로
        width=800,                # 이미지 가로 크기
        height=600,               # 이미지 세로 크기
        max_words=num_words,      # 시각화할 최대 단어 수
        background_color='white', # 배경색 (흰색)
        colormap='viridis'        # 단어 색상 테마
    )
    
    # 단어 빈도 딕셔너리를 사용하여 워드클라우드 생성
    wordcloud = wc.generate_from_frequencies(counter)
    return wordcloud
