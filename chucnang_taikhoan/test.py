import base64
import requests
import json

def image_to_base64(image_path):
    """Chuyển đổi hình ảnh PNG thành chuỗi base64."""
    with open(image_path, "rb") as image_file:
        # Đọc nội dung hình ảnh dưới dạng byte
        image_data = image_file.read()
        # Mã hóa dữ liệu hình ảnh thành base64
        base64_encoded_image = base64.b64encode(image_data).decode('utf-8')
    return base64_encoded_image

# Đường dẫn đến hình ảnh PNG
image_path = 'tmp/A_8_cropped.png'

# Chuyển đổi hình ảnh thành chuỗi base64
base64_image = image_to_base64(image_path)

# URL của API
url = "http://20.2.233.202:8081/"

# Tạo payload với chuỗi base64 của hình ảnh
payload = json.dumps({
    "apikey": "your_secret_api_key",
    "image": base64_image
})

# Đặt headers cho yêu cầu POST
headers = {
    'Content-Type': 'application/json'
}

# Gửi yêu cầu POST
response = requests.post(url, headers=headers, data=payload)

# In phản hồi từ server
print(response.text)



