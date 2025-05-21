#חישוב ועדכון הממוצעים
import os
import json
import cv2
import numpy as np
import mediapipe as mp
from configuring_Mediapipe_module import detector, draw_landmarks_on_image
import ast
import facial_features_functions_to_avg
import re
with open("C:\Users\This User\Desktop\Final project\server\points_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
def numeric_sort_key(name):
    # מוציא את כל המספרים במחרוזת, הופך אותם למספרים
    numbers = re.findall(r'\d+', name)
    return [int(num) for num in numbers]
# דוגמה לחישוב ממוצע עם בדיקה
def safe_mean(arr):
    if len(arr) == 0:
        return float(0)
    else:
        return np.mean(arr)
def Calculating_and_updating_averages():
    with open("facial_features_functions_to_avg.py", "r", encoding="utf-8") as f:
        tree = ast.parse(f.read()) 
    ordered_function_names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    arrf = [getattr(facial_features_functions_to_avg, name) for name in ordered_function_names if hasattr(facial_features_functions_to_avg, name)]
    mainFolder = r"C:\Users\This User\Desktop\Final project\server\photos to project"
    all_dirs = [d for d in os.listdir(mainFolder) if os.path.isdir(os.path.join(mainFolder, d))]
    all_dirs.sort(key=numeric_sort_key)
    matFase = np.array(all_dirs).reshape(20, 2)
    for i in range(0,20):
      for j in range(0,2):
      # נתיב לתיקייה עם תמונות (יש לעדכן את הנתיב הרצוי)
        input_folder = rf"C:\Users\This User\Desktop\Final project\server\photos to project\{matFase[i][j]}"
        # מעבר על כל התמונות בתיקייה
        valus=[]
        for filename in os.listdir(input_folder):
           if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # סינון קבצים שהם תמונות
              input_path = os.path.join(input_folder, filename)
              frame = cv2.imread(input_path)
              if frame is None:
                  print(f"Error reading image: {input_path}")
                  continue  
              frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
              image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
              detection_result = detector.detect(image)
              if detection_result.face_landmarks:
                  annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
              b=arrf[i](detection_result)
              if b is not None:
                  print(b)
                  valus.append(b)
        average_value = safe_mean(valus)
        data[arrf[i].__name__]["averages"][j] = average_value
        print(average_value)
        with open("points_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)