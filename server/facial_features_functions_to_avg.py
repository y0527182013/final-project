import json
with open(r"C:\Users\This User\Desktop\Final project\server\points_data.json", encoding="utf-8") as f:
    points_data = json.load(f)
def f1(detection_result):
    return (detection_result.face_landmarks[0][points_data['f1']['points'][0]].x
            - detection_result.face_landmarks[0][points_data['f1']['points'][1]].x)- ((detection_result.face_landmarks[0][points_data['f1']['points'][2]].x
                - detection_result.face_landmarks[0][points_data['f1']['points'][3]].x)
                + (detection_result.face_landmarks[0][points_data['f1']['points'][4]].x
                - detection_result.face_landmarks[0][points_data['f1']['points'][5]].x)
              ) / 2
def f2(detection_result):
    return (detection_result.face_landmarks[0][points_data['f2']['points'][0]].x
        -detection_result.face_landmarks[0][points_data['f2']['points'][1]].x)-(detection_result.face_landmarks[0][points_data['f2']['points'][2]].y-
        detection_result.face_landmarks[0][points_data['f2']['points'][3]].y)
def f3(detection_result):
    return detection_result.face_landmarks[0][points_data['f3']['points'][0]].y- detection_result.face_landmarks[0][points_data['f3']['points'][1]].y
def f4(detection_result):
    return ((1-detection_result.face_landmarks[0][points_data['f4']['points'][0]].y)-(1-detection_result.face_landmarks[0][points_data['f4']['points'][1]].y))/(detection_result.face_landmarks[0][points_data['f4']['points'][0]].x-detection_result.face_landmarks[0][points_data['f4']['points'][1]].x)
def f5(detection_result):
    return (detection_result.face_landmarks[0][points_data['f5']['points'][0]].y-detection_result.face_landmarks[0][points_data['f5']['points'][1]].y)-(detection_result.face_landmarks[0][points_data['f5']['points'][1]].y-detection_result.face_landmarks[0][points_data['f5']['points'][2]].y)
def f6(detection_result):
    return  detection_result.face_landmarks[0][points_data['f6']['points'][0]].x-detection_result.face_landmarks[0][points_data['f6']['points'][1]].x
def f7(detection_result):
    return ((1-detection_result.face_landmarks[0][points_data['f7']['points'][0]].y)-(1-detection_result.face_landmarks[0][points_data['f7']['points'][1]].y))/(detection_result.face_landmarks[0][points_data['f7']['points'][0]].x-detection_result.face_landmarks[0][points_data['f7']['points'][1]].x)
def f8(detection_result):
    return detection_result.face_landmarks[0][points_data['f8']['points'][0]].y-detection_result.face_landmarks[0][points_data['f8']['points'][1]].y
def f9(detection_result):
    # שלב 1: מחשבים את השיפוע m
    m = (detection_result.face_landmarks[0][points_data['f9']['points'][0]].y - detection_result.face_landmarks[0][
        points_data['f9']['points'][1]].y) / (detection_result.face_landmarks[0][points_data['f9']['points'][0]].x -
                                              detection_result.face_landmarks[0][points_data['f9']['points'][1]].x)
    # שלב 2: מחשבים את החיתוך עם ציר ה-Y b
    b = detection_result.face_landmarks[0][points_data['f9']['points'][0]].y - m * detection_result.face_landmarks[0][
        points_data['f9']['points'][0]].x
    # שלב 3: מחשבים את ערך ה-Y של הישר בנקודת x_point
    y_on_line = m * detection_result.face_landmarks[0][points_data['f9']['points'][2]].x + b
    return detection_result.face_landmarks[0][points_data['f9']['points'][2]].y-y_on_line
def f10(detection_result):
    return detection_result.face_landmarks[0][points_data['f10']['points'][0]].z-min(detection_result.face_landmarks[0][points_data['f10']['points'][1]].z,detection_result.face_landmarks[0][points_data['f10']['points'][2]].z)
def f11(detection_result):
    return abs(detection_result.face_landmarks[0][points_data['f11']['points'][0]].z-(detection_result.face_landmarks[0][points_data['f11']['points'][1]].z+detection_result.face_landmarks[0][points_data['f11']['points'][2]].z)/2)
def f12(detection_result):
    return detection_result.face_landmarks[0][points_data['f12']['points'][0]].y-detection_result.face_landmarks[0][points_data['f12']['points'][1]].y
def f13(detection_result):
    return (detection_result.face_landmarks[0][points_data['f13']['points'][0]].x-detection_result.face_landmarks[0][points_data['f13']['points'][1]].x)/(detection_result.face_landmarks[0][points_data['f13']['points'][2]].x-detection_result.face_landmarks[0][points_data['f13']['points'][3]].x)
def f14(detection_result):
    return abs(detection_result.face_landmarks[0][points_data['f14']['points'][0]].x - detection_result.face_landmarks[0][points_data['f14']['points'][1]].x) -abs(detection_result.face_landmarks[0][points_data['f14']['points'][2]].x - detection_result.face_landmarks[0][points_data['f14']['points'][3]].x)
def f15(detection_result):
    return detection_result.face_landmarks[0][points_data['f15']['points'][0]].y-detection_result.face_landmarks[0][points_data['f15']['points'][1]].y
def f16(detection_result):
    return detection_result.face_landmarks[0][points_data['f16']['points'][0]].z-detection_result.face_landmarks[0][points_data['f16']['points'][1]].z
def f17(detection_result):
    return detection_result.face_landmarks[0][points_data['f17']['points'][0]].z-detection_result.face_landmarks[0][points_data['f17']['points'][1]].z
# def f18(detection_result):
#          return detection_result.face_landmarks[0][points_data['f18']['points'][0]].y-detection_result.face_landmarks[0][points_data['f18']['points'][1]].z
# def f19(detection_result):
#         return detection_result.face_landmarks[0][points_data['f19']['points'][0]].x-detection_result.face_landmarks[0][points_data['f19']['points'][1]].z,
def f20(detection_result):
    return  detection_result.face_landmarks[0][points_data['f20']['points'][0]].z-detection_result.face_landmarks[0][points_data['f20']['points'][1]].z
# def f21(detection_result):
#         return detection_result.face_landmarks[0][points_data['f21']['points'][0]].y-detection_result.face_landmarks[0][points_data['f21']['points'][1]].z
# def f22(detection_result):
#         return detection_result.face_landmarks[0][points_data['f22']['points'][0]].x-detection_result.face_landmarks[0][points_data['f22']['points'][1]].z
def f23(detection_result):
    return detection_result.face_landmarks[0][points_data['f23']['points'][0]].z-detection_result.face_landmarks[0][points_data['f23']['points'][1]].z
# def f24(detection_result):
        # return detection_result.face_landmarks[0][points_data['f24']['points'][0]].y-detection_result.face_landmarks[0][points_data['f24']['points'][1]].z
def f25(detection_result):
    return detection_result.face_landmarks[0][points_data['f25']['points'][0]].z-detection_result.face_landmarks[0][points_data['f25']['points'][1]].z
