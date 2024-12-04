from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .models import Car, Price

def convert_to_int(value):
    # '-' 또는 빈 문자열인 경우 0을 반환
    if value == '-' or not value:
        return 0
    # 숫자 문자열에서 쉼표 제거 후 정수로 변환
    return int(value.replace(',', ''))

def search_car_by_number(car_number):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    try:
        url = "https://www.car365.go.kr/web/contents/usedcar_carcompare.do"
        driver.get(url)

        # 결과 로딩 대기
        time.sleep(2)
        
        # 차량번호 입력 및 검색
        driver.find_element(By.ID, "searchStr").send_keys(car_number)
        driver.find_element(By.CSS_SELECTOR, ".btn_soldvehicle").send_keys(Keys.ENTER)
        
        # 데이터 추출 로직
        try:
            # tbody 내의 tr 요소 찾기
            rows = driver.find_elements(By.CSS_SELECTOR, "#usedcarcompare_data tr")

            #####
            # 여기에 데이터 없음 체크 추가
            if not rows or len(rows) == 0:
                # 빈 데이터로 차량 정보만 저장
                car = Car.objects.create(
                    number=car_number,
                    name='미등록 차량',
                    car_type='정보없음',
                    year=0,
                    is_manual_input=True  # 수동입력 필요 표시
                )
                
                return {
                    'success': False,
                    'message': '차량 정보를 찾을 수 없습니다. 직접 입력해주세요.',
                    'car_id': car.id
                }
 
            saved_data = []  # 저장된 데이터 관리를 위한 리스트
            
            for row in rows:
                car_info = {
                    'name': row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text,
                    'car_type': row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text,
                    'year': convert_to_int(row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text),
                    'sell_count': convert_to_int(row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text),
                    'sell_average': convert_to_int(row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text),
                    'buy_count': convert_to_int(row.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text),
                    'buy_average': convert_to_int(row.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text)
                }

                try:
                    car, created = Car.objects.update_or_create(
                        number=car_number,
                        defaults={
                            'name': car_info['name'],
                            'car_type': car_info['car_type'],
                            'year': car_info['year']  # year 필드 추가
                        }
                    )

                    price = Price.objects.create(
                        car=car,
                        year=car_info['year'],
                        sell_count=car_info['sell_count'],
                        sell_average=car_info['sell_average'],
                        buy_count=car_info['buy_count'],
                        buy_average=car_info['buy_average']
                    )
                    
                    saved_data.append({
                        'car': car,
                        'price': price
                    })

                except Exception as e:
                    print(f"DB 저장 중 오류: {e}")
                    continue  # 다음 데이터 처리 진행

            return {
                'success': True,
                'message': '차량 정보가 성공적으로 저장되었습니다.',
                'data': saved_data
            }

        except Exception as e:
            print(f"데이터 추출 중 오류: {e}")
            return {'success': False, 'error': 'Data extraction error'}

    except Exception as e:
        print(f"검색 중 오류: {e}")
        return {'success': False, 'error': 'Search error'}

    finally:
        driver.quit()