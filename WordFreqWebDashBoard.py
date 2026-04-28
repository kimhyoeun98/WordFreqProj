import streamlit as st
import pandas as pd
import textMiningModule as tmm # 텍스트 처리 로직 모듈
import visualizerModule as vsm   # 시각화 및 UI 보조 모듈

# 1. 페이지 기본 설정 (브라우저 탭에 표시될 제목과 아이콘)
st.set_page_config(
    page_title="단어 빈도수 시각화",
    page_icon="👀"
)

# 시각화에 필요한 한글 폰트 미리 등록
vsm.register_korean_font()

# 2. 사이드바(Sidebar) 영역 구성
with st.sidebar:
    st.header("데이터 업로드")
    # CSV 파일 업로더 생성
    data_file = st.file_uploader("파일 선택", type=['csv'])
    # 분석할 텍스트가 들어있는 컬럼명 입력 받기
    column_name = st.text_input("데이터가 있는 컬럼명", value="review")

    # 데이터 미리보기 버튼 로직
    if st.button("데이터 미리보기"):
        if data_file:
            # 업로드된 파일을 읽어와서 다이얼로그(팝업)로 표시
            data_df = pd.read_csv(data_file)
            vsm.show_data_dialog(data_df)
        else:
            st.warning("파일을 먼저 업로드해주세요.")
    
    st.write("---") # 구분선
    st.write("분석 설정")
    
    # st.form을 사용하여 사용자가 여러 설정을 마친 후 한 번에 적용하도록 함
    with st.form("form"):
        # 빈도수 그래프 설정
        freq = st.checkbox("빈도수 그래프", value=True)
        num_freq_words = st.slider("그래프 단어 수", 10, 50, 20, 1, key="freq_slider")

        # 워드클라우드 설정
        wc = st.checkbox('워드클라우드')
        num_wc_words = st.slider('클라우드 단어 수', 20, 500, 50, 10, key="wc_slider")

        # 폼 전송 버튼 (클릭 시 페이지가 리로드되며 아래 분석 로직 실행)
        submitted = st.form_submit_button("분석 시작")

# 3. 메인 화면(Main Content) 영역 구성
st.title("📊 단어 빈도수 시각화 서비스")
# 앱 사용 안내 메시지 출력
status = st.info('분석할 파일을 업로드하고, 시각화 수단을 선택한 후 "분석 시작" 버튼을 클릭하세요.')

# 4. 분석 실행 로직 (버튼 클릭 시 작동)
if submitted:
    # 예외 처리: 파일이 없는 경우
    if not data_file:
        st.error("분석할 데이터 파일을 업로드 한 후 분석 시작을 눌러주세요.")
        st.stop() # 실행 중단
    
    # 예외 처리: 시각화 도구를 아무것도 선택하지 않은 경우
    if not freq and not wc:
        st.warning("빈도수 그래프 또는 워드클라우드 중 하나 이상 선택해주세요.")
        st.stop()

    # 진행 상태 표시 업데이트
    status.info("데이터 분석 및 토큰화 진행 중 ...")

    # 텍스트 데이터 로드 (tmm 모듈 활용)
    corpus, data_df = tmm.load_corpus_from_csv(data_file, column_name)
    
    # 컬럼명이 잘못되었거나 데이터가 없는 경우 처리
    if not corpus:
        st.error(f"컬럼명 '{column_name}'을 찾을 수 없습니다. 다시 확인 해주세요.")
        st.stop()

    # 단어 빈도 분석 수행 (tmm 모듈 활용)
    counter = tmm.analyze_word_freq(corpus)

    # 분석 결과 요약 정보 표시
    status.success(f"분석 완료 ! (총 {len(corpus):,}개의 문장, {sum(counter.values()):,}개의 의미 있는 단어 추출)")

    # 5. 시각화 결과 출력 및 다운로드 버튼 생성
    
    # 빈도수 막대 그래프 출력 세션
    if freq:
        st.subheader("📍 단어 빈도수 그래프")
        buf = vsm.draw_bar_chart(counter, num_freq_words) # 그래프 그리고 이미지 버퍼 받기
        # 다운로드 버튼 생성 (버퍼에 담긴 이미지 데이터를 png 파일로 제공)
        st.download_button("그래프 이미지 저장", buf.getvalue(), "bar_chart.png", "image/png")

    # 워드클라우드 출력 세션
    if wc:
        st.subheader("☁️ 워드클라우드")
        buf = vsm.draw_wordcloud(counter, num_wc_words) # 워드클라우드 생성 및 이미지 버퍼 받기
        # 다운로드 버튼 생성
        st.download_button("워드클라우드 이미지 저장", buf.getvalue(), "wordcloud.png", "image/png")
