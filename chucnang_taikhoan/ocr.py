from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
import pytesseract
from PIL import Image

app = Flask(__name__)
CORS(app)  # Thêm hỗ trợ CORS

API_KEY = 'your_secret_api_key'

@app.route('/captcha', methods=['POST'])
def captcha():
    data = request.get_json()

    api_key = data.get('apikey')
    if api_key != API_KEY:
        return jsonify({'error': 'Forbidden: Invalid API Key', 'message': 'Sai Apikey roi ban oi, Ib cho Minh de lay lai apikey moi nhe :)'}), 403

    base64_image = data.get('image')
    if base64_image:
        ocr_text = read_capcha_from_base64(base64_image)
        # response = {'text': ocr_text}
    else:
        ocr_text = "'error': 'Base64 image data is missing'"

    return ocr_text

def read_capcha_from_base64(base64_image):
    ocr_text = ""
    try:
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        
        ocr_text = pytesseract.image_to_string(image, lang='eng', config='--oem 3 --psm 7')

    except Exception as e:
        ocr_text = f"Error processing image: {e}"
    
    print(ocr_text)
    return ocr_text

if __name__ == "__main__":
    app.run(port=8081)
