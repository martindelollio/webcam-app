import cv2
import time
from flask import Flask, request, render_template
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from deep_translator import GoogleTranslator







app = Flask(__name__)

def list_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            break
        ret, _ = cap.read()
        if ret:
            arr.append(index)
        cap.release()
        index += 1
    return arr

def capture_image(camera_index):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    time.sleep(0.5)
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return None

    ret, frame = cap.read()
    cap.release()
    if ret:
        import os
        static_folder = os.path.join(os.path.dirname(__file__), 'static')
        filename = os.path.join(static_folder, 'captured_image.jpg')
        cv2.imwrite(filename, frame)
        print(f'Imagen guardada como {filename}')
        return filename
    else:
        print('Error al capturar la imagen')
        return None
def traducir_txt(texto):
    return GoogleTranslator(source='auto', target='es').translate(texto)


def analizar_foto(image_path):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    caption_es= traducir_txt(caption)
    return caption_es

@app.route('/')
def index():
    cameras = list_cameras()
    return render_template('index.html', cameras=cameras)

@app.route('/capture', methods=['POST'])
def capture():
    camera_index = int(request.form['camera_index'])
    image_path = capture_image(camera_index)
    if image_path:
        description = analizar_foto(image_path)
        return render_template('index.html', 
                               image_path=image_path, 
                               description=description, 
                               cameras=list_cameras())
    else:
        return render_template('index.html',
                               error="No se pudo tomar la foto",
                               cameras=list_cameras())

if __name__ == '__main__':
    app.run(debug=True)
