#חישוב ועדכון הממוצעים
import os
import json
import cv2
import numpy as np
import mediapipe as mp
from configuring_Mediapipe_module import detector
import ast
import facial_features_functions_to_avg
import re
with open(r"C:\Users\This User\Desktop\Final project\server\points_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
def numeric_sort_key(name):
    # מוציא את כל המספרים במחרוזת, הופך אותם למספרים
    numbers = re.findall(r'\d+', name)
    return [int(num) for num in numbers]

def Calculating_and_updating_averages():
    #פתיחת קובץ הפונקציות לקריאה
    with open("facial_features_functions_to_avg.py", "r", encoding="utf-8") as f:
        tree = ast.parse(f.read()) 
    ordered_function_names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    # סינון הפונקציות לפי שמות לתוך המערך
    functions = [getattr(facial_features_functions_to_avg, name) for name in ordered_function_names if hasattr(facial_features_functions_to_avg, name)]
    mainFolder = r"C:\Users\This User\Desktop\Final project\server\photos to project"
    all_dirs = [d for d in os.listdir(mainFolder) if os.path.isdir(os.path.join(mainFolder, d))]
    all_dirs.sort(key=numeric_sort_key)
    #יצירת מטריצה עם שמות כל התיקיות
    matFase = np.array(all_dirs).reshape(22, 2)
    for i in range(0,22):
      for j in range(0,2):
      # נתיב לתיקייה הנוכחית
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
              # זיהוי הפנים בתמונה
              detection_result = detector.detect(image)
              #זימון הפונקציה המתאימה
              b=functions[i](detection_result,image)
              if b is not None:
                  valus.append(b)
        # חישוב ממוצע עבור הפונקציה הנוכחית
        average_value = np.mean(valus)
        data[functions[i].__name__]["averages"][j] = average_value
        # עדכון הממוצע בקובץ JSON
        with open("points_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)