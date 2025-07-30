# import tkinter as tk
import cv2
import datetime
import mediapipe as mp
import numpy as np
# from tkinter import filedialog
import sys
from ultralytics import YOLO
import os
import time
model_path = os.path.join(os.path.dirname(__file__), 'models', 'best.pt')
yolo_model = YOLO(model_path)
# פונקציה לבדוק אם YOLO זיהה פנים מתאימות
def yolo_detect_valid_face(image):
    results = yolo_model.predict(source=image, conf=0.13, save=False, verbose=False)
    if results and results[0].boxes:
        names = results[0].names
        detected_labels = set()
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            label = names[cls_id]
            detected_labels.add(label)
        print("Detected labels:", detected_labels) 
        required_labels = {"Straight face", "Looking to camera", "Closed mouth"}
        return required_labels.issubset(detected_labels)
    return False
def face_reconize(image_np):
    timestamp = int(time.time())
    image_path = f"temp/captured_image_{timestamp}.png"
    os.makedirs("temp", exist_ok=True)
    cv2.imwrite(image_path, image_np)
    print(">>>> נשמרה תמונה לבדיקה:", image_path)
    return yolo_detect_valid_face(image_path)