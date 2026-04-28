# NaverNewsCrawler 모듈에서 NaverNewsCrawler 클래스를 가져옵니다.
# (이 클래스는 별도의 .py 파일로 정의되어 있어야 합니다.)
from NaverNewsCrawler import NaverNewsCrawler

# 1. 인증 정보 설정
# 네이버 개발자 센터(Naver Developers)에서 애플리케이션을 등록하고 발급받은 API 키를 입력하는 단계입니다.
# 클라이언트 ID와 시크릿은 API 호출 시 본인 인증을 위해 사용됩니다.
client_id = "3mBVTgYjeeXH5teGFhoM"
client_secret = "JTKp3FEVkn"

# 2. 크롤러 객체 생성
# 위에서 설정한 ID와 Secret 값을 인자로 전달하여 네이버 API와 통신할 'crawler' 객체를 인스턴스화합니다.
crawler = NaverNewsCrawler(client_id, client_secret)

# 3. 데이터 수집 실행
# 'crawl' 메서드를 호출하여 검색어(keyword)와 관련된 뉴스 데이터를 가져옵니다.
# total_count=30은 최대 30개의 뉴스 아이템을 가져오겠다는 의미입니다.
keyword = "2026년 신작 게임"
crawled_data = crawler.crawl(keyword, total_count=30)

# 4. 수집된 결과 확인
# 수집된 데이터(리스트 형태) 중 슬라이싱([:3])을 사용하여 상위 3개 데이터만 반복문으로 출력해 봅니다.
print("\n--- 수집 결과 샘플 ---")
for item in crawled_data[:3]:
    # 각 뉴스 아이템의 'title'(제목)과 'link'(기사 주소)를 화면에 표시합니다.
    print(f"제목: {item['title']}")
    print(f"링크: {item['link']}")
    print("-" * 20)

# 5. CSV 파일로 저장
# 수집한 데이터를 엑셀 등에서 열어볼 수 있는 CSV 형식으로 저장합니다.
# f-string을 이용해 파일명에 키워드를 포함시켰으며, 경로에 폴더가 없으면 자동으로 생성하는 로직이 포함되어 있습니다.
save_path = f"./data/{keyword}_news_test.csv"
crawler.save_csv(save_path)
