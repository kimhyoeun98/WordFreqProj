import pandas as pd 

# 1. CSV 파일에서 말뭉치(Corpus) 로드
def load_corpus_from_csv(data_filename, column):
    """
    CSV 파일을 읽어 특정 컬럼의 데이터를 리스트 형태로 반환합니다.
    """
    data_df = pd.read_csv(data_filename)
    
    # 해당 컬럼에 데이터가 없는 행(결측치)이 있는지 확인하고 제거합니다.
    if data_df[column].isnull().sum():
        # inplace=True를 통해 원본 데이터프레임에서 직접 결측치를 제거합니다.
        data_df.dropna(subset=[column], inplace=True) 
        
    # 데이터프레임의 특정 컬럼을 파이썬 리스트로 변환하여 반환합니다.
    corpus = list(data_df[column])
    return corpus


# 2. 한국어 토큰화 및 필터링
def tokenize_korean_corpus(corpus, tokenizer, my_tags=None, my_stopwords=None):
    """
    말뭉치를 형태소 분석기를 사용하여 토큰화하고, 원하는 품사(tags)와 불용어(stopwords)를 필터링합니다.
    """
    all_tokens = []
    
    # 원하는 품사(my_tags)와 제외할 단어(my_stopwords) 설정이 모두 있을 경우
    if my_tags and my_stopwords:  
        for text in corpus:
            # 형태소와 품사 태그를 함께 추출하여 조건에 맞는 단어만 리스트에 담습니다.
            tokens = [word for word, tag in tokenizer(text) if tag in my_tags and word not in my_stopwords]
            all_tokens += tokens
    # 그 외의 경우 (품사 제한 없이 불용어만 체크하는 경우 등)
    else:
        for text in corpus:
            tokens = [word for word, tag in tokenizer(text) if word not in my_stopwords]
            all_tokens += tokens
            
    return all_tokens

from collections import Counter

# 3. 단어 빈도 분석
def analyze_word_freq(tokens):
    """
    토큰 리스트를 입력받아 각 단어가 몇 번 등장했는지 세어서 반환합니다.
    """
    return Counter(tokens)

import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 4. Matplotlib 한글 폰트 설정 (한글 깨짐 방지)
def set_korean_font_for_matplotlib(font_path):
    """
    시스템에 설치된 한글 폰트를 Matplotlib에 적용합니다.
    """
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

# 5. 수평 막대 그래프 시각화
def visualize_barhgraph(counter, num_words, title=None, xlabel=None, ylabel=None, font_path = None):
    """
    빈도가 높은 상위 단어들을 수평 막대 그래프로 그립니다.
    """
    # 고빈도 단어를 지정한 개수(num_words)만큼 추출 (현재 코드상으로는 20개 고정되어 있음)
    wordcount_list = counter.most_common(num_words)

    # 그래프에 표시하기 위해 단어(x)와 빈도수(y)를 각각 분리
    x_list = [word for word, count in wordcount_list]
    y_list = [count for word, count in wordcount_list]

    # 한글 폰트 경로가 제공되었다면 폰트 설정 함수 실행
    if font_path: set_korean_font_for_matplotlib(font_path)

    # 수평 막대 그래프 생성 (상위 단어가 위로 오도록 리스트를 역순[::-1]으로 시각화)
    plt.barh(x_list[::-1], y_list[::-1])

    # 그래프의 부가 정보(제목, 축 이름) 설정
    if title : plt.title(title)
    if xlabel : plt.xlabel(xlabel)
    if ylabel : plt.ylabel(ylabel)

    # 그래프 출력
    plt.show()

from wordcloud import WordCloud
  
# 6. 워드클라우드 시각화
def visualize_wordcloud(counter, num_words, font_path):
    """
    단어 빈도 정보를 바탕으로 글자 크기가 다른 워드클라우드를 생성합니다.
    """
    # WordCloud 객체 생성 (배경색, 크기, 최대 단어 수, 폰트 설정)
    wc = WordCloud(
      font_path = font_path,
      width = 800,
      height = 600,
      max_words = num_words,
      background_color = 'ivory'
    )
    
    # 빈도수 딕셔너리(counter)를 입력받아 워드클라우드 이미지 생성
    wc = wc.generate_from_frequencies(counter)

    # Matplotlib을 사용하여 이미지를 화면에 표시
    plt.imshow(wc)
    plt.axis('off') # 그래프의 축(숫자)을 숨김
    plt.show()
