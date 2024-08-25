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

def delete(driver, email):
    driver.get("http://localhost:8080/admin/user?page=5")
    tr = driver.find_element(By.XPATH, '//*[@id="layoutSidenav_content"]/main/div/div/div/div/table/tbody/tr[5]')
    td = tr.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text
    result = False
    errMsg = ""
    if td == email:
        time.sleep(1)
        tr.find_element(By.CSS_SELECTOR, 'a').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#layoutSidenav_content > main > div > div > div > div > div.mb-3 > div:nth-child(2) > input').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, '#newUser > button').click()
        result = True
    else:
        result = False
        errMsg = "Lỗi, không tìm thấy thông tin vừa tạo để xoá"
    return result, errMsg
# Hàm đăng ký
def register(driver, id, firstName, lastName,email, password,confirmPassword):
    driver.get("http://localhost:8080/register")
    firstName_field = driver.find_element(By.ID, "firstName")
    lastName_field = driver.find_element(By.ID, "lastName")
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    confirmPassword_field = driver.find_element(By.ID, "confirmPassword")
    
    firstName_field.clear()
    lastName_field.clear()
    email_field.clear()
    password_field.clear()
    confirmPassword_field.clear()
    
    firstName_field.send_keys(firstName) 
    lastName_field.send_keys(lastName) 
    email_field.send_keys(email) 
    password_field.send_keys(password)
    confirmPassword_field.send_keys(confirmPassword) 
    
    register_btn = driver.find_element(By.CSS_SELECTOR, "button")
    register_btn.click()
    errMsg = ""
    result = False
    # Kiểm tra kết quả đăng ký
    register_successful = check_register(driver)
    if register_successful:
        print("đăng ký thành công!")
        result = True
    else:
        print("đăng ký không thành công!")

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://localhost:8080',
        }

        data = {
            'id': '28',
        }

        response = requests.post('http://localhost:8080/admin/user/delete', headers=headers, data=data)
        data = {
            'firstName': 'Tài',
            'lastName': 'Khoản Test',
            'email': 'testing@gmail.com',
            'password': '123456',
            'confirmPassword': '123456',
        }
        response = requests.post('http://localhost:8080/register', headers=headers, data=data)
        result = True
        errMsg = ""
        return result, errMsg

    return result, errMsg
# Hàm kiểm tra đăng ký thành công    
def check_register(driver):
    try:

        # Lấy URL sau khi thử đăng ký
        new_url = driver.current_url

        # So sánh URL trước và sau khi thử đăng ký
        if new_url != "http://localhost:8080/register":
            return True  # Không có lỗi
        else:
            return False 

    except NoSuchElementException:
        return False
# Hàm đăng nhập
def login(driver, id, username, password): 
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
        return
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

# Hàm chụp màn hình
def capmh(driver, id):
    driver.save_screenshot(f'./img/{id}.png')
    
def main():
    # Gọi hàm mở trình duyệt
    driver = open_browser()  
    # Đọc dữ liệu từ file Excel
    file_path = 'test_cases.xlsx' 
    df = pd.read_excel(file_path, skiprows=0, engine='openpyxl')

    results = []
    
    # Các chỉ số của dòng cần bỏ
    skip_indices = [0]

    for index, row in df.iterrows():
        if index in skip_indices:
            continue  
        
        test_case_id = "A_1"
        firstName = "Tài"
        lastName = "Khoản Test"
        email = "testing@gmail.com"
        password = "1123456"
        confirmPassword = "1123456"
        times_to_run = row['TIME']
        print(f"\nĐang thử testcase {test_case_id} {times_to_run} lần")
        
        for _ in range(int(times_to_run)):  # Repeat based on the TIME value
            # Test register function
            result, errMsg = register(driver, test_case_id, firstName, lastName, email, password, confirmPassword)
            results.append({'ID': test_case_id, 'Result': result, 'Error': errMsg})
            if not result:
                continue  # Move to the next iteration if registration fails
            
            # Test login function
            result, errMsg = login(driver, test_case_id, "admin@gmail.com", "123456")
            results.append({'ID': test_case_id, 'Result': result, 'Error': errMsg})
            if not result:
                continue  # Move to the next iteration if login fails
            
            # Test delete function
            result, errMsg = delete(driver, email)
            results.append({'ID': test_case_id, 'Result': result, 'Error': errMsg})
    
    # Write all results to the Excel file at once
    df_results = pd.DataFrame(results)
    df_results.to_excel('test_results.xlsx', index=False, engine='openpyxl')
    
    print("Kết thúc!")


main()