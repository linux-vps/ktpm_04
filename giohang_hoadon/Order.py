from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
# Tạo đối tượng ChromeOptions
chrome_options = Options()
chrome_options.add_argument('--start-maximized')
#chrome_options.add_argument('--disable-gpu')  # Vô hiệu hóa GPU
#chrome_options.add_argument('--headless')  # Chạy trình duyệt ngầm
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

# Khởi tạo WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Điều hướng đến trang web
driver.get("http://localhost:8080/")

#Điều hướng đến trang đăng nhập
def go_to_login_page():
    try:
        # Đợi nút đăng nhập xuất hiện và nhấp vào nó
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#navbarCollapse > div.d-flex.me-0 > a"))
        ).click()
        
        # Xác nhận chuyển hướng đến trang đăng nhập
        WebDriverWait(driver, 10).until(
            EC.url_contains("/login")
        )
    except Exception as e:
        print(f"An error occurred: {e}")
# Đăng nhập vào tài khoản người dùng
def login(username, password):
    # Giả sử có form đăng nhập trên trang
    driver.find_element(By.CSS_SELECTOR, "#layoutAuthentication_content > main > div > div > div > div > div.card-body > form > div:nth-child(1) > input").send_keys(username)
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "#layoutAuthentication_content > main > div > div > div > div > div.card-body > form > div.mt-4.mb-0 > div > button").click()

#Điều hướng đến trang admin
def go_to_admin():
    try:
        # Đợi tối đa 10 giây cho liên kết "Laptop Haui" xuất hiện
        haui_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='navbar-brand ps-3' and text()='Laptop Haui']"))
        )
        
        # Nhấp vào liên kết khi đã tìm thấy
        haui_link.click()
        print("Đã nhấp vào liên kết 'Laptop Haui'.")

    except TimeoutException:
        print("Đã hết thời gian chờ. Không tìm thấy liên kết 'Laptop Haui'.")

    except NoSuchElementException:
        print("Không tìm thấy liên kết 'Laptop Haui' trên trang.")
        
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

#go_to_managerOrder
def go_to_managerOrder():
    try:
        # Đợi tối đa 10 giây cho phần tử xuất hiện
        detail_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.small.text-white.stretched-link[href='/admin/order']"))
        )
        # Nhấp vào phần tử khi đã tìm thấy
        detail_link.click()
        print("Đã nhấp vào liên kết chi tiết.")

    except TimeoutException:
        print("Đã hết thời gian chờ. Không tìm thấy phần tử 'Chi tiết'.")

    except NoSuchElementException:
        print("Không tìm thấy phần tử 'Chi tiết' trên trang.")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

#Xem đơn hàng
def view_order(order_id):
    try:
        view_button_selector = f'a.btn.btn-success[href="/admin/order/{order_id}"]'
        # Đợi tối đa 10 giây cho phần tử nút "Xem" xuất hiện
        view_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, view_button_selector))
        )
        # Nhấp vào nút "Xem" khi đã tìm thấy
        view_button.click()
        print("Đã nhấp vào nút 'Xem'.")

    except TimeoutException:
        print("Đã hết thời gian chờ. Không tìm thấy nút 'Xem'.")

    except NoSuchElementException:
        print("Không tìm thấy phần tử nút 'Xem' trên trang.")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

#Chi tiết đơn hàng
from selenium.webdriver.common.by import By

def get_order_details():
    try:
        # Lấy ID đơn hàng
        order_id = driver.find_element(By.CSS_SELECTOR, "h2").text
        print(f"{order_id}")

        products = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
        
        for product in products:
            try:
                # Lấy tên sản phẩm
                name = product.find_element(By.CSS_SELECTOR, "td a").text
                
                # Lấy giá sản phẩm
                price = product.find_element(By.CSS_SELECTOR,"td:nth-child(3)").text
                
                # Lấy số lượng sản phẩm
                quantity = product.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
                
                #Lấy thành tiền
                total_price = product.find_element(By.CSS_SELECTOR, "td:nth-child(5").text

                print(f"Sản phẩm: {name}, Giá: {price}, Số lượng: {quantity}, Thành tiền: {total_price}")
                
            except Exception as e:
                print(f"Lỗi khi lấy thông tin sản phẩm: {e}")
    
    except Exception as e:
        print(f"Đã xảy ra lỗi khi lấy thông tin đơn hàng: {e}")

#Điều hướng đến cập nhật đơn hàng
def change_order(order_id):
    try:
        update_button_selector = f'a.btn.btn-warning[href="/admin/order/update/{order_id}"]'
        # Đợi tối đa 10 giây cho phần tử nút "Xem" xuất hiện
        update_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, update_button_selector))
        )
        # Nhấp vào nút "Xem" khi đã tìm thấy
        update_button.click()
        print("Đã nhấp vào nút 'Cập nhật'.")

    except TimeoutException:
        print("Đã hết thời gian chờ. Không tìm thấy nút 'Cập nhật'.")

    except NoSuchElementException:
        print("Không tìm thấy phần tử nút 'Xem' trên trang.")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")



#Cập nhật đơn hàng
def change_order_status_and_update(status_value):
    try:
        # Tìm phần tử select theo ID
        status_select = Select(driver.find_element(By.ID, "status"))
        
        # Chọn giá trị trong thẻ select dựa trên value của option
        status_select.select_by_value(status_value)
        print(f"Đã chọn trạng thái: {status_value}")

        # Tìm và nhấp vào nút "Cập nhật"
        update_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-warning[type="submit"]')
        update_button.click()
        print("Cập nhật đơn hàng thành công")
    
    except NoSuchElementException:
        print("Không tìm thấy phần tử cần thao tác.")
    
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")


