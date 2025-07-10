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
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    time.sleep(0.5)
    if not cap.isOpened():
        print("No se pudo abirir la camara")
        return None
    
    ret, frame = cap.read()
    cap.release()
    if ret:
        filename = 'static/captured_image.jpg'
        cv2.imwrite(filename,frame)
        return filename
        
    else:
        print('error al imprimir la imagen')

print(list_camera())
capture_image(0)