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


# import cv2
# import numpy as np
# import mediapipe as mp
# from configuring_Mediapipe_module import detector
# # מחשבת זווית בין שלוש נקודות
# def calc_angle(a, b, c):
#     ba = a - b
#     bc = c - b
#     cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
#     angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
#     return np.degrees(angle)
# def analyze_eyebrow_shape(image, detection_result):
#     face_landmarks = detection_result.face_landmarks[0]
#     h, w = image.shape[:2]
#     left_eyebrow_indexes = [65, 70, 107, 55, 46, 53, 52, 105]
#     eyebrow_points = np.array([
#         [int(face_landmarks[i].x * w), int(face_landmarks[i].y * h)]for i in left_eyebrow_indexes])
#     margin = 20
#     x_min, y_min = np.min(eyebrow_points, axis=0) - margin
#     x_max, y_max = np.max(eyebrow_points, axis=0) + margin
#     x_min, y_min = max(0, x_min), max(0, y_min)
#     x_max, y_max = min(w, x_max), min(h, y_max)
#     eyebrow_roi = image[y_min:y_max, x_min:x_max]
#     # עיבוד תמונה למציאת קונטור הגבה
#     gray = cv2.cvtColor(eyebrow_roi, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     biggest = max(contours, key=cv2.contourArea)
#     points = biggest[:, 0, :]
#     points = points[np.argsort(points[:, 0])]
#     top_point = points[np.argmin(points[:, 1])]
#     top_idx = np.where((points == top_point).all(axis=1))[0][0]
#     min_dist = 15
#     left_candidates = points[:top_idx]
#     right_candidates = points[top_idx + 1:]
#     left_filtered = left_candidates[(top_point[0] - left_candidates[:, 0]) > min_dist]
#     right_filtered = right_candidates[(right_candidates[:, 0] - top_point[0]) > min_dist]
#     if len(left_filtered) == 0:
#         left_filtered = left_candidates
#     if len(right_filtered) == 0:
#         right_filtered = right_candidates
#     left = left_filtered[np.argmin(left_filtered[:, 1])]
#     right = right_filtered[np.argmin(right_filtered[:, 1])]
#     left_abs = left + [x_min, y_min]
#     top_abs = top_point + [x_min, y_min]
#     right_abs = right + [x_min, y_min]
#     angle = calc_angle(np.array(left_abs), np.array(top_abs), np.array(right_abs))
#        # גבולות אזור הגבה

#        # if len(left_filtered) == 0 or len(right_filtered) == 0:
#     #     print("לא נמצאו נקודות מספיקות לקביעת זווית")
#     #     return
#     print(angle)



# # קריאה לקובץ תמונה כמו שצריך
# image_path = r"C:\Users\This User\Desktop\fase\matt-sings-T97ZXyhCok8-unsplash.jpg"
# image = cv2.imread(image_path)
# if image is None:
#     print("שגיאה: לא ניתן לטעון את התמונה")
# else:
#     mp_image = mp.Image(mp.ImageFormat.SRGB, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#     detection_result = detector.detect(mp_image)
#     analyze_eyebrow_shape(image, detection_result)




# # # מסווגת את הזווית לסוג גבה
# # def classify_eyebrow_angle(angle):
# #     if angle < 140:
# #         return "זוויתית"
# #     elif angle < 160:
# #         return "משולבת"
# #     else:
# #         return "מעוגלת"
# # #הקטנת איכות התמונה כדי להתאים למסך
# # def resize_to_fit_screen(img, max_width=800):
# #     h, w = img.shape[:2]
# #     if w > max_width:
# #         scale = max_width / w
# #         img = cv2.resize(img, (int(w * scale), int(h * scale)))
# #     return img

# # # ניתוח צורת גבה
# # def analyze_eyebrow_shape(image_path):
# #     image = cv2.imread(image_path)
# #     if image is None:
# #         print("לא הצליח לקרוא את התמונה")
# #         return

# #     h, w = image.shape[:2]
# #     mp_face_mesh = mp.solutions.face_mesh

# #     with mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True) as face_mesh:
# #         rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# #         results = face_mesh.process(rgb)

# #         if not results.multi_face_landmarks:
# #             print("לא זוהו פנים")
# #             return

# #         face_landmarks = results.multi_face_landmarks[0]
# #         left_eyebrow_indexes = [65, 70, 107, 55, 46, 53, 52, 105]
# #         eyebrow_points = np.array([
# #             [int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)]
# #             for i in left_eyebrow_indexes
# #         ])

