# Import thư viện
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import pandas as pd
import time
import requests
from PIL import Image
import base64
import json

def open_browser():
    options = Options()
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')
    options.add_argument('--start-maximized')
    # options.add_argument('--headless=new')
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=options)
    return driver

# Hàm đăng nhập
def login(id, username, password):
    # Gọi hàm mở trình duyệt
    driver = open_browser()  
    driver.get("http://localhost:8080/login")
    username_field = driver.find_element(By.CSS_SELECTOR, "#layoutAuthentication_content > main > div > div > div > div > div.card-body > form > div:nth-child(1) > input")
    password_field = driver.find_element(By.CSS_SELECTOR, "#password")
    username_field.clear()
    password_field.clear()
    username_field.send_keys(username) 
    password_field.send_keys(password)
    login_button = driver.find_element(By.CSS_SELECTOR, "#layoutAuthentication_content > main > div > div > div > div > div.card-body > form > div.mt-4.mb-0 > div > button")
    login_button.click()
    errMsg = ""
    result = False
    # Kiểm tra kết quả đăng nhập
    login_successful = check_login(driver)
    if login_successful:
        print("Đăng nhập thành công!")
        result = True
    else:
        print("Đăng nhập không thành công!")
        try:
            new_url = driver.current_url
            if new_url != "http://localhost:8080/login?error":
                driver.save_screenshot(f'./img/{id}.png')
                # Mở ảnh toàn màn hình
                full_img = Image.open(f'./img/{id}.png')
                x1, y1 = 813, 356  # Tọa độ góc trên bên trái
                x2, y2 = 1730, 450  # Tọa độ góc dưới bên phải
                # Cắt vùng đã chọn từ ảnh
                cropped_img = full_img.crop((x1, y1, x2, y2))
                # Lưu ảnh đã cắt
                cropped_img_path = f'./img/{id}.png'
                cropped_img.save(cropped_img_path)
                errMsg = read_OCR(cropped_img_path)
            else:
                # Đợi cho phần tử chứa thông báo lỗi xuất hiện
                wait = WebDriverWait(driver, 3)  # Thay đổi thời gian chờ nếu cần
                err_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layoutAuthentication_content"]/main/div/div/div/div/div[2]/div')))
                errMsg = err_element.text   
                print("Thông báo lỗi:", errMsg)
                capmh(driver, id)
                result = False
        except:
            time.sleep(2)
            # Đợi cho phần tử chứa thông báo lỗi xuất hiện
            wait = WebDriverWait(driver, 3)  # Thay đổi thời gian chờ nếu cần
            err_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="layoutAuthentication_content"]/main/div/div/div/div/div[2]/div')))
            errMsg = err_element.text   
            print("Thông báo lỗi:", errMsg)
            capmh(driver, id)
            result = False
    # Clear cookies
    driver.delete_all_cookies()
    return result, errMsg
# Hàm kiểm tra đăng nhập thành công    
def check_login(driver):
    try:
        # URL trang login
        current_url = "http://localhost:8080/login"
        
        time.sleep(1) 

        # Lấy URL sau khi thử đăng nhập
        new_url = driver.current_url

        # So sánh URL trước và sau khi thử đăng nhập
        if new_url != "http://localhost:8080/login?error" and new_url != "http://localhost:8080/login":
            return True  # Không có lỗi
        else:
            return False 

    except NoSuchElementException:
        return False

def image_to_base64(image_path):
    """Chuyển đổi hình ảnh PNG thành chuỗi base64."""
    with open(image_path, "rb") as image_file:
        # Đọc nội dung hình ảnh dưới dạng byte
        image_data = image_file.read()
        # Mã hóa dữ liệu hình ảnh thành base64
        base64_encoded_image = base64.b64encode(image_data).decode('utf-8')
    return base64_encoded_image

def read_OCR(image_path):
    base64_image = image_to_base64(image_path)

    apiUrl = "http://127.0.0.1:8081/captcha"
    payload = json.dumps({
        "apikey": "your_secret_api_key",
        "image": base64_image
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(apiUrl, headers=headers, data=payload)
    text = response.text.encode('utf-8').decode('unicode_escape')
    if text:
        return text
    return "Lỗi"


# Hàm chụp màn hình
def capmh(driver, id):
    driver.save_screenshot(f'./img/{id}.png')
    
def main():
    # Đọc dữ liệu từ file Excel
    file_path = 'test_cases.xlsx' 
    df = pd.read_excel(file_path, skiprows=0, engine='openpyxl')

    results = []
    
    # Các chỉ số của dòng cần bỏ
    skip_indices = [0, 1, 7]

    for index, row in df.iterrows():
        if index in skip_indices:
            continue  
        
        test_case_id = row['ID']
        username = row['EMAIL']
        password = row['PASSWORD']
        
        print(f"\nĐang thử testcase {test_case_id}")
        result, errMsg = login(test_case_id, username, password)
        results.append({
            'ID': test_case_id,
            'Username': username,
            'Password': password,
            'Result': result,
            'Error': errMsg
        })
    
    df_results = pd.DataFrame(results)
    df_results.to_excel('test_results.xlsx', index=False, engine='openpyxl')
    print("Kết thúc!")


main()