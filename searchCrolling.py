'''
크롤링 하는 함수를 담으려고 만든 py
네이버 api에서 영화 순위를 가지고 오는게 잘 되지 않아 그냥 크롤링으로 했는데
추우 네이버 말고 다른 사이트에서 크롤링 할 일이 생기면 이 파일에서 함수를 만들면
좋을 것 같습니다
'''
from selenium import webdriver 
from selenium.webdriver.common.by import By

import time

import pandas as pd


'''
크롬 드라이버 구동 
option을 이용해 크롬을 띄우지 않고 검색
마지막 옵션은 로봇이 아니라는 페이크라고 하는데....
'''
def run_chrome():
    chrome_options = webdriver.ChromeOptions()
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


driver = run_chrome()
movie_croll(driver)


driver.quit()


#main_pack > div.sc_new.cs_common_module.case_list.color_5._au_movie_list_content_wrap > div.cm_content_wrap > div > div > div.mflick > div._panel_popular._tab_content > div.list_image_info.type_pure_top > div > ul > li

#main_pack > div.sc_new.cs_common_module.case_list.color_5._au_movie_list_content_wrap > div.cm_content_wrap > div > div > div > div.card_content._result_area > div.card_area._panel > div > div.data_area > div > div.title._ellipsis

