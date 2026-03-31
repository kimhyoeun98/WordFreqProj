from mylib import myTextAnalyzer as ta

# 데이터 로딩
data_filename = ".\data\daum_movie_review.csv"
column ="review"

corpus = ta.load_corpus_from_csv(data_filename, column)
print(corpus[:5])

# 토큰화 -> 빈도수 추출

from konlpy.tag import Okt

tokenizer = Okt().pos
my_tags = ['Noun', 'Verb', 'Adjective']
my_stopwords = ['돈', '나', '할', '헐', '사람', '진짜', '보고', '마지막', '시간', '그냥', '정도','영화','생각','마동석','윤계상','내용','연기','감동','정말','광주','마블','감독']

tokens = ta.tokenize_korean_corpus(corpus[:10], tokenizer, my_tags, my_stopwords)
print(tokens[:10])

counter = ta.analyze_word_freq(tokens)
print(list(counter.items())[:10])

# 시각화

# 수평 막대 그래프
num_words = 20
title = "영화 리뷰"
xlabel = "키워드"
ylabel =  "빈도수"
font_path = "c:/Windows/fonts/malgun.ttf"
ta.visualize_barhgraph(counter, num_words, title, xlabel, ylabel, font_path)

# 워드클라우드
ta.visualize_wordcloud(counter, num_words, font_path)
