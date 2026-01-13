from flask import Flask, render_template, request, send_file
from PIL import Image
import numpy as np
import io
import base64

app = Flask(__name__)

def bit_level_encrypt(image, shift):
    image = image.convert("RGB")
    data = np.array(image)
    h, w, c = data.shape
    flat = data.reshape(-1, 3)

    binary = np.unpackbits(flat, axis=1)
    shifted = np.roll(binary, shift, axis=1)
    encrypted = np.packbits(shifted, axis=1).reshape(h, w, 3)
    return Image.fromarray(encrypted)

def bit_level_decrypt(image, shift):
    image = image.convert("RGB")
    data = np.array(image)
    h, w, c = data.shape
    flat = data.reshape(-1, 3)

    binary = np.unpackbits(flat, axis=1)
    shifted = np.roll(binary, -shift, axis=1)
    decrypted = np.packbits(shifted, axis=1).reshape(h, w, 3)
    return Image.fromarray(decrypted)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    shift = int(request.form['shift'])
    action = request.form['action']

    image = Image.open(file)

    if action == 'encrypt':
        result = bit_level_encrypt(image, shift)
    else:
        result = bit_level_decrypt(image, shift)

    img_io = io.BytesIO()
    result.save(img_io, 'PNG')
    img_io.seek(0)

    img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
    return {'status': 'success', 'image': img_base64, 'filename': f'{action}ed_image.png'}

if __name__ == '__main__':
    app.run(debug=True)
