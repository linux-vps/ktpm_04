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

# Hàm đăng ký
def register(id, firstName, lastName,email, password,confirmPassword):
    # Gọi hàm mở trình duyệt
    driver = open_browser()  
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
        try:
            firstNameErrors = "null"
            emailErrors = "null"
            confirmPasswordErrors = "null"
            form = driver.find_element(By.ID, "registerUser")

            try:
                firstNameErrors = form.find_element(By.ID, 'firstName.errors').text
            except:
                print("")

            try:
                emailErrors = form.find_element(By.ID, 'email.errors').text
            except:
                print("")

            try:
                confirmPasswordErrors = form.find_element(By.ID, 'confirmPassword.errors').text
            except:
                print("")

            # Initialize errMsg as an empty string
            errMsg = ""

            if firstNameErrors != "null":
                errMsg += firstNameErrors

            if emailErrors != "null":
                if errMsg:
                    errMsg += ", "
                errMsg += emailErrors

            if confirmPasswordErrors != "null":
                if errMsg:
                    errMsg += ", "
                errMsg += confirmPasswordErrors
            capmh(driver, id)
            result = False
            print(errMsg)
        except:
            capmh(driver, id)
            errMsg = "Lỗi"
            result = False
    # Clear cookies
    driver.delete_all_cookies()
    return result, errMsg
# Hàm kiểm tra đăng ký thành công    
def check_register(driver):
    try:
        time.sleep(1) 

        # Lấy URL sau khi thử đăng ký
        new_url = driver.current_url

        # So sánh URL trước và sau khi thử đăng ký
        if new_url != "http://localhost:8080/register":
            return True  # Không có lỗi
        else:
            return False 

    except NoSuchElementException:
        return False



# Hàm chụp màn hình
def capmh(driver, id):
    driver.save_screenshot(f'./img/{id}.png')
    
def main():
    # Đọc dữ liệu từ file Excel
    file_path = 'test_cases.xlsx' 
    df = pd.read_excel(file_path, skiprows=0, engine='openpyxl')

    results = []
    
    # Các chỉ số của dòng cần bỏ
    skip_indices = [0, 4]

    for index, row in df.iterrows():
        if index in skip_indices:
            continue  
        
        test_case_id = row['ID']
        firstName = row['FIRST_NAME']
        lastName = row['NAME']
        email = row['EMAIL']
        password = row['PASSWORD']
        confirmPassword = row['RETYPE_PASSWORD']
        print(f"\nĐang thử testcase {test_case_id}")
        result, errMsg = register(id, firstName, lastName,email, password,confirmPassword)
        results.append({
            'ID': test_case_id,
            'Result': result,
            'Error': errMsg
        })
    
    df_results = pd.DataFrame(results)
    df_results.to_excel('test_results.xlsx', index=False, engine='openpyxl')
    print("Kết thúc!")


main()