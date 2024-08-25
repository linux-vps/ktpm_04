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
chrome_options.add_argument('--disable-gpu')  # Vô hiệu hóa GPU
chrome_options.add_argument('--headless')  # Chạy trình duyệt ngầm
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
# Thêm sản phẩm vào giỏ hàng ở homepage
def add_product_to_cart(product_id):
    try:
        # Xây dựng selector cho nút "Thêm vào giỏ" dựa trên data-product-id
        button_selector = f"button[data-product-id='{product_id}']"

        add_to_cart_button = driver.find_element(By.CSS_SELECTOR, button_selector)

        # Cuộn đến phần tử
        driver.execute_script("arguments[0].scrollIntoView();", add_to_cart_button)
        print("Đã cuộn đến nút 'Thêm vào giỏ'.")

        # Đợi cho đến khi nút có thể nhấp và nhấp vào nó
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
        ).click()
        print("Sản phẩm đã được thêm vào giỏ hàng.")
    
    except TimeoutException:
        print("Lỗi: Hết thời gian chờ đợi nút 'Thêm vào giỏ hàng' có thể nhấp được.")
    
    except NoSuchElementException:
        print("Lỗi: Không tìm thấy nút 'Thêm vào giỏ hàng'. Có thể selector không chính xác hoặc phần tử không tồn tại.")
    
    except ElementClickInterceptedException:
        print("Lỗi: Không thể nhấp vào nút 'Thêm vào giỏ hàng' vì bị chặn bởi một phần tử khác.")
    
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn: {e}")
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
# Điều hướng đến giỏ hàng
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
# Kiểm tra chi tiết sản phẩm trong giỏ hàng
def check_cart_details():
    try:
        # Kiểm tra nếu giỏ hàng trống bằng cách tìm kiếm phần tử thông báo
        empty_cart_message = driver.find_element(By.XPATH, "//td[contains(text(),'Không có sản phẩm trong giỏ hàng')]")
        if empty_cart_message.is_displayed():
            print("Giỏ hàng trống.")
            return
    except Exception as e:
        print("Giỏ hàng không trống, kiểm tra các sản phẩm.")
        
        # Lấy tất cả các hàng trong bảng sản phẩm
        products = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
        
        for product in products:
            try:
                # Lấy tên sản phẩm
                name = product.find_element(By.CSS_SELECTOR, "td a").text
                
                # Lấy giá sản phẩm
                price = product.find_element(By.CSS_SELECTOR,"td:nth-child(3) > p").text
                
                # Lấy số lượng sản phẩm
                quantity = product.find_element(By.CSS_SELECTOR, "td input").get_attribute("value")
                
                print(f"Sản phẩm: {name}, Giá: {price}, Số lượng: {quantity}")
                
            except Exception as e:
                print(f"Lỗi khi lấy thông tin sản phẩm: {e}")
#Lấy giá trị tổng đơn hàng        
def get_cart_total_price():
    try:
        # Đợi phần tử tổng số tiền xuất hiện và lấy giá trị của nó
        total_price_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "p[data-cart-total-price]"))
        )
        total_price = total_price_element.get_attribute("data-cart-total-price")
        formatted_price = total_price_element.text.strip()  # Để lấy giá hiển thị
        
        print(f"Tổng số tiền trong giỏ hàng: {formatted_price} (Giá trị thuộc tính: {total_price})")
    except Exception as e:
        print(f"An error occurred while getting the cart total price: {e}")
#xem sản phẩm
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
#Xóa sản phẩm khỏi giỏ hàng
def remove_product():
    try:
        # Đợi nút "xóa" xuất hiện và nhấp vào nó
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-md.rounded-circle.bg-light.border.mt-4"))
        ).click()
        print("Sản phẩm đã được xóa khỏi giỏ hàng.")
    except Exception as e:
        print(f"An error occurred: {e}")
