from selenium import webdriver
from bs4 import BeautifulSoup
from openpyxl import load_workbook

# 로그인
driver = webdriver.Chrome('chromedriver.exe')
driver.get("크롤링할주소")
driver.find_element_by_id('아이디 적는 곳의 id').send_keys('계정 아이디')
driver.find_element_by_id('비밀번호 적는 곳의 id').send_keys('계정 비밀번호')
driver.find_element_by_xpath('//*[@id="버튼이름"]').click()
driver.implicitly_wait(10)

# 엑셀과의 연동
wb = load_workbook(filename = '파일명.확장자') # 파일 연동
sr = wb['시트이름'] # 워크시트 호출

a = 2 # 행 시작 번호
while a <=500:
    i = str(a)
    ac = sr['A'+i].value #A열 i번째 셀의 셀값으로 검색어에 해당한다
 
    # 홈페이지 접근
    driver.get("주소"+ac) #검색어를 넣었을 때의 주소문 분석이 필요하다.

    # html을 추출하여 A정보와 B정보 내용 찾기
    html = driver.page_source
    bs = BeautifulSoup(html, 'html.parser')
    res1 = bs.find_all("label", id='A정보의 id')
    res2 = bs.find_all("span", id='B정보의 id')

    #호출한 엑셀 파일에 A정보와 B정보를 각각 B열과 C열 i행에 입력
    ws1 = wb.active #현재 참조하고 있는 엑셀 파일
    for r in res1:
        ws1['B'+i] = r.text #B열 i번째 셀에 res1의 text만 추출하여 입력
    for r in res2:
        ws1['C'+i] = r.text #C열 i번째 셀에 res2의 text만 추출하여 입력
    a = a+1
wb.save('C:/크롤링.xlsx') # 엑셀 파일 저장