#Xóa đơn hàng
def delete_order(order_id):
    try:
        delete_button_selector = f'a.btn.btn-danger[href="/admin/order/delete/{order_id}"]'
        # Đợi tối đa 10 giây cho phần tử nút "Xóa" xuất hiện
        delete_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, delete_button_selector))
        )
        # Nhấp vào nút "Xóa" khi đã tìm thấy
        delete_button.click()
        print("Đã nhấp vào nút 'Xóa'.")

    except TimeoutException:
        print("Đã hết thời gian chờ. Không tìm thấy nút 'Xóa'.")

    except NoSuchElementException:
        print("Không tìm thấy phần tử nút 'Xóa' trên trang.")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

#Xác nhận xóa

def delete_order_with_reason(reasons):
    try:
        # Chọn lý do từ danh sách các checkbox
        for reason in reasons:
            checkbox = driver.find_element(By.XPATH, f"//label[contains(text(), '{reason}')]/preceding-sibling::input[@type='checkbox']")
            if not checkbox.is_selected():
                checkbox.click()
        print(f"Đã chọn các lý do: {', '.join(reasons)}")

        # Nhấn vào nút "Xác nhận"
        confirm_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-danger')
        confirm_button.click()
        print("Đã nhấp vào nút 'Xác nhận' để xóa đơn hàng.")
        print("Xóa đơn hàng thành công")
    
    except NoSuchElementException:
        print("Không tìm thấy phần tử cần thao tác.")
    
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

def enter_custom_reason(custom_reason):
    try:
        # Tìm và nhấp vào checkbox "Khác"
        other_reason_checkbox = driver.find_element(By.XPATH, "//label[contains(text(), 'Khác')]/preceding-sibling::input[@type='checkbox']")
        if not other_reason_checkbox.is_selected():
            other_reason_checkbox.click()

        # Điền lý do khác vào ô nhập văn bản
        text_input = driver.find_element(By.CSS_SELECTOR, 'input.ms-1[style*="border-bottom: 1px solid"]')
        text_input.clear()
        text_input.send_keys(custom_reason)
        print(f"Đã nhập lý do khác: {custom_reason}")

        # Nhấn vào nút "Xác nhận"
        confirm_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-danger')
        confirm_button.click()
        print("Đã nhấp vào nút 'Xác nhận' để xóa đơn hàng.")
    except NoSuchElementException:
        print("Không tìm thấy phần tử nhập văn bản hoặc checkbox 'Khác'.")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")


#Xuất hóa đơn

def export_invoice(data_id):
    try:
        # Tạo selector XPATH dựa trên thuộc tính data-id
        xpath_selector = f"//a[@data-id='{data_id}' and contains(@class, 'exportBill')]"
        
        # Đợi tối đa 10 giây cho nút xuất hóa đơn xuất hiện
        export_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_selector))
        )
        
        # Nhấp vào nút xuất hóa đơn khi đã tìm thấy
        export_button.click()
        print("Đã xuất hóa đơn cho đơn hàng có ID:", {data_id})

    except TimeoutException:
        print("Đã hết thời gian chờ. Không tìm thấy nút 'Xuất hóa đơn'.")

    except NoSuchElementException:
        print("Không tìm thấy phần tử nút 'Xuất hóa đơn' trên trang.")
        
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

#Thực hiện kịch bản kiểm thử
def test_cart_functionality():
    try:
        go_to_login_page()
        time.sleep(3)
        login("manager@gmail.com", "123456") 
        time.sleep(3)

        # Danh sách các test case
        test_cases = [
            "test_case_1",
            "test_case_2",
            "test_case_3",
            "test_case_4"
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            try:
                print(f"Đang kiểm thử : Testcase {i}")
                
                if test_case == "test_case_1":
                    # Testcase 1: Xem đơn hàng
                    go_to_managerOrder()
                    view_order(order_id=1)
                    time.sleep(3)
                    get_order_details()
                    time.sleep(3)
                    
                elif test_case == "test_case_2":
                    # Testcase 2: Cập nhật đơn hàng
                    go_to_admin()
                    time.sleep(3)
                    go_to_managerOrder()
                    time.sleep(3)
                    change_order(1)
                    time.sleep(3)
                    change_order_status_and_update("SHIPPING")
                    time.sleep(3)
                
                elif test_case == "test_case_3":
                    # Testcase 3: Xóa đơn hàng
                    delete_order(order_id=3)
                    reasons = ["Đã hết hàng", "Không hỗ trợ giao hàng trong khu vực"]
                    delete_order_with_reason(reasons)
                    
                elif test_case == "test_case_4":
                    # Testcase 4: Xuất hóa đơn
                    export_invoice(data_id=1)

                print(f"Testcase {i} passed.")
                print("----------------")  # In dấu gạch sau mỗi test case thành công

            except Exception as e:
                print(f"Testcase {i} thất bại: {e}")
                print("----------------")  # In dấu gạch sau mỗi test case thất bại

    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình kiểm thử: {e}")

    finally:
        # Đóng trình duyệt hoặc thực hiện các bước dọn dẹp khác nếu cần
        driver.quit()

#Thực hiện kiểm thử
test_cart_functionality()

# Đóng trình duyệt sau khi kiểm thử xong
driver.quit()