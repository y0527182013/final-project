
import cv2
import numpy as np
import mediapipe as mp

def calc_angle(a, b, c):
    ba = a - b
    bc = c - b
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    return np.degrees(angle)

def classify_eyebrow_angle(angle):
    if angle < 140:
        return "זוויתית"
    elif angle < 160:
        return "משולבת"
    else:
        return "מעוגלת"

def analyze_eyebrow_shape(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("לא הצליח לקרוא את התמונה")
        return

    h, w = image.shape[:2]

    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True) as face_mesh:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            print("לא זוהו פנים")
            return

        face_landmarks = results.multi_face_landmarks[0]
        left_eyebrow_indexes = [65, 66, 107, 55, 52]
        eyebrow_points = np.array([
            [int(face_landmarks.landmark[i].x * w), int(face_landmarks.landmark[i].y * h)]
            for i in left_eyebrow_indexes
        ])

        # גבולות אזור הגבה
        margin = 20
        x_min, y_min = np.min(eyebrow_points, axis=0) - margin
        x_max, y_max = np.max(eyebrow_points, axis=0) + margin
        x_min, y_min = max(0, x_min), max(0, y_min)
        x_max, y_max = min(w, x_max), min(h, y_max)

        eyebrow_roi = image[y_min:y_max, x_min:x_max]
        gray = cv2.cvtColor(eyebrow_roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            print("לא נמצאה גבה בקונטור")
            return

        biggest = max(contours, key=cv2.contourArea)
        points = biggest[:, 0, :]
        points = points[np.argsort(points[:, 0])]

        # נקודה עליונה
        top_point = points[np.argmin(points[:, 1])]
        top_idx = np.where((points == top_point).all(axis=1))[0][0]

        # בחירת נקודות קצה (שמאל וימין)
        min_dist = 15
        left_candidates = points[:top_idx]
        right_candidates = points[top_idx + 1:]

        left_filtered = left_candidates[(top_point[0] - left_candidates[:, 0]) > min_dist]
        right_filtered = right_candidates[(right_candidates[:, 0] - top_point[0]) > min_dist]

        if len(left_filtered) == 0:
            left_filtered = left_candidates
        if len(right_filtered) == 0:
            right_filtered = right_candidates

        if len(left_filtered) == 0 or len(right_filtered) == 0:
            print("לא נמצאו נקודות מספיקות לקביעת זווית")
            return

        left = left_filtered[np.argmin(left_filtered[:, 1])]
        right = right_filtered[np.argmin(right_filtered[:, 1])]

        # החזרה לקואורדינטות מקור
        left_abs = left + [x_min, y_min]
        top_abs = top_point + [x_min, y_min]
        right_abs = right + [x_min, y_min]

        # חישוב וסיווג
        angle = calc_angle(np.array(left_abs), np.array(top_abs), np.array(right_abs))
        category = classify_eyebrow_angle(angle)

        # ציור
        for pt in [left_abs, top_abs, right_abs]:
            cv2.circle(image, tuple(pt), 6, (0, 255, 0), -1)

        cv2.putText(image, f"{category} ({angle:.1f})", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.imshow("Eyebrow Analysis", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(f"צורת הגבה: {category}, זווית: {angle:.1f} מעלות")

# שימוש:
analyze_eyebrow_shape(r"C:\Users\This User\Downloads\ChatGPT Image May 21, 2025, 03_32_27 AM.png")








# # #זה ממש בכיוון אבל הנקודות קצת מדי צמודות
# # import cv2
# # import numpy as np
# # import mediapipe as mp

# # def calc_angle(a, b, c):
# #     ba = a - b
# #     bc = c - b
# #     cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
# #     angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
# #     return np.degrees(angle)

# # def classify_eyebrow_angle(angle):
# #     if angle < 140:
# #         return "זוויתית"
# #     elif angle < 160:
# #         return "משולבת"
# #     else:
# #         return "מעוגלת"

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
# #         left_eyebrow_indexes = [65, 66, 107, 55, 52]
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

# #         # נקודה עליונה
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

# #         # החזרה לקואורדינטות מקור
# #         left_abs = left + [x_min, y_min]
# #         top_abs = top_point + [x_min, y_min]
# #         right_abs = right + [x_min, y_min]

# #         # חישוב וסיווג
# #         angle = calc_angle(np.array(left_abs), np.array(top_abs), np.array(right_abs))
# #         category = classify_eyebrow_angle(angle)

# #         # ציור
# #         for pt in [left_abs, top_abs, right_abs]:
# #             cv2.circle(image, tuple(pt), 6, (0, 255, 0), -1)

# #         cv2.putText(image, f"{category} ({angle:.1f})", (30, 50),
# #                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# #         cv2.imshow("Eyebrow Analysis", image)
# #         cv2.waitKey(0)
# #         cv2.destroyAllWindows()
# #         print(f"צורת הגבה: {category}, זווית: {angle:.1f} מעלות")

# # # שימוש:
# # analyze_eyebrow_shape(r"C:\Users\This User\Desktop\ChatGPT Image May 19, 2025, 02_28_11 PM.png")