# #         # גבולות אזור הגבה
# #         margin = 20
# #         x_min, y_min = np.min(eyebrow_points, axis=0) - margin
# #         x_max, y_max = np.max(eyebrow_points, axis=0) + margin
# #         x_min, y_min = max(0, x_min), max(0, y_min)
# #         x_max, y_max = min(w, x_max), min(h, y_max)

# #         eyebrow_roi = image[y_min:y_max, x_min:x_max]

# #         # הצגת אזור הגבה
# #         cv2.imshow("Left Eyebrow ROI", eyebrow_roi)
# #         cv2.waitKey(0)
# #         cv2.destroyAllWindows()

# #         # עיבוד תמונה למציאת קונטור הגבה
# #         gray = cv2.cvtColor(eyebrow_roi, cv2.COLOR_BGR2GRAY)
# #         blur = cv2.GaussianBlur(gray, (5, 5), 0)
# #         _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# #         contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# #         if not contours:
# #             print("לא נמצאה גבה בקונטור")
# #             return

# #         biggest = max(contours, key=cv2.contourArea)
# #         points = biggest[:, 0, :]
# #         points = points[np.argsort(points[:, 0])]

# #         for pt in points:
# #             abs_pt = pt + [x_min, y_min]  # להתאים לקואורדינטות המקוריות
# #             cv2.circle(image, tuple(abs_pt), 2, (0, 255, 255), -1)  # צהוב בהיר

# #         # נקודת השיא העליונה
# #         top_point = points[np.argmin(points[:, 1])]
# #         top_idx = np.where((points == top_point).all(axis=1))[0][0]

# #         # בחירת נקודות קצה (שמאל וימין)
# #         min_dist = 15
# #         left_candidates = points[:top_idx]
# #         right_candidates = points[top_idx + 1:]

# #         left_filtered = left_candidates[(top_point[0] - left_candidates[:, 0]) > min_dist]
# #         right_filtered = right_candidates[(right_candidates[:, 0] - top_point[0]) > min_dist]

# #         if len(left_filtered) == 0:
# #             left_filtered = left_candidates
# #         if len(right_filtered) == 0:
# #             right_filtered = right_candidates

# #         if len(left_filtered) == 0 or len(right_filtered) == 0:
# #             print("לא נמצאו נקודות מספיקות לקביעת זווית")
# #             return

# #         left = left_filtered[np.argmin(left_filtered[:, 1])]
# #         right = right_filtered[np.argmin(right_filtered[:, 1])]

# #         # התאמה לקואורדינטות מקור
# #         left_abs = left + [x_min, y_min]
# #         top_abs = top_point + [x_min, y_min]
# #         right_abs = right + [x_min, y_min]

# #         # ציור נקודות
# #         eyebrow_display = eyebrow_roi.copy()
# #         shifted_points = points - np.array([x_min, y_min])
# #         shifted_top = top_point - np.array([x_min, y_min])
# #         shifted_left = left - np.array([x_min, y_min])
# #         shifted_right = right - np.array([x_min, y_min])

# #         for pt in shifted_points:
# #             cv2.circle(eyebrow_display, tuple(pt.astype(int)), 2, (0, 255, 0), -1)
# #         cv2.circle(eyebrow_display, tuple(shifted_top.astype(int)), 4, (0, 0, 255), -1)
# #         cv2.circle(eyebrow_display, tuple(shifted_left.astype(int)), 4, (255, 0, 0), -1)
# #         cv2.circle(eyebrow_display, tuple(shifted_right.astype(int)), 4, (255, 0, 0), -1)

# #         cv2.imshow("Eyebrow with points", eyebrow_display)
# #         cv2.waitKey(0)
# #         cv2.destroyAllWindows()

# #         # חישוב וסיווג
# #         angle = calc_angle(np.array(left_abs), np.array(top_abs), np.array(right_abs))
# #         category = classify_eyebrow_angle(angle)

# #         # ציור על התמונה המקורית
# #         for pt in [left_abs, top_abs, right_abs]:
# #             cv2.circle(image, tuple(pt), 6, (0, 255, 0), -1)

# #         cv2.putText(image, f"{category} ({angle:.1f})", (30, 50),
# #                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# #         cv2.imshow("Eyebrow Analysis", resize_to_fit_screen(image))
# #         cv2.waitKey(0)
# #         cv2.destroyAllWindows()

# #         print(f"צורת הגבה: {category}, זווית: {angle:.1f} מעלות")

# # # שימוש:
