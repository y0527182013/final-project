from GABA import analyze_eyebrow_shape
import json
import cv2
import mediapipe as mp
with open("points_data.json", encoding="utf-8") as f:
    points_data = json.load(f)
from com import compute_trait
def f1(detection_result,image_path):
    return compute_trait((detection_result.face_landmarks[0][points_data['f1']['points'][0]].x
            - detection_result.face_landmarks[0][points_data['f1']['points'][1]].x)
            - ((detection_result.face_landmarks[0][points_data['f1']['points'][2]].x
                - detection_result.face_landmarks[0][points_data['f1']['points'][3]].x)
                + (detection_result.face_landmarks[0][points_data['f1']['points'][4]].x
                - detection_result.face_landmarks[0][points_data['f1']['points'][5]].x)
              ) / 2, 'f1')
def f2(detection_result,image_path):
    return compute_trait((detection_result.face_landmarks[0][points_data['f2']['points'][0]].x
        -detection_result.face_landmarks[0][points_data['f2']['points'][1]].x)-
        (detection_result.face_landmarks[0][points_data['f2']['points'][2]].y-
        detection_result.face_landmarks[0][points_data['f2']['points'][3]].y), 'f2')
def f3(detection_result,image_path):
    return compute_trait(detection_result.face_landmarks[0][points_data['f3']['points'][0]].y
         - detection_result.face_landmarks[0][points_data['f3']['points'][1]].y, 'f3')
def f4(detection_result,image_path):
    return compute_trait(((1-detection_result.face_landmarks[0][points_data['f4']['points'][0]].y)-
                          (1-detection_result.face_landmarks[0][points_data['f4']['points'][1]].y)
                         )/(detection_result.face_landmarks[0][points_data['f4']['points'][0]].x-
                            detection_result.face_landmarks[0][points_data['f4']['points'][1]].x),'f4')
def f5(detection_result,image_path):
    return compute_trait((detection_result.face_landmarks[0][points_data['f5']['points'][0]].y-
                          detection_result.face_landmarks[0][points_data['f5']['points'][1]].y)-
                         (detection_result.face_landmarks[0][points_data['f5']['points'][1]].y-
                          detection_result.face_landmarks[0][points_data['f5']['points'][2]].y), 'f5')
def f6(detection_result,image_path):
    return compute_trait(detection_result.face_landmarks[0][points_data['f6']['points'][0]].x-
                         detection_result.face_landmarks[0][points_data['f6']['points'][1]].x,'f6')
def f7(detection_result,image_path):
    return compute_trait(((1-detection_result.face_landmarks[0][points_data['f7']['points'][0]].y)-
                          (1-detection_result.face_landmarks[0][points_data['f7']['points'][1]].y))/
                          (detection_result.face_landmarks[0][points_data['f7']['points'][0]].x-
                           detection_result.face_landmarks[0][points_data['f7']['points'][1]].x),'f7')
def f8(detection_result,image_path):
    return compute_trait(detection_result.face_landmarks[0][points_data['f8']['points'][0]].y-
                         detection_result.face_landmarks[0][points_data['f8']['points'][1]].y,'f8')
def f9(detection_result,image_path):
    #חישוב השיפוע
    m = (detection_result.face_landmarks[0][points_data['f9']['points'][0]].y - detection_result.face_landmarks[0][
        points_data['f9']['points'][1]].y) / (detection_result.face_landmarks[0][points_data['f9']['points'][0]].x -
                                              detection_result.face_landmarks[0][points_data['f9']['points'][1]].x)
    # חישוב החיתוך עם ציר ה-Y
    b = detection_result.face_landmarks[0][points_data['f9']['points'][0]].y - m * detection_result.face_landmarks[0][
        points_data['f9']['points'][0]].x
    # שלב 3: מחשבים את ערך ה-Y של הישר בנקודת x_point
    y_on_line = m * detection_result.face_landmarks[0][points_data['f9']['points'][2]].x + b
    return compute_trait(detection_result.face_landmarks[0][points_data['f9']['points'][2]].y-y_on_line,'f9')
