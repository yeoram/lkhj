
import urllib.request
import requests
import json
import pandas as pd



CLIENT_ID = "서비스키"
CLIENT_SECRET = "서비스 시크릿 넘버"
BASE_URL = "https://openapi.naver.com/v1/search/"
DL_URL = "https://openapi.naver.com/v1/datalab/search" #데이터랩 url



'''
naver api 이용해서 검색 후 csv 파일로 저장
search_type = 'blog.json''book.json','news.json','shop.json'
    --> 'shop.json'은 전시회/연극/뮤지컬 등을 검색할 때 사용
display : 몇 개를 받아 올 건지
'''
def search_naver(keyword, search_type, display):
    url = BASE_URL +search_type
    params ={ "query":keyword, "display": display}
    
    headers ={ "X-Naver-Client-Id":CLIENT_ID, "X-Naver-Client-Secret":CLIENT_SECRET}
    
    response = requests.get(url, params= params, headers=headers)
    data = response.json()
    
    titles = []
    if "items" in data:
        items = data['items']
        for item in items:
            #print(item)
            if "<b>" in item['title']:
                item['title']= item['title'].replace('<b>', ' ')
                item['title'] = item['title'].replace('</b>',' ')
            titles.append([item['title'], item['link']])
            #print(titles)
        df = pd.DataFrame(titles, columns=['title', 'link'])
        df.to_csv(f"data/naver_{keyword}.csv")
    else:
        print('검색 결과 없음')

'''
데이터랩에서 키워드 검색량 알아오는 함수
json으로 받아오는 거 하다가 실패해서 구글링으로 xml로 받아오게 만들었어요 
'''
def get_datalab_result(body):
    request = urllib.request.Request(DL_URL)
    request.add_header("X-Naver-Client-Id", CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        # Json Result
        response_body = response.read()
        result = json.loads(response_body)

        response_results = pd.DataFrame()
        for data in result['results']:
            result=pd.DataFrame(data['data'])
            result['title']=data['title']

            response_results = pd.concat([response_results,result])
    else:
        response_results ="Error Code:" + rescode
        
    return response_results

'''
데이터랩 api 호출 시 넘겨주는 parameter를 형식에 맞춰서 변환해주는 함수

'''
def get_params(startDate,endDate,timeUnit,keywordGroups):
    params = json.dumps({"startDate": startDate,
        "endDate": endDate,
        "timeUnit": timeUnit,
        "keywordGroups": keywordGroups}, ensure_ascii=False)
    
    return params

'''
데이터랩 api 호출 시 넘겨주는 parameter 중 keywordGroups를 만드는 함수
굳이 함수로 만든 건 여러 개의 키워드를 한 번에 검색할 수 있게 하기 위해서입니다
'''

def input_keyword(keyword):
    keywordGroups=[]
    print(type(keyword['groupName']))
    keywordGroup = {
        'groupName' : keyword['groupName'],
        'keywords' : keyword['keywords']
    }
    keywordGroups.append(keywordGroup)
    print(keywordGroups)
    
    return keywordGroups

