from NaverNewsCrawler import NaverNewsCrawler

# 1. 인증 정보 설정 (네이버 개발자 센터에서 발급받은 본인의 정보를 입력하세요)
client_id = "3mBVTgYjeeXH5teGFhoM"
client_secret = "JTKp3FEVkn"

# 2. 크롤러 객체 생성
crawler = NaverNewsCrawler(client_id, client_secret)

# 3. 데이터 수집 실행 (예: '인공지능' 키워드로 30개 수집)
keyword = "2026년 신작 게임"
crawled_data = crawler.crawl(keyword, total_count=30)

# 4. 수집된 결과 확인 (상위 3개만 출력해보기)
print("\n--- 수집 결과 샘플 ---")
for item in crawled_data[:3]:
    print(f"제목: {item['title']}")
    print(f"링크: {item['link']}")
    print("-" * 20)

# 5. CSV 파일로 저장
# 파일 경로 앞에 './data/'를 붙이면 data 폴더가 자동으로 생성됩니다.
save_path = f"./data/{keyword}_news_test.csv"
crawler.save_csv(save_path)