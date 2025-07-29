import cv2
import numpy as np
import mediapipe as mp
from configuring_Mediapipe_module import detector

# מחשבת זווית בין שלוש נקודות
def calc_angle(a, b, c):
    ba = a - b
    bc = c - b
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    return np.degrees(angle)

def analyze_eyebrow_shape(image, detection_result):
    face_landmarks = detection_result.face_landmarks[0]
    np_image = image.numpy_view()
    h, w = np_image.shape[:2]

    # נקודות הגבה השמאלית
    left_eyebrow_indexes = [65, 70, 107, 55, 46, 53, 52, 105]
    eyebrow_points = np.array([
        [int(face_landmarks[i].x * w), int(face_landmarks[i].y * h)]
        for i in left_eyebrow_indexes
    ])

    # גבולות אזור הגבה
    margin = 20
    x_min, y_min = np.min(eyebrow_points, axis=0) - margin
    x_max, y_max = np.max(eyebrow_points, axis=0) + margin
    x_min, y_min = max(0, x_min), max(0, y_min)
    x_max, y_max = min(w, x_max), min(h, y_max)

    eyebrow_roi = np_image[y_min:y_max, x_min:x_max]

    # עיבוד תמונה למציאת קווי הגבה
    gray = cv2.cvtColor(eyebrow_roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("❌ לא נמצאו קונטורים בגבה")
        return
    biggest = max(contours, key=cv2.contourArea)
    points = biggest[:, 0, :]
    points = points[np.argsort(points[:, 0])]  # סידור לפי ציר X
    # הנקודה העליונה ביותר
    top_point = points[np.argmin(points[:, 1])]
    top_idx = np.where((points == top_point).all(axis=1))[0][0]
    min_dist = 15
    left_candidates = points[:top_idx]
    right_candidates = points[top_idx + 1:]
    left_filtered = left_candidates[(top_point[0] - left_candidates[:, 0]) > min_dist]
    right_filtered = right_candidates[(right_candidates[:, 0] - top_point[0]) > min_dist]
    if left_filtered.size == 0:
        left_filtered = left_candidates
    if right_filtered.size == 0:
        right_filtered = right_candidates
    if left_filtered.size == 0 or right_filtered.size == 0:
        print("❌ לא נמצאו נקודות מספיקות לקביעת זווית הגבה")
        return 0
    left = left_filtered[np.argmin(left_filtered[:, 1])]
    right = right_filtered[np.argmin(right_filtered[:, 1])]
    # התאמת הנקודות לקואורדינטות בתמונה המקורית
    left_abs = left + [x_min, y_min]
    top_abs = top_point + [x_min, y_min]
    right_abs = right + [x_min, y_min]
    angle = calc_angle(np.array(left_abs), np.array(top_abs), np.array(right_abs))
    print("זווית גבה:", angle)
    return angle  # או אפשר להחזיר מבנה נתונים מתאים לניתוח