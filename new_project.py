from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import requests
import time

TEST_URL = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!

driver = webdriver.Chrome(r'C:/Users/LGPC/Desktop/project2/chromedriver') # 각자 컴퓨터 크롬 드라이버 경로

driver.get('https://www.wadiz.kr/web/main')


#스크롤 내리기
driver.maximize_window()
prev_height = driver.execute_script("window.scrollTo(0, 3000)")

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

reallist=[]
try:
    
    for i in range(2,8):
        time.sleep(3)
        driver.find_element_by_css_selector('#main-app > div.MainWrapper_content__GZkTa > div > div:nth-child(4) > article > div:nth-child(2) > div > section > div > ul > div > div:nth-child(%d) > div > a > article > div.commons_thumbnail__3wYGv.CardType_thumbnail__2dtTe.commons_active__1tjD5 > span'%i).click()
        time.sleep(2)
        reallist.append(driver.current_url)
        driver.back()

#2번째
    
    for i in range(2,8):
        time.sleep(2) #버튼 누르기
        driver.find_element_by_css_selector("#main-app > div.MainWrapper_content__GZkTa > div > div:nth-child(4) > article > div:nth-child(2) > div > section > div > ul > div > div.DebutFundingDesktop_page__2fUBj > div > ul > li:nth-child(2) > button").click()
        time.sleep(3)
        driver.find_element_by_css_selector('#main-app > div.MainWrapper_content__GZkTa > div > div:nth-child(4) > article > div:nth-child(2) > div > section > div > ul > div > div:nth-child(%d) > div > a > article > div.commons_thumbnail__3wYGv.CardType_thumbnail__2dtTe.commons_active__1tjD5 > span'%i).click()
        time.sleep(2)
        reallist.append(driver.current_url)
        driver.back()

#3번째
    
    for i in range(2,8):
        time.sleep(2) #버튼 누르기
        driver.find_element_by_css_selector("#main-app > div.MainWrapper_content__GZkTa > div > div:nth-child(4) > article > div:nth-child(2) > div > section > div > ul > div > div.DebutFundingDesktop_page__2fUBj > div > ul > li:nth-child(3) > button").click()
        time.sleep(3)
        driver.find_element_by_css_selector('#main-app > div.MainWrapper_content__GZkTa > div > div:nth-child(4) > article > div:nth-child(2) > div > section > div > ul > div > div:nth-child(%d) > div > a > article > div.commons_thumbnail__3wYGv.CardType_thumbnail__2dtTe.commons_active__1tjD5 > span'%i).click()
        time.sleep(2)
        reallist.append(driver.current_url)
        driver.back()
    

#4번째

    for i in range(2,8):
        time.sleep(2) #버튼 누르기
        driver.find_element_by_css_selector("#main-app > div.MainWrapper_content__GZkTa > div > div:nth-child(4) > article > div:nth-child(2) > div > section > div > ul > div > div.DebutFundingDesktop_page__2fUBj > div > ul > li:nth-child(4) > button").click()
        time.sleep(3)
        driver.find_element_by_css_selector('#main-app > div.MainWrapper_content__GZkTa > div > div:nth-child(4) > article > div:nth-child(2) > div > section > div > ul > div > div:nth-child(%d) > div > a > article > div.commons_thumbnail__3wYGv.CardType_thumbnail__2dtTe.commons_active__1tjD5 > span'%i).click()
        time.sleep(2)
        reallist.append(driver.current_url)
        driver.back()
except:
    pass

#오늘 새로뜬 프로젝트 url (list)     
#오늘 새로 뜬 프로젝트 csv로 추출
reallist
