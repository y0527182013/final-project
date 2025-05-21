from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import json
import mediapipe as mp
from facial_features_functions import f1, f2, f3,f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17,f18,f19, f20,f21,f22,f23,f24,f25
from configuring_Mediapipe_module import draw_landmarks_on_image, detector
from yolo_and_taking_picture import face_reconize
from dictionary_definition import my_dict
from fastapi.middleware.cors import CORSMiddleware

# from calculating_and_updating_averages import Calculating_and_updating_averages
import json
with open(r"C:\Users\This User\Desktop\Final project\server\points_data.json", encoding="utf-8") as f:
    points_data = json.load(f)
app = FastAPI()
#זימון של הפונקציה לעדכון הממוצעים אין ענין לעשות כל פעם מחדש כרגע
# Calculating_and_updating_averages()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/validate")
async def validate(file: UploadFile = File(...)):
    arrMatchingTraits=[]
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    cv2.imwrite("received_image.jpg", image)  # לשמירת בדיקה
    arrf = [f1, f2, f3,f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17,f18,f19, f20,f21,f22,f23,f24,f25]
    if face_reconize(image):
        mp_image = mp.Image(mp.ImageFormat.SRGB, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        detection_result = detector.detect(mp_image)
        print(f"מספר נקודות בפנים הראשונה: {len(detection_result.face_landmarks[0])}")
        for func in arrf:
            arrMatchingTraits.append(func(detection_result))
        print(arrMatchingTraits)
        with open("personality_data.json", encoding="utf-8") as f:
            personality_data = json.load(f)
        a = 0b00000000
        count = 0
        i = 1
        while count < 4:
            v1=0
            v2 = 0
            if i == 8:
                break
            for j in personality_data[str(i)]["values1"]:
                v1 +=arrMatchingTraits[j-1]
            for j in personality_data[str(i)]["values2"]:
                v1 +=points_data["f"+str(j)]['averages'][1]-arrMatchingTraits[j-1]
            v1 /= personality_data[str(i)]["count"]
            for j in personality_data[str(i+1)]["values1"]:
                v2 += arrMatchingTraits[j-1]
            for j in personality_data[str(i+1)]["values2"]:
                print(points_data["f"+str(j)])
                v2 +=points_data["f"+str(j)]['averages'][1]-arrMatchingTraits[j-1]
            v2 /= personality_data[str(i+1)]["count"]
            a |= int(personality_data[str(i)]["name"], 2) if v1 > v2 else int(personality_data[str(i+1)]["name"], 2)
            print(f"i: {i}, v1: {v1}, v2: {v2}, a: {a}")
            i += 2
            count += 1
        return {"result": my_dict[a]}
    else:
        print("לא זוהו פנים")
        return JSONResponse(
            content={"valid": False, "message": "No valid face detected in the image"},
            status_code=400
        )
# אופציונלי: טיפול כללי בשגיאות שיחזיר CORS
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return PlainTextResponse(str(exc), status_code=500)