def f10(detection_result,image_path):
    return compute_trait(detection_result.face_landmarks[0][points_data['f10']['points'][0]].z-
                         min(detection_result.face_landmarks[0][points_data['f10']['points'][1]].z,
                             detection_result.face_landmarks[0][points_data['f10']['points'][2]].z),'f10')
def f11(detection_result,image_path):
    return compute_trait(abs(detection_result.face_landmarks[0][points_data['f11']['points'][0]].z-
                             (detection_result.face_landmarks[0][points_data['f11']['points'][1]].z+
                              detection_result.face_landmarks[0][points_data['f11']['points'][2]].z)/2),'f11')
def f12(detection_result,image_path):
    return compute_trait(detection_result.face_landmarks[0][points_data['f12']['points'][0]].y-
                         detection_result.face_landmarks[0][points_data['f12']['points'][1]].y,'f12')
def f13(detection_result,image_path):
    return compute_trait((detection_result.face_landmarks[0][points_data['f13']['points'][0]].x-
                          detection_result.face_landmarks[0][points_data['f13']['points'][1]].x)
             /(detection_result.face_landmarks[0][points_data['f13']['points'][2]].x-
               detection_result.face_landmarks[0][points_data['f13']['points'][3]].x),'f13')
def f14(detection_result,image_path):
    return compute_trait(abs(detection_result.face_landmarks[0][points_data['f14']['points'][0]].x - 
                             detection_result.face_landmarks[0][points_data['f14']['points'][1]].x) 
                             -abs(detection_result.face_landmarks[0][points_data['f14']['points'][2]].x 
                            - detection_result.face_landmarks[0][points_data['f14']['points'][3]].x),'f14')
def f15(detection_result,image_path):
    return compute_trait(detection_result.face_landmarks[0][points_data['f15']['points'][0]].y
                         -detection_result.face_landmarks[0][points_data['f15']['points'][1]].y,'f15')
def f16(detection_result,image_path):
    return compute_trait(detection_result.face_landmarks[0][points_data['f16']['points'][0]].z-
                         detection_result.face_landmarks[0][points_data['f16']['points'][1]].z,'f16')
def f17(detection_result,image_path):
    return compute_trait(detection_result.face_landmarks[0][points_data['f17']['points'][0]].z-
                         detection_result.face_landmarks[0][points_data['f17']['points'][1]].z,'f17')
def f18(detection_result,image_path):
         return compute_trait(detection_result.face_landmarks[0][points_data['f18']['points'][0]].y-
                              detection_result.face_landmarks[0][points_data['f18']['points'][1]].z,'f18')
def f19(detection_result,image_path):
        return compute_trait(detection_result.face_landmarks[0][points_data['f19']['points'][0]].x-
                             detection_result.face_landmarks[0][points_data['f19']['points'][1]].z,'f19')
def f20(detection_result,image_path):
    return compute_trait(detection_result.face_landmarks[0][points_data['f20']['points'][0]].z-
                         detection_result.face_landmarks[0][points_data['f20']['points'][1]].z,'f20')
def f21(detection_result,image_path):
        image_path = mp.Image(mp.ImageFormat.SRGB, cv2.cvtColor(image_path, cv2.COLOR_BGR2RGB))
        return compute_trait(analyze_eyebrow_shape(image_path,detection_result),'f21')
def f22(detection_result,image_path):
        image_path = mp.Image(mp.ImageFormat.SRGB, cv2.cvtColor(image_path, cv2.COLOR_BGR2RGB))
        return compute_trait(analyze_eyebrow_shape(image_path,detection_result),'f22')
def f23(detection_result,image_path):
    return compute_trait(detection_result.face_landmarks[0][points_data['f23']['points'][0]].z-detection_result.face_landmarks[0][points_data['f23']['points'][1]].z,'f23')
def f24(detection_result,image_path):
        return compute_trait(detection_result.face_landmarks[0][points_data['f24']['points'][0]].y-detection_result.face_landmarks[0][points_data['f24']['points'][1]].z,'f24')
def f25(detection_result,image_path):
    return compute_trait(detection_result.face_landmarks[0][points_data['f25']['points'][0]].z-detection_result.face_landmarks[0][points_data['f25']['points'][1]].z,'f25')
