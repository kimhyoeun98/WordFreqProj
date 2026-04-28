import os
import urllib.request 
import json as j
import time as t
import pandas as pd

class NaverNewsCrawler:
    def __init__(self, client_id, client_secret):
        """
        API 사용을 위한 인증 정보 초기화 및 데이터 저장소 준비
        :param client_id: 네이버 개발자 센터에서 발급받은 클라이언트 아이디
        :param client_secret: 네이버 개발자 센터에서 발급받은 클라이언트 시크릿
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.results = [] # 수집된 뉴스 아이템들을 담을 리스트

    def crawl(self, keyword, total_count = 100):
        """
        뉴스 검색 API를 사용하여 데이터를 수집하는 핵심 메서드
        :param keyword: 검색할 키워드 (예: '인공지능')
        :param total_count: 수집할 아이템 총 개수 (최대 1000개)
        """
        self.results = [] # 실행 시마다 결과 리스트 초기화
        start = 1        # API 검색 시작 위치 (최초 1번부터 시작)
        display = 10     # 한 번의 API 호출로 가져올 뉴스 개수 (최대 100개 가능)

        # 수집 목표 개수에 도달할 때까지 반복 호출
        while start <= total_count:
            # 1. 한글 검색어를 URL에 사용할 수 있도록 인코딩 (UTF-8)
            encText = urllib.parse.quote(keyword)
            # 2. 요청 URL 구성 (검색어, 시작 위치, 표시 개수 포함)
            url = f'https://openapi.naver.com/v1/search/news?query={encText}&start={start}&display={display}'

            # 3. HTTP 요청 객체 생성 및 인증 헤더 추가
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", self.client_id)
            request.add_header("X-Naver-Client-Secret", self.client_secret)

            try:
                # 4. 실제 API 호출 및 응답 받기
                response = urllib.request.urlopen(request)
                
                # 응답 코드가 200(성공)인 경우
                if response.getcode() == 200:
                    # 응답 바이트 데이터를 UTF-8로 디코딩하고 JSON 형식으로 파싱
                    data = j.loads(response.read().decode('utf-8'))
                    items = data.get('items', []) # 'items' 키의 값(뉴스 리스트) 추출

                    # 더 이상 가져올 뉴스가 없으면 반복 중단
                    if not items:
                        break

                    # 수집된 리스트를 전체 결과 리스트에 확장(추가)
                    self.results.extend(items)
                    print(f'{keyword} - {start}번부터 {len(items)}개 수집 완료')

                    # 다음 수집을 위해 시작 위치 갱신
                    start += display
                    # API 서버 부하를 방지하고 차단을 막기 위해 0.5초간 대기
                    t.sleep(0.5)

                else:
                    # 200이 아닌 에러 코드 출력 시 반복 중단
                    print(f'Error Code: {response.getcode()}')
                    break
            except Exception as e:
                # 네트워크 문제나 기타 예외 처리
                print(f'Error: {e}')
                break

        return self.results
    

    def save_csv(self, file_path):
        """
        수집된 데이터를 CSV 파일로 저장
        :param file_path: 저장할 파일의 경로 (파일명 포함)
        """
        # 저장할 데이터가 없는 경우 종료
        if not self.results:
            print('No Data to Save')
            return
        
        # 1. 리스트 형태의 데이터를 Pandas DataFrame(표 형식)으로 변환
        df = pd.DataFrame(self.results)

        # 2. 경로에서 폴더 부분만 추출하여 해당 폴더가 없으면 생성
        # 예: './data/news.csv' -> './data/' 폴더 생성
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 3. CSV 파일로 저장
        # index=False: 행 번호 제외
        # encoding='utf-8-sig': 엑셀에서 한글 깨짐 방지를 위한 인코딩 방식
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f'Save Success: {file_path}')
