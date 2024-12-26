from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .models import Car, Price
import os

def convert_to_int(value):
    # '-' 또는 빈 문자열인 경우 0을 반환
    if value == '-' or not value:
        return 0
    # 숫자 문자열에서 쉼표 제거 후 정수로 변환
    return int(value.replace(',', ''))

def search_car_by_number(car_number):
    driver = None
#     options = Options()
#     options.add_argument("--headless=new")  # 헤드리스 모드 활성화
#     options.add_argument("--window-size=1920,1080")  # 창 크기 설정
#     options.add_experimental_option("detach", True)

#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=options)

#     try:
#         url = "https://www.car365.go.kr/web/contents/usedcar_carcompare.do"
#         driver.get(url)

    # options = Options()
    # 필수적인 headless 옵션들
    # options.add_argument('--headless=new')
    # options.add_argument('--no-sandbox')  # 리눅스 환경에서 필수
    # options.add_argument('--disable-dev-shm-usage')  # 메모리 문제 방지
    # options.add_argument('--disable-gpu')  # 리눅스에서 필요
    # options.add_argument('--window-size=1920,1080')
    # options.add_argument('--disable-extensions')
    # options.add_argument('--ignore-certificate-errors')
    # options = webdriver.ChromeOptions()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')  # 필수
    chrome_options.add_argument('--disable-dev-shm-usage')  # 필수
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=1920x1080')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f'user-agent=M')
    chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')

    
    # 로깅 관련 옵션
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_experimental_option('detach', True)
    

    try:        
        driver_path=os.getenv('CHROM_DRIVER_PATH', ChromeDriverManager().install())
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver = webdriver.Chrome(excutable_path ='chromedriver',chrome_options=chrome_options)

        url = "https://www.car365.go.kr/web/contents/usedcar_carcompare.do"
        driver.get(url)

        wait = WebDriverWait(driver, 2)  # 10초로 증가

        # 명시적 대기 추가 (더 안정적)
        # wait = WebDriverWait(driver, 10)
        # search_input = wait.until(
        #     EC.presence_of_element_located((By.ID, "searchStr"))
        # )
        # search_input.send_keys(car_number)
        
        # search_button = wait.until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn_soldvehicle"))
        # )
        # search_button.click()

        # 결과 로딩 대기
        # time.sleep(2)

        
        # 차량번호 입력 및 검색
        driver.find_element(By.ID, "searchStr").send_keys(car_number)
        driver.find_element(By.CSS_SELECTOR, ".btn_soldvehicle").send_keys(Keys.ENTER)

        wait = WebDriverWait(driver, 2)


        
        # 데이터 추출 로직
        try:
            # tbody 내의 tr 요소 찾기
            rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#usedcarcompare_data tr")))
          
            print('rows',rows)

            #####
            # 여기에 데이터 없음 체크 추가
            if not rows or len(rows) == 0:
                
                return {
                    'exist': False
                }
 
            datas = [] # 저장된 데이터 관리를 위한 리스트
            
            for row in rows:
                print("outerHTML:", row.get_attribute('outerHTML'))

                # car_info = {
                #     'name': row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text,
                #     'car_type': row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text,
                #     'year': convert_to_int(row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text),
                #     'sell_count': convert_to_int(row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text),
                #     'sell_average': convert_to_int(row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text),
                #     'buy_count': convert_to_int(row.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text),
                #     'buy_average': convert_to_int(row.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text)
                # }

                car_info = {
                    'name': row.find_elements(By.TAG_NAME, "td")[0].get_attribute("textContent"),
                    'car_type': row.find_elements(By.TAG_NAME, "td")[1].get_attribute("textContent"),
                    'year': convert_to_int(row.find_elements(By.TAG_NAME, "td")[2].get_attribute("textContent")),
                    'sell_count': convert_to_int(row.find_elements(By.TAG_NAME, "td")[3].get_attribute("textContent")),
                    'sell_average': convert_to_int(row.find_elements(By.TAG_NAME, "td")[4].get_attribute("textContent")),
                    'buy_count': convert_to_int(row.find_elements(By.TAG_NAME, "td")[5].get_attribute("textContent")),
                    'buy_average': convert_to_int(row.find_elements(By.TAG_NAME, "td")[6].get_attribute("textContent"))
                }
                print('car_info',car_info)


                datas.append (car_info)
            return {
                'exist': True,
                'datas': datas
            }

        except Exception as e:
            print(f"데이터 추출 중 오류: {e}")
            return {'success': False, 'error': 'Data extraction error'}

    except Exception as e:
        print(f"검색 중 오류: {e}")
        return {'success': False, 'error': 'Search error'}

    finally:
        if driver:  # driver가 None이 아닐 때만 quit 실행
            driver.quit()