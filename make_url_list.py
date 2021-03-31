from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

TEST_URL = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!
driver = webdriver.Chrome('C:\chromedriver\chromedriver') # 각자 컴퓨터 크롬 드라이버 경로-> 이거 바꾸기

driver.get(TEST_URL)

#https://www.wadiz.kr/web/campaign/detail/101368 댓글 없음
#https://www.wadiz.kr/web/campaign/detail/98041 댓글 있음

user_agent = driver.find_element_by_css_selector('#user-agent').text

df = pd.read_csv('result.csv') #엑셀 불러오기
i=0
yes_urls_list = []
#매겨준 번호대로 엑셀에서 전처리해서 쓰셈->중요 
for url in df.urls:
    driver.get(url)
    driver.implicitly_wait(1)
    try:
        comunity = driver.find_element_by_xpath('//*[@id="container"]/div[5]/ul/li[5]/a') #클릭 위치(커뮤니티)
        temp = comunity.get_attribute('text') #댓글 있는지 확인

        #스토리에서 커뮤니티 넘어갈때 숫자체크
        if any(chr.isdigit() for chr in temp):
            li_comunity_num = temp.split()
            comunity.click()
            time.sleep(0.5)

            #응원.칭찬댓글,있는지확인
            try:
                coments = driver.find_element_by_xpath("//*[@id='reward-static-community-app']/div/div[3]/div[1]/div/p/em")
                yes_urls_list.append(url)
                print(url)
            except:
                pass

        else:
            pass
    except NoSuchElementException:
        pass
        
print(i+'번째 까지 수집')
