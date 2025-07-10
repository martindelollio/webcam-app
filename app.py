import cv2
import time
import base64
from dotenv import load_dotenv
from flask import Flask,request, render_template
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration


load_dotenv()

app =Flask (__name__)

def list_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_MSMF)
        if not cap.isOpened():
            break
        ret, _ = cap.read()
        if ret:
            arr.append(index)
        cap.release()
        index += 1
    return arr


def capture_image(camera_index):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_MSMF)
    time.sleep(0.5)
    if not cap.isOpened():
        print("No se pudo abirir la camara")
        return None
    
    ret, frame = cap.read()
    cap.release()
    if ret:
        
        filename = 'webcam-app/static/captured_image.jpg'
        cv2.imwrite(filename,frame)
        print(f'Imagen guardada como {filename}')
        return filename
        
    else:
        print('error al imprimir la imagen')


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")




def analizar_foto(image_path):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    return caption

@app.route('/')
def index():
    cameras = list_cameras()
    return render_template('index.html',cameras=cameras)