#Thay đổi số lượng sản phẩm trong giỏ hàng
def change_product_quantity(index, quantity_to_set):
    try:
        # Tìm phần tử div chứa số lượng sản phẩm và nút "+" và "-" dựa trên chỉ số
        quantity_div = driver.find_element(By.XPATH, f"//div[@class='input-group quantity mt-4'][{index + 1}]")
        
        # Tìm phần tử input chứa số lượng sản phẩm hiện tại
        quantity_input = quantity_div.find_element(By.XPATH, ".//input[@class='form-control form-control-sm text-center border-0']")
        
        # Lấy số lượng hiện tại
        current_quantity = int(quantity_input.get_attribute("value"))
        
        # Tìm nút "+" và "-" trong div đó
        minus_button = quantity_div.find_element(By.XPATH, ".//button[@class='btn btn-sm btn-minus rounded-circle bg-light border']")
        plus_button = quantity_div.find_element(By.XPATH, ".//button[@class='btn btn-sm btn-plus rounded-circle bg-light border']")
        
        # Thay đổi số lượng bằng cách nhấp vào nút "+" hoặc "-" cho đến khi đạt được số lượng mong muốn
        if quantity_to_set > current_quantity:
            for _ in range(quantity_to_set - current_quantity):
                plus_button.click()
                time.sleep(1)  # Đợi một chút giữa các lần nhấp để đảm bảo trang web cập nhật
        elif quantity_to_set < current_quantity:
            for _ in range(current_quantity - quantity_to_set):
                minus_button.click()
                time.sleep(1)  # Đợi một chút giữa các lần nhấp để đảm bảo trang web cập nhật
        print(f"Thay đổi số lượng sản phẩm thành công")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
#Chuyển hướng đến trang sản phẩm
def go_to_product():
    try:
        # Nhấp vào liên kết sản phẩm
        product_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/products']"))
        )
        product_link.click()
    except Exception as e:
        print(f"An error occurred: {e}")
#Thêm số luọng sản phẩm ở trang sản phẩm
def add_product_quantity(index, quantity_to_add):
    try:
        # Tìm phần tử div chứa số lượng sản phẩm và nút "+"
        quantity_div = driver.find_element(By.XPATH, f"//div[@class='input-group quantity mb-5'][{index + 1}]")
        
        # Tìm nút "+" bên trong div đó
        plus_button = quantity_div.find_element(By.XPATH, ".//button[@class='btn btn-sm btn-plus rounded-circle bg-light border']")
        
        # Nhấp vào nút "+" số lần tương ứng với số lượng muốn thêm
        for _ in range(quantity_to_add):
            plus_button.click()
            time.sleep(1)  # Đợi một chút giữa các lần nhấp để đảm bảo trang web cập nhật

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
#Thực hiện kịch bản kiểm thử
def test_cart_functionality():
    try:
        go_to_login_page()
        time.sleep(3)
        # Đăng nhập với thông tin tài khoản
        login("abc@gmail.com", "123456")  # Thay thế bằng thông tin đăng nhập của bạn
        time.sleep(3)

        # Danh sách các test case
        test_cases = [
            "test_case_1",
            "test_case_2",
            "test_case_3",
            "test_case_4",
            "test_case_5",
            "test_case_6"
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            try:
                print(f"Đang kiểm thử : Testcase {i}")
                
                if test_case == "test_case_1":
                    # Testcase 1: Kiểm tra giỏ hàng trống
                    go_to_cart()
                    check_cart_details()
                
                elif test_case == "test_case_2":
                    # Testcase 2: Xem chi tiết sản phẩm và thêm vào giỏ
                    go_to_product()
                    view_product(1)
                    add_product_to_cart_detail()
                    go_to_product()
                    view_product(2)
                    add_product_to_cart_detail()
                    close_toast_notifications()
                    go_to_cart()
                    check_cart_details()
                
                elif test_case == "test_case_3":
                    # Testcase 3: Kiểm tra chi tiết giỏ hàng
                    goto_homepage()
                    go_to_cart()
                    check_cart_details()
                    get_cart_total_price()

                elif test_case == "test_case_4":
                    # Testcase 4: xóa sản phẩm khỏi giỏ hàng
                    goto_homepage()
                    go_to_cart()
                    remove_product()
                    check_cart_details()
                    get_cart_total_price()

                elif test_case == "test_case_5":
                    # Testcase 5: Thay đổi số lượng sản phẩm trong giỏ hàng
                    goto_homepage()
                    go_to_cart()
                    change_product_quantity(index=0, quantity_to_set=3)
                    check_cart_details()
                    get_cart_total_price()

                elif test_case == "test_case_6":
                    # Testcase 6: Thêm 10 sản phẩm từ trang chi tiết sản phẩm
                    goto_homepage()
                    go_to_product()
                    view_product(1)
                    add_product_quantity(index=0, quantity_to_add=10)
                    add_product_to_cart_detail()
                    close_toast_notifications()
                    go_to_cart()
                    check_cart_details()
                    get_cart_total_price()

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


# Gọi hàm kiểm thử
test_cart_functionality()

# Đóng trình duyệt sau khi kiểm thử xong
driver.quit()
