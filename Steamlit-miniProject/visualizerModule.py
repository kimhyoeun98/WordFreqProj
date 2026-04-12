import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
import textMiningModule as tmm
import os
import io


def get_font_info():
    """한글 폰트 정보 반환"""
    font_path = os.getcwd() + '/myFonts'
    font_file = font_path + '/NanumGothic.ttf'
    font_name = 'NanumGothic'
    return font_path, font_file, font_name


@st.cache_data
def register_korean_font():
    """한글 폰트 등록"""
    font_path, _, _ = get_font_info()
    font_files = font_manager.findSystemFonts(fontpaths=[font_path])
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)
    font_manager._load_fontmanager(try_read_cache=False)


@st.dialog("데이터 미리보기", width='large')
def show_data_dialog(data_df):
    """데이터 미리보기 다이얼로그"""
    num_rows = st.number_input("확인할 행 수", min_value=1, max_value=100, value=10)
    st.dataframe(data_df.head(num_rows))


def draw_bar_chart(counter, num_words):
    _, _, font_name = get_font_info()
    plt.rc('font', family=font_name)

    top_words = counter.most_common(num_words)
    words = [word for word, _ in top_words]
    counts = [count for _, count in top_words]

    fig, ax = plt.subplots(figsize=(8, num_words * 0.35))
    ax.barh(words[::-1], counts[::-1], color='steelblue')
    ax.set_xlabel('빈도수')
    ax.set_ylabel('단어')
    ax.set_title(f'상위 {num_words}개 단어 빈도수')
    st.pyplot(fig)

    # ✅ buf만 반환
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    return buf


def draw_wordcloud(counter, num_words):
    _, font_file, _ = get_font_info()
    
    with st.spinner("워드클라우드 생성 중..."):
        wordcloud = tmm.generate_wordcloud(counter, num_words, font_file)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        # ✅ buf만 반환
        import io
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        return buf