from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#headless 설정을 통해 크롤링 봇이 사람이 스크롤 내리는 것처럼 보이게 하기
TEST_URL = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!
driver = webdriver.Chrome('C:/Users/user/chromedriver') # 각자 컴퓨터 크롬 드라이버 경로

driver.get(TEST_URL)

user_agent = driver.find_element_by_css_selector('#user-agent').text

print('User-Agent: ', user_agent)

# 드라이버 위치 경로 입력
driver.get('https://www.wadiz.kr/web/wreward/main?keyword=&endYn=ALL&order=recommend')

SCROLL_PAUSE_SEC1 = 1
# 스크롤 높이 가져옴
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 끝까지 스크롤 다운
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    time.sleep(SCROLL_PAUSE_SEC1)
    SCROLL_PAUSE_SEC1 =  SCROLL_PAUSE_SEC1 +0.5
    

    # 스크롤 다운 후 스크롤 높이 다시 가져옴
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        time.sleep(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
    last_height = new_height
    
    
    #url 파싱 후 문자 형식 통일- 16번 기부,후원 카테고리로 파싱했음
urllists_16=[] #파싱 후 리스트
urllist_16=[] # 파싱+수정 후 리스트
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
mydata = soup.select('#main-app > div.MainWrapper_content__GZkTa > div > div.RewardProjectListApp_container__1ZYeD > div.ProjectCardList_container__3Y14k > div.ProjectCardList_list__1YBa2 div > div > div > div > div.RewardProjectCard_infoTop__3QR5w > a')
for item in mydata:
    urllists_16.append(item.get('href').split('?')[0])
for url in urllists_16:
    if 'https' in url:
        url =url.replace(url[0:-5],"/web/campaign/detail/"+str(url[-5:0]))
    new_url='https://www.wadiz.kr/' + url
    print(new_url)
    urllist_16.append(new_url)

#리스트를 데이터프레임으로 변환 후 csv파일로 저장
df_16= pd.DataFrame(urllist_16)
df_16.to_csv("url_16.csv")

# mysql 연동
import pymysql

conn =pymysql.connect(host='localhost',user='root',password='wjsckdqja1',db='capston', charset='utf8')
cursor= conn.cursor()
#url 주소를 product Table 안에 insert 
sql = "insert into product(id,url) values(%d,%s);"
for i in range(len(urllist_16)):
    cursor.execute(sql,(i+1,urllist_16[i]))
conn.commit()
conn.close()
