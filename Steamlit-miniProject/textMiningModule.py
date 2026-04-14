import streamlit as st
import pandas as pd
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter


def load_corpus_from_csv(filename, column):
    """CSV 파일에서 텍스트 데이터 로드"""
    data_df = pd.read_csv(filename)
    corpus = None
    
    if column in data_df.columns:
        if data_df[column].isnull().sum():
            data_df.dropna(subset=[column], inplace=True)
        corpus = list(data_df[column])
    
    return corpus, data_df  # data_df 같이 반환


def tokenize_corpus(corpus):
    """형태소 분석 및 토큰화"""
    okt = Okt()
    
    # 명사(Noun), 형용사(Adjective) 추출
    target_tags = ['Noun', 'Adjective']
    
    # 불용어 설정
    stopwords = [
        '정말', '진짜', '그냥', '너무', '좀', '것', '수', '엄청',
        '나', '내', '들', '더', '이', '그', '저', '잘', '못',
        '도', '는', '을', '를', '이', '가', '에', '의', '너무'
    ]
    
    result_tokens = []

    for text in corpus:
        tokens = [
            word for word, tag in okt.pos(text)
            if tag in target_tags
            and word not in stopwords
            and len(word) > 1  # 한 글자 단어 제거
        ]
        result_tokens.extend(tokens)
    
    return result_tokens


@st.cache_data
def analyze_word_freq(corpus):
    tokens = tokenize_corpus(corpus)
    counter = Counter(tokens)
    return counter


def generate_wordcloud(counter, num_words, font_path):
    """워드클라우드 생성"""
    wc = WordCloud(
        font_path=font_path,
        width=800,
        height=600,
        max_words=num_words,
        background_color='white',
        colormap='viridis'
    )
    wordcloud = wc.generate_from_frequencies(counter)
    return wordcloud
