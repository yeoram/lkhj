from selenium import webdriver 
from selenium.webdriver.common.by import By

import time

import pandas as pd


# In[2]:


'''
크롬 드라이버 구동 
option을 이용해 크롬을 띄우지 않고 검색
마지막 옵션은 로봇이 아니라는 페이크라고 하는데....
'''
def run_chrome():
    chrome_options = webdriver.ChromeOptions()
    #chrome.options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko")
    driver = webdriver.Chrome('C:/Users/eoyeo/Desktop/sparta/project', options=chrome_options)
    
    return driver


'''
네이버에서 현재상영영화 크롤링 함수
'''
def movie_croll(driver):
    
    driver.get('https://search.naver.com/search.naver?query=현재상영영화')
    time.sleep(2)
    rank_elements = driver.find_elements(By.CSS_SELECTOR, "#main_pack > div.sc_new.cs_common_module.case_list.color_5._au_movie_list_content_wrap > div.cm_content_wrap > div > div > div > div.card_content._result_area > div.card_area._panel > div > div.data_area > div > div.title._ellipsis")
    movie_rank = [element.text for element in rank_elements]
    
    mv_titles=[]
    for title in movie_rank:
        mv_titles.append(title)
    df = pd.DataFrame(mv_titles, columns=['movie rank'])
    df.to_csv(f"data/naver_현재상영영화.csv")


'''
날씨 크롤링 하는 함수
'''
def weather_croll(driver):
    driver.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=날씨')
    time.sleep(2)
    wthr_elements = driver.find_elements(By.CSS_SELECTOR,'#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div > div > div.weather_info > div > div._today')
    #print(wthr_elements)
    weathers = [element.text for element in wthr_elements]
    today_weather = []
    for weather in weathers:
        today_weather.append(weather)
        
    return today_weather


'''
크롤링 해온 날씨에서 원하는 정보만 추출하는 함수
'''
def get_weatherInfo(weather):
    weatherInfo = {}
    strWeather = str(weather)  #weather가 리스트형으로 넘어오기때문에 문자형으로 변환
    strWeather=strWeather.replace('\\n', ' ') #포함되어 있는 기호들 제거
    strWeather = strWeather.replace('°','')
    strWeather = strWeather.replace("['","")
    strWeather = strWeather.split(" ") #다시 리스트로 쪼개기
    for i, data in enumerate(strWeather): #필요한 정보 추출
        if i==0:
            weatherInfo['state'] = data
        elif i==3:
            weatherInfo['temp'] = data
        elif i==9:
            weatherInfo['windchill']=data
        elif i==11:
            weatherInfo['humidity'] =data
    return weatherInfo #딕셔너리 형태로 넘겨주기
        

driver = run_chrome()
#movie_croll(driver)
weather = weather_croll(driver)


weatherInfo = get_weatherInfo(weather)
print(weatherInfo)


driver.quit()


#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div > div > div.weather_info > div > div._today

#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div > div > div.weather_info > div


#main_pack > div.sc_new.cs_common_module.case_list.color_5._au_movie_list_content_wrap > div.cm_content_wrap > div > div > div.mflick > div._panel_popular._tab_content > div.list_image_info.type_pure_top > div > ul > li

#main_pack > div.sc_new.cs_common_module.case_list.color_5._au_movie_list_content_wrap > div.cm_content_wrap > div > div > div > div.card_content._result_area > div.card_area._panel > div > div.data_area > div > div.title._ellipsis

