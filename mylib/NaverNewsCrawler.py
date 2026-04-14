import os
import urllib.request 
import json as j
import time as t
import pandas as pd

class NaverNewsCrawler:
    def __init__(self, client_id, client_secret):
        """API 사용을 위한 인증 정보 초기화"""
        self.client_id = client_id
        self.client_secret = client_secret
        self.results = []

    def crawl(self, keyword, total_count = 100):
        """
        뉴스 검색 API를 사용하여 데이터를 수집.
        :param keyword: 검색어
        :param total_count: 수집할 아이템 총 개수 (최대 1000개)
        """
        self.results = []
        start = 1
        display = 10 # 한 번 호출 시 가져올 갯수 10개

        while start <= total_count:
            encText = urllib.parse.quote(keyword)
            url = f'https://openapi.naver.com/v1/search/news?query={encText}&start={start}&display={display}'

            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", self.client_id)
            request.add_header("X-Naver-Client-Secret", self.client_secret)

            try:
                response = urllib.request.urlopen(request)
                
                if response.getcode() == 200:
                    data = j.loads(response.read().decode('utf-8'))
                    items = data.get('items', [])

                    if not items:
                        break

                    self.results.extend(items)
                    print(f'{keyword} - {start}번부터 {len(items)}개 수집 완료')

                    start += display
                    t.sleep(0.5)

                else:
                    print(f'Error Code: {response.getcode()}')
                    break
            except Exception as e:
                print(f'Error: {e}')
                break

        return self.results
    

    def save_csv(self, file_path):

        if not self.results:
            print('No Data to Save')
            return
        
        df = pd.DataFrame(self.results)


        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f'Save Success: {file_path}')