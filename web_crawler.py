from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import re


TEST_URL = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!
driver = webdriver.Chrome('C:/Users/user/chromedriver') # 각자 컴퓨터 크롬 드라이버 경로

driver.get(TEST_URL)
user_agent = driver.find_element_by_css_selector('#user-agent').text
url_list=[]
df=pd.read_csv('url_temp.csv') #최종 url 넣기
for url in df.urls:
    
    driver.get(url)
    #--------------------------------------------------------------------------
    res = requests.get(url)
    temp_list =[]
    between_days = []
    soup = BeautifulSoup(res.content,'html.parser')
    # 성공 여부 파싱- 종속변수
    success= soup.select_one('''#container > div.reward-body-wrap > div > div.wd-ui-info-wrap > 
                                div.wd-ui-sub-opener-info > div.project-state-info > div.state-box > p.remaining-day.success''')
    if success == None: #실패한 프로젝트는 아무것도 파싱되지 않음, 즉 None타입을 반환함
        is_success=1
    else: 
        is_success=0 
    temp_list.append(is_success)
    print('성공 여부: ',is_success,' ->성공:0 , 실패:1')#성공:0 , 실패:1



    #1.제목 파싱-저장x
    title= soup.select_one('h2.title > a')
    title_name = title.get_text()
    print('제목:',title_name)

    #1-1 제목에 '앵콜' 포함 여부 //제품 앵콜:1 , 앵콜 x :0
    if '앵콜' not in title_name:
        is_refunding =0
    else:
        is_refunding=1
    print("앵콜 여부:",is_refunding)
    temp_list.append(is_refunding)


    # 2.카테고리 파싱
    category = soup.select_one('#container > div.reward-header > p > em')
    category_name= category.get_text()
    print("카테고리:",category_name)

    temp_list.append(category_name)

    #3.목표 펀딩금액, 4.펀딩 기간, 5.펀딩 시작 월 파싱
    day_temp = driver.find_element_by_xpath('//*[@id="container"]/div[6]/div/div[1]/div[2]/div/div/section/div[4]/div/div[5]/div/p[1]').text
    goal_money = day_temp.splitlines()[0].split()[2]
    goal_money = re.findall("\d",goal_money)
    goal_money = int("".join(goal_money))
    print(goal_money)
    temp_list.append(goal_money)

    #시작 월
    start_temp = day_temp.splitlines()[1].split()[2].split('-')[0].split('.')
    starting_day = datetime(int(start_temp[0]),int(start_temp[1]),int(start_temp[2]))
    starting_month = int(start_temp[1])
    print(starting_month)
    temp_list.append(starting_month)

    #끝날짜 -저장x
    end_temp = day_temp.splitlines()[1].split()[2].split('-')[1].split('.')
    end_day = datetime(int(end_temp[0]),int(end_temp[1]),int(end_temp[2]))
    print(end_day)

    #펀딩기간
    funding_time = (end_day - starting_day).days
    print(funding_time)
    temp_list.append(funding_time)

    # 6.사진 개수
    imgs= soup.find_all('img')
    img_count=len(imgs)
    print('이미지 개수:',img_count)
    temp_list.append(img_count)

    #7.리워드 개수
    reward=soup.select_one('#container > div.reward-body-wrap > div > div.wd-ui-info-wrap > div.wd-ui-sub-opener-info > div.moveRewards > div')
    reward_button=soup.select('button.rightinfo-reward-list')
    reward_num=len(reward_button)
    print('리워드 개수:',reward_num)
    temp_list.append(reward_num)

    #커뮤니티 파싱 시작

    comunity = driver.find_element_by_xpath('//*[@id="container"]/div[5]/ul/li[5]/a') #클릭 위치(커뮤니티)
    comunity.click()
    time.sleep(0.5)

    #응원.의견.체험리뷰 숫자 있는지 확인
    try :
        coments = driver.find_element_by_xpath('//*[@id="reward-static-community-app"]/div/div[3]/div[1]/div/p/em')
        coments_number = int(coments.text)
        coments_range_number = (coments_number//15)+1
    except:
        pass

    #더보기 누르기


    if coments_number>15:
        moreview_btn = driver.find_element_by_xpath("//*[@id='reward-static-community-app']/div/div[3]/div[4]/button") # 더 보기 위치
        for i in range(1,coments_range_number):
            moreview_btn.click()
            time.sleep(0.7)


    #날짜 추출
    comment_temp = []

    for k in range(1,coments_number+1):        
        comment_list=[]
        comment_list.append("//*[@id='reward-static-community-app']/div/div[3]/div[3]/div/div[%d]/div[1]/div[2]/div[1]/span[2]"%k)
        comment_list.append("//*[@id='reward-static-community-app']/div/div[3]/div[3]/div/div[%d]/div[1]/div[2]/div[1]/span[3]"%k)
        comment_list.append("//*[@id='reward-static-community-app']/div/div[3]/div[3]/div/div[%d]/div/div[2]/div[1]/span[2]"%k)
        comment_list.append("//*[@id='reward-static-community-app']/div/div[3]/div[3]/div/div[%d]/div/div[2]/div[1]/span[3]"%k)



        for j in comment_list:
            try:
                com = driver.find_element_by_xpath(j).text
                if com != '펀딩 참여자' and com[-1] != "전":
                    com_num = re.findall("\d",com)
                    year = int("".join(com_num[0:4]))
                    month = int("".join(com_num[4:6]))
                    day = int("".join(com_num[6:8]))

                    support_day = datetime(year,month,day)
                    bet_day = (support_day - starting_day).days
                    between_days.append(bet_day)

                    comment_temp.append(k)
                    break

                else : 
                    pass
            except:
                pass

    comment_text = []
    for a in comment_temp:
        text_temp = []
        text_temp.append('//*[@id="reward-static-community-app"]/div/div[3]/div[3]/div/div[%d]/div[1]/div[2]/div[2]/div/div'%a)
        text_temp.append('//*[@id="reward-static-community-app"]/div/div[3]/div[3]/div/div[%d]/div/div[2]/div[2]/div/div'%a)

        for b in text_temp:
            try:
                t_temp = driver.find_element_by_xpath(b).text
                comment_text.append(t_temp)
                break
            except:
                pass

    support_tap = driver.find_element_by_xpath('//*[@id="container"]/div[5]/ul/li[6]/a') #클릭 위치(서포트)
    temp = support_tap.get_attribute('text') #서프트 있는지 확인
    temp_list.append(between_days)
    temp_list.append(comment_text)

    #스토리에서 서포트 넘어갈때 숫자체크
    if any(chr.isdigit() for chr in temp):
        li_comunity_num = temp.split()
        support_tap.click()
        time.sleep(2)

    support = driver.find_element_by_xpath('//*[@id="container"]/div[6]/div/div/div[1]/div[1]/div[1]/p[5]/strong')
    support_number = int(support.text)
    support_range_number = (support_number//20)+1
    facebook_date = [] # 페이스북 지지서명 날짜 -펀딩 시작일
    funding_date = [] # 펀딩 참여 날짜 - 펀딩 시작일


    moreview_btn = driver.find_element_by_xpath('//*[@id="reward-static-supports-list-app"]/div/div/div/div[2]/button') 
    facebook_count = 0
    funding_count = 0 
    sup_data = []

    # 더보기 버튼 누르기
    if support_number>20:
        for i in range(2,support_range_number):
            moreview_btn.click()
            time.sleep(2)



    #서포트 내용 class
    sup = driver.find_elements_by_class_name('RewardSupporterItem_container__1UTDZ') 
    sup_contents = []



    for i in sup:

        i = i.text
        sup_contents.append(i)


        #기간 차이
        temp = i.splitlines()
        date = temp[1]
        date = date.split('.')
        #print(date[-1][-1])
        if date[-1][-1] !="전":
            support_day = datetime(int(date[0]),int(date[1]),int(date[2]))
            bet_day = (support_day - starting_day).days

            if 'Facebook' in i:
                facebook_count += 1
                facebook_date.append(bet_day)
            else:
                funding_count+=1
                funding_date.append(bet_day)
    temp_list.append(facebook_date)
    temp_list.append(funding_date)
        #서포트 숫자는 support_number
        #페이스북 지지자는 facebook_count
    url_list.append(temp_list)

     #upport_number와 facebook_count 각기 다른 리스트에 담은 엑셀로 저장
