from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import json
import mediapipe as mp
from configuring_Mediapipe_module import detector
from yolo_and_taking_picture import face_reconize
from dictionary_definition import my_dict
from fastapi.middleware.cors import CORSMiddleware
import facial_features_functions
from weights_dictionary import weights
import ast
from calculating_and_updating_averages import Calculating_and_updating_averages
import json
with open(r"facial_features_functions.py", "r", encoding="utf-8") as f:
    tree = ast.parse(f.read()) 
with open(r"personality_data.json", encoding="utf-8") as f:
        personality_data = json.load(f)
with open(r"points_data.json", encoding="utf-8") as f:
    points_data = json.load(f)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://localhost:3002",
    "http://127.0.0.1:3002",
    "https://lookiny.netlify.app"],
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
    ordered_function_names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    arrf = [getattr(facial_features_functions, name) for name in ordered_function_names if hasattr(facial_features_functions, name)]
    if face_reconize(image):
        mp_image = mp.Image(mp.ImageFormat.SRGB, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        detection_result = detector.detect(mp_image)
        for func in arrf:
            arrMatchingTraits.append(func(detection_result,image))
        a = 0b00000000
        count = 0
        i = 1
        print("arrMatchingTraits:", arrMatchingTraits)
        while count < 4:
            v1=0
            v2 = 0
            if i == 8:
                break
            for j in personality_data[str(i)]["values1"]:
                v1 +=arrMatchingTraits[j-1]*weights[j][i]
            for j in personality_data[str(i)]["values2"]:
                v1 +=(1-arrMatchingTraits[j-1])*weights[j][i]
            v1 /= personality_data[str(i)]["count"]
            for j in personality_data[str(i+1)]["values1"]:
                v2 += arrMatchingTraits[j-1]*weights[j][i+1]
            for j in personality_data[str(i+1)]["values2"]:
                print(points_data["f"+str(j)])
                v2 +=(1-arrMatchingTraits[j-1])*weights[j][i+1]
            v2 /= personality_data[str(i+1)]["count"]
            a |= int(personality_data[str(i)]["name"], 2) if v1 > v2 else int(personality_data[str(i+1)]["name"], 2)
            print(f"i: {i}, v1: {v1}, v2: {v2}, a: {a}")
            i += 2
            count += 1
        return {"result": my_dict[a]}
    else:
        print("לא זוהו פנים")
        return JSONResponse(
            content="התמונה שהועלתה אינה עומדת בתנאי הסף עבור האבחון",
            status_code=400
        )
# אופציונלי: טיפול כללי בשגיאות שיחזיר CORS
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return PlainTextResponse(str(exc), status_code=500)