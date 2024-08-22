from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
#Go to homepage form cart page
def goto_homepage():
    try:
        # Chờ cho liên kết "Trang Chủ" xuất hiện và có thể nhấp vào
        home_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-item.nav-link"))
        )
        
        # Nhấp vào liên kết để về trang chủ
        home_link.click()
        print("Đã chuyển hướng về trang chủ.")
    
    except TimeoutException:
        print("Lỗi: Hết thời gian chờ đợi liên kết 'Trang Chủ'. Có thể liên kết không khả dụng.")
    
    except NoSuchElementException:
        print("Lỗi: Không tìm thấy liên kết 'Trang Chủ'. Có thể selector không chính xác hoặc phần tử không tồn tại.")
    
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn: {e}")
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
#Điều hướng đến trang sản phẩm
def go_to_product():
    try:
        # Nhấp vào liên kết sản phẩm
        product_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
        )
        product_link.click()
    except Exception as e:
        print(f"An error occurred: {e}")
 #Xem 1 sản phẩm       
def view_product(product_id):
    try:
        # Xây dựng selector cho liên kết sản phẩm dựa trên thuộc tính href
        link_selector = f"a[href='/product/{product_id}']"

        # Tìm liên kết sản phẩm
        product_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, link_selector))
        )

        # Cuộn đến phần tử
        driver.execute_script("arguments[0].scrollIntoView();", product_link)
        print("Đã cuộn đến liên kết sản phẩm.")

        # Đợi cho đến khi liên kết có thể nhấp và nhấp vào nó
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, link_selector))
        ).click()
        print(f"Đã nhấp vào sản phẩm với ID {product_id}.")
    
    except TimeoutException:
        print("Lỗi: Hết thời gian chờ đợi liên kết sản phẩm có thể nhấp được.")
    
    except NoSuchElementException:
        print(f"Lỗi: Không tìm thấy liên kết sản phẩm với ID {product_id}.")
    
    except ElementClickInterceptedException:
        print("Lỗi: Không thể nhấp vào liên kết sản phẩm vì bị chặn bởi một phần tử khác.")
    
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn: {e}")

#thêm sản phẩm vào giỏ hàng ở chi tiết sản phẩm
def add_product_to_cart_detail():
    # Chờ đến khi nút "Thêm vào giỏ" xuất hiện và nhấn vào nó
    try:
        # Đợi nút "Thêm vào giỏ" xuất hiện và nhấp vào nó
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btnAddToCartDetail"))
        ).click()
        
        print("Sản phẩm đã được thêm vào giỏ hàng.")
    except Exception as e:
        print(f"An error occurred: {e}")
#đóng thông báo        
def close_toast_notifications():
    try:
        # Đợi thông báo toast xuất hiện và đóng nó nếu có thể
        toast_close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".close-jq-toast-single"))
        )
        toast_close_button.click()
        print("Thông báo toast đã được đóng.")
    except Exception as e:
        print(f"Không có thông báo toast hoặc không thể đóng: {e}")
#Đến giỏ hàng
def go_to_cart():
    try:
        # Nhấp vào liên kết giỏ hàng
        cart_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/cart']"))
        )
        cart_link.click()
        print(f"Đã chuyển hướng đến giỏ hàng")
    except Exception as e:
        print(f"An error occurred: {e}")
#Điều hướng đến trang thanh toán
def go_to_payment():
    try:
        # Tìm nút xác nhận thanh toán bằng CSS Selector
        button = driver.find_element(By.CSS_SELECTOR, "button.btn.border-secondary.rounded-pill.px-4.py-3.text-primary.text-uppercase.mb-4.ms-4")
        # Nhấp vào nút
        button.click()
        print("Đã chuyển hướng đến trang thanh toán.")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi nhấp vào nút xác nhận thanh toán: {e}")
#Thanh toán
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def test_order_functionality(receiver_name, receiver_address_input, receiver_phone_input):
    try:
        # Xóa các trường thông tin
        receiver_address_field = driver.find_element(By.NAME, "receiverAddress")
        receiver_address_field.clear()

        receiver_phone_field = driver.find_element(By.NAME, "receiverPhone")
        receiver_phone_field.clear()
        
        # Điền thông tin vào các trường
        driver.find_element(By.NAME, 'receiverName').send_keys(receiver_name)
        driver.find_element(By.NAME, 'receiverAddress').send_keys(receiver_address_input)
        driver.find_element(By.NAME, 'receiverPhone').send_keys(receiver_phone_input)

        # Nhấn vào nút "Xác nhận thanh toán"
        payment_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.border-secondary.rounded-pill.px-4.py-3.text-primary.text-uppercase.mb-4.ms-4')
        payment_button.click()

        # Kiểm tra thông báo đặt hàng thành công
        try:
            # Chờ thông báo thành công
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.w-100.text-center.text-success'))
            )
            print("Thông báo đặt hàng thành công đã xuất hiện.")
            assert success_message.text == "Đặt hàng thành công"
        except NoSuchElementException:
            print("Đặt hàng không thành công: Không được để trống các tên và địa chỉ")
        
    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình kiểm thử: {e}")

def test_cart_functionality():
    try:
        go_to_login_page()
        time.sleep(3)
        login("abc@gmail.com", "123456")  # Thay thế bằng thông tin đăng nhập của bạn
        time.sleep(3)
        go_to_product()
        view_product(product_id = 1)
        add_product_to_cart_detail()
        close_toast_notifications()
        go_to_cart()
        go_to_payment()
        test_order_functionality("", "", "012321313")
    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình kiểm thử: {e}")
#Goi
test_cart_functionality()

# Đóng trình duyệt sau khi kiểm thử xong
driver.quit()