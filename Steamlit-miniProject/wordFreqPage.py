import streamlit as st
import pandas as pd
import textMiningModule as tmm
import visualizerModule as vsm

st.set_page_config(
    page_title="단어 빈도수 시각화",
    page_icon="👀"
)

# 한글 폰트
vsm.register_korean_font()

# sidebar
with st.sidebar:
    data_file = st.file_uploader("파일 선택", type=['csv'])
    column_name = st.text_input("데이터가 있는 컬럼명", value="review")

    if st.button("데이터 미리보기"):
        if data_file:
            data_df = pd.read_csv(data_file)
            vsm.show_data_dialog(data_df)
        else:
            st.warning("파일을 먼저 업로드해주세요.")
    
    st.write("설정")
    with st.form("form"):
        freq = st.checkbox("빈도수 그래프", value=True)
        num_freq_words = st.slider("단어 수", 10, 50, 20, 1, key="freq_slider")

        wc = st.checkbox('워드클라우드')
        num_wc_words = st.slider('단어 수', 20, 500, 50, 10, key="wc_slider")

        submitted = st.form_submit_button("분석 시작")

# 메인 화면

st.title("단어 빈도수 시각화")
status = st.info('분석할 파일을 업로드하고, 시각화 수단을 선택한 후 "분석 시작" 버튼을 클릭하세요.')

if submitted:
    if not data_file:
        st.error("분석할 데이터 파일을 업로드 한 후 분석 시작을 눌러주세요.")
        st.stop()
    
    if not freq and not wc:
        st.warning("빈도수 그래프 또는 워드클라우드 중 하나 이상 선택해주세요.")
        st.stop()

    status.info("데이터 분석 중 ...")

    corpus, data_df = tmm.load_corpus_from_csv(data_file, column_name)
    
    if not corpus:
        st.error(f"컬럼명 '{column_name}'을 찾을 수 없습니다. 다시 확인 해주세요.")
        st.stop()

    # 빈도수 분석
    counter = tmm.analyze_word_freq(corpus)

    status.success(f"분석 완료 ! ({len(corpus):,}개의 리뷰, {sum(counter.values()):,}개의 단어)")


    if freq:
        buf = vsm.draw_bar_chart(counter, num_freq_words)
        st.download_button("그래프 저장", buf.getvalue(), "bar_chart.png", "image/png")

    if wc:
        buf = vsm.draw_wordcloud(counter, num_wc_words)
        st.download_button("워드클라우드 저장", buf.getvalue(), "wordcloud.png", "image/png")