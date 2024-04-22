from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

import time

def main():
    # ChromeDriverManager를 사용하여 ChromeDriver 설정
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    # 원하는 웹사이트로 이동
    # 네이버 지도로 이동한다. 의정부시
    url = "https://m.map.kakao.com/actions/searchView?q=%EC%9D%8C%EC%8B%9D%EC%A0%90&wxEnc=MNPQLP&wyEnc=QNQPULN&lvl=7&BT=1710750754528"
    driver.get(url)
    time.sleep(3)  # 웹페이지 로딩을 기다림, 필요에 따라 시간 조절

   

    # for i in range(3, 500):  # XPath는 1부터 시작합니다.
    #     market = f'/html/body/div[3]/div/div[2]/div[1]/ul/li{[i]}/div[1]/a[1]/div/div'  # 인덱스 i를 사용하여 XPath 업데이트
                 
    #     select_market = driver.find_element(By.XPATH, market)
    #     # 이후 필요한 동작 수행, 예를 들어 클릭:
    #     select_market.click()
    #     # 필요한 경우 페이지 내 다른 요소를 확인하거나 다른 작업을 수행
    #     # 정보창을 클릭
    #    # select_info = driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div[1]/ul/li[3]/a').click
    #     # 그리고 페이지 또는 특정 상태로 돌아가기 위한 코드 추가
    #     # 예: time.sleep(2), driver.back(), 등
    #     time.sleep(2)  # 필요한 경우, 페이지가 완전히 로드될 때까지 기다림


    #search_location.send_keys(Keys.ENTER)  # 검색 실행
    time.sleep(2)  # 검색 결과 로딩 대기

    input("Press Enter to continue...")  # 사용자가 Enter 키를 누를 때까지 대기

    #정보창을 클릭

    # 두가지 정보를 가져옴

    # 작업 완료 후 드라이버 종료
    #driver.quit()

if __name__ == '__main__':
    main()