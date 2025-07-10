import cv2
import time
import base64
from dotenv import load_dotenv
from flask import Flask,request, render_template

load_dotenv()

app =Flask (__name__)

def list_camera():
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
    from openai import OpenAI
    base64_image = encode_image(image_path)
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe la imagen en detalle"},
                    {
                        "type": "image_url",
                        "image_url":{
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high"

                        }
                    }
                ]
            }
        ],
        max_tokens=300,
    )


    return response.choices[0].message.content


capture_image(0)
respuesta = analizar_foto("webcam-app/static/captured_image.jpg")
print(respuesta)