import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
import textMiningModule as tmm # 이전 단계에서 만든 텍스트 마이닝 모듈
import os
import io


def get_font_info():
    """
    프로젝트 내 나눔고딕 폰트의 경로와 정보를 반환합니다.
    (한글 깨짐 방지를 위해 로컬 폰트를 사용하도록 설정)
    """
    font_path = os.getcwd() + '/myFonts'      # 폰트가 저장된 폴더 경로
    font_file = font_path + '/NanumGothic.ttf' # 실제 폰트 파일 경로
    font_name = 'NanumGothic'                  # 설정할 폰트 이름
    return font_path, font_file, font_name


@st.cache_data
def register_korean_font():
    """
    시스템 및 Matplotlib에 한글 폰트를 등록합니다.
    @st.cache_data를 사용하여 앱 실행 시 딱 한 번만 수행되도록 캐싱합니다.
    """
    font_path, _, _ = get_font_info()
    # 지정된 경로에서 폰트 파일들을 찾아 리스트로 반환
    font_files = font_manager.findSystemFonts(fontpaths=[font_path])
    
    # 찾은 폰트들을 Matplotlib 폰트 매니저에 하나씩 추가
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)
    
    # 폰트 매니저를 새로고침하여 등록된 폰트를 사용할 수 있게 함
    font_manager._load_fontmanager(try_read_cache=False)


@st.dialog("데이터 미리보기", width='large')
def show_data_dialog(data_df):
    """
    Streamlit의 다이얼로그(팝업창) 기능을 이용해 데이터프레임을 미리 보여줍니다.
    :param data_df: 불러온 전체 데이터프레임
    """
    # 사용자로부터 몇 줄을 볼지 입력받음 (기본 10줄)
    num_rows = st.number_input("확인할 행 수", min_value=1, max_value=100, value=10)
    # 입력받은 수만큼 데이터 상단(head) 출력
    st.dataframe(data_df.head(num_rows))


def draw_bar_chart(counter, num_words):
    """
    단어 빈도수를 수평 막대 그래프로 화면에 그리고, 
    나중에 다운로드할 수 있도록 이미지 버퍼(BytesIO)를 반환합니다.
    """
    _, _, font_name = get_font_info()
    plt.rc('font', family=font_name) # 그래프 한글 폰트 적용

    # 빈도수가 높은 단어 추출
    top_words = counter.most_common(num_words)
    words = [word for word, _ in top_words]
    counts = [count for _, count in top_words]

    # 그래프 객체 생성 (단어 개수에 따라 그래프 높이를 유동적으로 조절)
    fig, ax = plt.subplots(figsize=(8, num_words * 0.35))
    ax.barh(words[::-1], counts[::-1], color='steelblue') # 역순으로 그려 빈도가 높은 게 위로 오게 함
    ax.set_xlabel('빈도수')
    ax.set_ylabel('단어')
    ax.set_title(f'상위 {num_words}개 단어 빈도수')
    
    # Streamlit 화면에 그래프 출력
    st.pyplot(fig)

    # 그래프를 메모리 버퍼(io.BytesIO)에 저장하여 반환
    # (파일로 물리적 저장을 하지 않고도 이미지를 전달할 수 있음)
    import io
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    return buf


def draw_wordcloud(counter, num_words):
    """
    워드클라우드를 생성하여 화면에 출력하고, 이미지 버퍼를 반환합니다.
    """
    _, font_file, _ = get_font_info()
    
    # 처리 시간이 걸릴 수 있으므로 스피너(로딩바) 표시
    with st.spinner("워드클라우드 생성 중..."):
        # tmm 모듈의 함수를 호출하여 워드클라우드 객체 생성
        wordcloud = tmm.generate_wordcloud(counter, num_words, font_file)
        
        # Matplotlib을 이용해 워드클라우드 시각화
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off') # 눈금과 축 숨김
        st.pyplot(fig)

        # 이미지 데이터를 메모리에 바이트 형태로 저장 (다운로드 버튼 등에 활용 가능)
        import io
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        return buf
