# NaverApi 클래스 - OpenAPI 인터넷 통해서 데이터를 전달 받음
from urllib.request import Request, urlopen
from urllib.parse import quote
import datetime     # 현재시간 사용
import json         # 결과는 json으로 return


class NaverApi:
    # 생성자
    def __init__(self) -> None:
        print('Naver API 생성')

    # NaverAPI 호출함수
    def get_request_url(self, url):
        req = Request(url)
        # Naver API 개인별 인증
        req.add_header('X-Naver-Client-Id', 'hpNcLT4pOwTAmPBH4Zcc')
        req.add_header('X-Naver-Client-Secret', 'XSgisvB92y')

        try:
            res = urlopen(req)  # 요청 결과가 바로 돌아옴
            if res.getcode() == 200:    # response OK
                print(f'[{datetime.datetime.now()}] NAVER API 요청 성공')
                return res.read().decode('utf-8')
            else:
                print(f'[{datetime.datetime.now()}] NAVER API 요청 실패')
                return None
            
        except Exception as e:
            print(f'[{datetime.datetime.now()}] 예외발생 : {e}')
            return None

    # 호출함수        
    def get_naver_search(self, node, search, start, display):
        base_url = 'https://openapi.naver.com/v1/search'
        node_url = f'/{node}.json'
        params = f'?query={quote(search)}&start={start}&display={display}'

        url = base_url + node_url + params
        retData = self.get_request_url(url)

        if retData == None:
            return None
        else:
            return json.loads(retData) # json으로 return.

    # json 데이터 --> list로 변환
    def get_post_data(self, post, outputs):
        title = post['title']
        description = post['description']
        originallink = post['originallink']
        link = post['link']

        # 문자열로 들어온 걸 날짜형으로 변경
        pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d, %b, %Y, %H:%M:%S+0900')
        pubDate = pDate.strftime('%Y=%m-%d %H:%M:%S')

        # outputs에 옮기기


