# import cv2
# import numpy as np
# import mediapipe as mp
# from configuring_Mediapipe_module import detector

# image_path = r"C:\Users\This User\Desktop\fase\34.jpeg"
# image = cv2.imread(image_path)
# if image is None:
#     raise ValueError("לא ניתן לטעון את התמונה")

# h, w = image.shape[:2]
# mp_image = mp.Image(mp.ImageFormat.SRGB, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# detection_result = detector.detect(mp_image)

# if not detection_result.face_landmarks:
#     raise ValueError("לא זוהו פנים בתמונה")

# # נקודות במצח
# face_landmarks = detection_result.face_landmarks[0]
# forehead_indices = [10, 338, 297, 332, 284, 251, 389, 356, 8, 454, 323, 361, 288, 397, 365, 379]
# forehead_points = [(int(face_landmarks[idx].x * w), int(face_landmarks[idx].y * h)) for idx in forehead_indices]
# forehead_y_top = min([pt[1] for pt in forehead_points])

# # חיתוך אזור גבוה יותר - איפה שצפוי קו שיער
# crop_top = max(0, forehead_y_top - 100)
# crop_bottom = forehead_y_top - 10
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# forehead_crop = gray[crop_top:crop_bottom, :]

# # עיבוד חכם יותר למציאת קצה: שימוש ב-threshold במקום Canny
# blurred = cv2.GaussianBlur(forehead_crop, (5, 5), 0)
# _, binary = cv2.threshold(blurred, 80, 255, cv2.THRESH_BINARY_INV)

# # חיפוש הקו התחתון בכל עמודה
# hairline_points = []
# for col in range(binary.shape[1]):
#     white_pixels = np.where(binary[:, col] > 0)[0]
#     if len(white_pixels) > 0:
#         y = white_pixels[-1] + crop_top
#         hairline_points.append((col, y))

# # ציור
# output = image.copy()
# for i in range(1, len(hairline_points)):
#     cv2.line(output, hairline_points[i - 1], hairline_points[i], (0, 255, 0), 2)

# cv2.imshow("Hairline Detection", output)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



###########################

# import cv2
# import numpy as np
# import mediapipe as mp

# # Initialize Mediapipe Face Detection
# mp_face_mesh = mp.solutions.face_mesh
# detector = mp_face_mesh.FaceMesh(static_image_mode=True)

# # Use a raw string for the image path to avoid escape sequence issues
# image_path = r"C:\Users\This User\Desktop\fase\11111111111111.jpeg"
# image = cv2.imread(image_path)

# if image is None:
#     raise ValueError("Can't Read the Image. Please check the path.")

# h, w = image.shape[:2]
# mp_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# # Process the image with Mediapipe
# detection_result = detector.process(mp_image)

# if not detection_result.multi_face_landmarks:
#     raise ValueError("No Face In the Picture")

# # Points in forehead
# face_landmarks = detection_result.multi_face_landmarks[0]
# forehead_indices = [10, 338, 297, 332, 284, 251, 389, 356, 8, 454, 323, 361, 288, 397, 365, 379]
# forehead_points = [(int(face_landmarks.landmark[idx].x * w), int(face_landmarks.landmark[idx].y * h)) for idx in forehead_indices]

# # Calculate the top of the forehead
# forehead_y_top = min([pt[1] for pt in forehead_points])

# # Define crop area for hairline detection
# crop_top = max(0, forehead_y_top - 100)
# crop_bottom = forehead_y_top - 10

# # Convert to grayscale and crop
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# forehead_crop = gray[crop_top:crop_bottom, :]

# # Edge detection using Canny
# edges = cv2.Canny(forehead_crop, 50, 150)

# # Find hairline points
# hairline_points = []
# for col in range(edges.shape[1]):
#     white_pixels = np.where(edges[:, col] > 0)[0]
#     if len(white_pixels) > 0:
#         y = white_pixels[-1] + crop_top
#         hairline_points.append((col, y))

# # Drawing the detected hairline
# output = image.copy()
# for i in range(1, len(hairline_points)):
#     cv2.line(output, hairline_points[i - 1], hairline_points[i], (0, 255, 0), 2)

# cv2.imshow("Hairline Detection", output)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



###########################


# import cv2
# import numpy as np
# import mediapipe as mp

# # הגדרת מודולי Mediapipe
# # עבור זיהוי נקודות ציון של הפנים (FaceMesh)
# mp_face_mesh = mp.solutions.face_mesh
# # עבור סגמנטציה של אובייקטים אנושיים (SelfieSegmentation)
# mp_selfie_segmentation = mp.solutions.selfie_segmentation

# def detect_hairline_and_forehead_shape(image_path):
#     """
#     מזהה את קו השיער בתמונה ומסווג את צורת המצח כמעוגלת או ריבועית.

#     :param image_path: הנתיב לקובץ התמונה.
#     :return: תמונה עם קו השיער המזוהה וסיווג צורת המצח, או None אם הזיהוי נכשל.
#     """
#     image = cv2.imread(image_path)
#     if image is None:
#         print(f"שגיאה: לא ניתן לטעון את התמונה מנתיב: {image_path}")
#         return None

#     h, w = image.shape[:2]
#     rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     output_image = image.copy()

#     # 1. זיהוי פנים ונקודות ציון עם Mediapipe FaceMesh
#     # static_image_mode=True כי אנו עובדים עם תמונה סטטית
#     # max_num_faces=1 כי אנו מצפים לפנים אחד
#     # refine_landmarks=True לדיוק רב יותר בנקודות הציון
#     # min_detection_confidence=0.5 סף ביטחון לזיהוי פנים
#     with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5) as face_mesh:
#         results_face_mesh = face_mesh.process(rgb_image)

#         if not results_face_mesh.multi_face_landmarks:
#             print("שגיאה: לא זוהו פנים בתמונה.")
#             # מציג את התמונה המקורית עם הודעת שגיאה
#             cv2.putText(output_image, "לא זוהו פנים", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
#             return output_image 

#         face_landmarks = results_face_mesh.multi_face_landmarks[0]

#         # 2. זיהוי סגמנטציה של האדם (כולל שיער) עם SelfieSegmentation
#         # model_selection=1 מספק מודל מדויק יותר עבור תמונות סטטיות
#         with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
#             results_segmentation = selfie_segmentation.process(rgb_image)
#             if results_segmentation.segmentation_mask is None:
#                 print("שגיאה: לא ניתן לבצע סגמנטציה בתמונה.")
#                 # מציג את התמונה המקורית עם הודעת שגיאה
#                 cv2.putText(output_image, "שגיאת סגמנטציה", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
#                 return output_image

#             # יצירת מסיכה בינארית של האדם
#             # סף של 0.1 הוא ערך התחלתי, ניתן לכוונן אותו בהתאם לתאורה וגווני עור/שיער
#             mask = results_segmentation.segmentation_mask > 0.1
#             binary_mask = np.zeros_like(image[:,:,0], dtype=np.uint8) # מסיכה חד ערוצית
#             binary_mask[mask] = 255 # האזורים המזוהים כלבנים (אדם/שיער)

#             # 3. מציאת קו השיער מהמסיכה והגבלתו לאזור המצח
#             # נשתמש בנקודות ציון של הפנים כדי להגדיר אזור חיפוש רלוונטי
#             # נקודות לדוגמה מ-FaceMesh להגדרת אזור המצח:
#             # 61 (רקה שמאלית), 291 (רקה ימנית) - להגדרת רוחב
#             # 10 (מרכז מצח עליון) - להגדרת גובה התחלתי לחיפוש
            
#             # קואורדינטות X של אזור החיפוש (בין הרקות)
#             min_x_forehead_region = int(face_landmarks.landmark[61].x * w)
#             max_x_forehead_region = int(face_landmarks.landmark[291].x * w)

#             # קואורדינטת Y של מרכז המצח העליון
#             top_forehead_y = int(face_landmarks.landmark[10].y * h)
            
#             # טווח חיפוש אנכי מעל המצח (לדוגמה, 100 פיקסלים מעל נקודה 10 ו-10 פיקסלים מתחתיה)
#             # זה מאפשר לחפש את קו השיער באזור סביר מעל המצח
#             search_top_y = max(0, top_forehead_y - 100) # מתחילים גבוה יותר
#             search_bottom_y = min(h, top_forehead_y + 10) # יורדים מעט מתחת לנקודה 10

#             hairline_points = []
#             for x in range(min_x_forehead_region, max_x_forehead_region + 1):
#                 # סרוק את העמודה מה-Y הנמוך ביותר (קרוב למצח) וכלפי מעלה
#                 # חפש את הפיקסל הלבן הראשון (העליון ביותר) ששייך לאדם באזור השיער.
#                 found_y = -1
#                 for y in range(search_top_y, search_bottom_y):
#                     # ודא שהקואורדינטות חוקיות בתוך גבולות התמונה
#                     if 0 <= y < h and 0 <= x < w: 
#                         if binary_mask[y, x] == 255: # אם הפיקסל לבן (שייך לאדם)
#                             found_y = y
#                             break # מצאנו את הפיקסל הלבן הראשון מלמעלה באזור החיפוש
                
#                 if found_y != -1:
#                     hairline_points.append((x, found_y))

#             # 4. החלקת קו השיער והתאמת פולינום
#             # דרושות מספיק נקודות להתאמה טובה של פולינום
#             if len(hairline_points) < 10: 
#                 print("אזהרה: לא זוהו מספיק נקודות קו שיער כדי להתאים פולינום מדויק.")
#                 cv2.putText(output_image, "לא זוהה קו שיער מדויק", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
#                 return output_image

#             x_coords = np.array([p[0] for p in hairline_points])
#             y_coords = np.array([p[1] for p in hairline_points])

#             # התאמת פולינום מדרגה 2 לקו השיער (y = ax^2 + bx + c)
#             # דרגה 2 מתאימה היטב לזיהוי קימור (מעוגל) או קו ישר יחסית (ריבועי)
#             try:
#                 # np.polyfit מחזיר את המקדמים בסדר יורד של חזקות (a, b, c)
#                 coeffs = np.polyfit(x_coords, y_coords, 2)
#                 poly_func = np.poly1d(coeffs) # יצירת אובייקט פונקציית פולינום
#             except np.linalg.LinAlgError:
#                 print("שגיאה: בעיה בהתאמת הפולינום. ייתכן שאין מספיק נקודות או שהן ליניאריות מדי.")
#                 cv2.putText(output_image, "שגיאה בהתאמת פולינום", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
#                 return output_image

#             # יצירת נקודות חדשות עבור הקו המוחלק על בסיס הפולינום
#             smooth_hairline_points = []
#             # נצייר את הקו על פני כל רוחב אזור הפנים שזוהה
#             for x in range(min_x_forehead_region, max_x_forehead_region + 1):
#                 y = int(poly_func(x))
#                 # ודא שהנקודות נשארות בתוך גבולות התמונה
#                 if 0 <= y < h:
#                     smooth_hairline_points.append((x, y))

#             # 5. ציור קו השיער המזוהה על התמונה
#             for i in range(1, len(smooth_hairline_points)):
#                 cv2.line(output_image, smooth_hairline_points[i - 1], smooth_hairline_points[i], (0, 255, 0), 2)

#             # 6. ניתוח צורת המצח (מעוגל/ריבועי)
#             # נשתמש במקדם המוביל של הפולינום (a) כדי להעריך את הקימור.
#             # עבור פולינום y = ax^2 + bx + c, המקדם a קובע את הקימור.
#             # אם a חיובי, הפרבולה פתוחה כלפי מעלה. אם y גדל כלפי מטה בתמונה,
#             # אז קו שיער מעוגל כלפי מעלה יתאים ל-a חיובי.
#             a_coeff = coeffs[0] # המקדם של x^2

#             # הגדרת סף לקימור. זהו ערך ניסיוני שיש לכוונן.
#             # ערך זה תלוי ברזולוציית התמונה ובטווח ערכי ה-Y.
#             # ערך גדול יותר של abs(a_coeff) מצביע על קימור רב יותר.
#             curvature_threshold = 0.0005 # סף לדוגמה, ייתכן שיהיה צורך לכייל

#             if abs(a_coeff) > curvature_threshold:
#                 forehead_shape = "מעוגל"
#             else:
#                 forehead_shape = "ריבועי"
            
#             # הצגת צורת המצח על התמונה
#             cv2.putText(output_image, f"צורת מצח: {forehead_shape}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
#             cv2.putText(output_image, f"מקדם קימור (a): {a_coeff:.5f}", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1, cv2.LINE_AA)

#             return output_image

# # --- דוגמה לשימוש בקוד ---
# # שנה את הנתיב לקובץ התמונה שלך
# # image_path = r"C:\Users\This User\Desktop\saved_images\captured_image_20250510_231719.png"
# # השתמש באחת מהתמונות שהעלית לדוגמה:
# image_path = r"C:\Users\This User\Desktop\fase\34.jpeg"

# detected_image = detect_hairline_and_forehead_shape(image_path)

# if detected_image is not None:
#     cv2.imshow("Hairline Detection and Forehead Shape", detected_image)
#     cv2.waitKey(0) # המתן ללחיצת מקש כלשהי
#     cv2.destroyAllWindows() # סגור את כל החלונות של OpenCV



import cv2
import numpy as np
import mediapipe as mp

# הגדרת מודולי Mediapipe
# עבור זיהוי נקודות ציון של הפנים (FaceMesh)
mp_face_mesh = mp.solutions.face_mesh
# עבור סגמנטציה של אובייקטים אנושיים (SelfieSegmentation)
mp_selfie_segmentation = mp.solutions.selfie_segmentation

def detect_hairline_and_forehead_shape(image_path):
    """
    מזהה את קו השיער בתמונה ומסווג את צורת המצח כמעוגלת או ריבועית.

    :param image_path: הנתיב לקובץ התמונה.
    :return: תמונה עם קו השיער המזוהה וסיווג צורת המצח, או None אם הזיהוי נכשל.
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"שגיאה: לא ניתן לטעון את התמונה מנתיב: {image_path}")
        return None

    h, w = image.shape[:2]
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output_image = image.copy()

    # 1. זיהוי פנים ונקודות ציון עם Mediapipe FaceMesh
    # static_image_mode=True כי אנו עובדים עם תמונה סטטית
    # max_num_faces=1 כי אנו מצפים לפנים אחד
    # refine_landmarks=True לדיוק רב יותר בנקודות הציון
    # min_detection_confidence=0.5 סף ביטחון לזיהוי פנים
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5) as face_mesh:
        results_face_mesh = face_mesh.process(rgb_image)

        if not results_face_mesh.multi_face_landmarks:
            print("שגיאה: לא זוהו פנים בתמונה.")
            # מציג את התמונה המקורית עם הודעת שגיאה
            cv2.putText(output_image, "לא זוהו פנים", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            return output_image 

        face_landmarks = results_face_mesh.multi_face_landmarks[0]

        # 2. זיהוי סגמנטציה של האדם (כולל שיער) עם SelfieSegmentation
        # model_selection=1 מספק מודל מדויק יותר עבור תמונות סטטיות
        with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
            results_segmentation = selfie_segmentation.process(rgb_image)
            if results_segmentation.segmentation_mask is None:
                print("שגיאה: לא ניתן לבצע סגמנטציה בתמונה.")
                # מציג את התמונה המקורית עם הודעת שגיאה
                cv2.putText(output_image, "שגיאת סגמנטציה", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                return output_image

            # יצירת מסיכה בינארית של האדם
            # סף של 0.1 הוא ערך התחלתי, ניתן לכוונן אותו בהתאם לתאורה וגווני עור/שיער
            mask = results_segmentation.segmentation_mask > 0.1
            binary_mask = np.zeros_like(image[:,:,0], dtype=np.uint8) # מסיכה חד ערוצית
            binary_mask[mask] = 255 # האזורים המזוהים כלבנים (אדם/שיער)

            # אופרציות מורפולוגיות לניקוי המסיכה
            # kernel בגודל קטן לטיפול ברעש קטן
            kernel = np.ones((3,3), np.uint8) 
            # סגירה (Closing): מילוי חורים קטנים וחיבור רכיבים קרובים. שימושי לשיער.
            binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
            # פתיחה (Opening): הסרת רעש קטן מחוץ לאובייקט.
            binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel, iterations=1)

            # 3. מציאת קו השיער מהמסיכה והגבלתו לאזור המצח
            # נשתמש בנקודות ציון של הפנים כדי להגדיר אזור חיפוש רלוונטי
            
            # קואורדינטות X של אזור החיפוש (בין הרקות)
            min_x_forehead_region = int(face_landmarks.landmark[61].x * w)
            max_x_forehead_region = int(face_landmarks.landmark[291].x * w)

            # קואורדינטת Y של קודקוד הראש (landmark 151)
            top_of_head_y = int(face_landmarks.landmark[151].y * h)
            # קואורדינטת Y של מרכז המצח העליון/בין הגבות (landmark 10)
            # נשתמש בנקודה זו כגבול תחתון לחיפוש קו השיער
            lower_forehead_y = int(face_landmarks.landmark[10].y * h)
            
            # טווח חיפוש אנכי: מקודקוד הראש ועד מעל הגבות
            # הוספתי מרווח קטן מעל קודקוד הראש ומעל הגבות כדי לכלול את כל אזור קו השיער הפוטנציאלי
            search_top_y = max(0, top_of_head_y - 20) 
            search_bottom_y = min(h, lower_forehead_y - 20) 

            hairline_points = []
            # ודא שאזור החיפוש חוקי
            if search_top_y >= search_bottom_y:
                print("אזהרה: אזור חיפוש קו השיער אינו חוקי או קטן מדי. ייתכן שנקודות הפנים אינן מדויקות.")
                cv2.putText(output_image, "אזור חיפוש לא חוקי", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                return output_image

            for x in range(min_x_forehead_region, max_x_forehead_region + 1):
                # סרוק את העמודה מלמטה למעלה (מ-search_bottom_y ל-search_top_y)
                # כדי למצוא את הפיקסל הלבן העליון ביותר ששייך לאדם באזור השיער.
                # זה ייתן את קו השיער התחתון באותה עמודה.
                found_y = -1
                # ודא שהלולאה רצה בכיוון הנכון (מלמטה למעלה)
                for y in range(search_bottom_y - 1, search_top_y - 1, -1): 
                    if 0 <= y < h and 0 <= x < w:
                        if binary_mask[y, x] == 255: # אם הפיקסל לבן (שייך לאדם)
                            found_y = y
                            break # מצאנו את הפיקסל הלבן התחתון ביותר באזור החיפוש (שהוא קו השיער)
                
                if found_y != -1:
                    hairline_points.append((x, found_y))

            # 4. החלקת קו השיער והתאמת פולינום
            # דרושות מספיק נקודות להתאמה טובה של פולינום
            if len(hairline_points) < 10: 
                print("אזהרה: לא זוהו מספיק נקודות קו שיער כדי להתאים פולינום מדויק.")
                cv2.putText(output_image, "לא זוהה קו שיער מדויק", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                return output_image

            x_coords = np.array([p[0] for p in hairline_points])
            y_coords = np.array([p[1] for p in hairline_points])

            # התאמת פולינום מדרגה 2 לקו השיער (y = ax^2 + bx + c)
            # דרגה 2 מתאימה היטב לזיהוי קימור (מעוגל) או קו ישר יחסית (ריבועי)
            try:
                # np.polyfit מחזיר את המקדמים בסדר יורד של חזקות (a, b, c)
                coeffs = np.polyfit(x_coords, y_coords, 2)
                poly_func = np.poly1d(coeffs) # יצירת אובייקט פונקציית פולינום
            except np.linalg.LinAlgError:
                print("שגיאה: בעיה בהתאמת הפולינום. ייתכן שאין מספיק נקודות או שהן ליניאריות מדי.")
                cv2.putText(output_image, "שגיאה בהתאמת פולינום", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                return output_image

            # יצירת נקודות חדשות עבור הקו המוחלק על בסיס הפולינום
            smooth_hairline_points = []
            # נצייר את הקו על פני כל רוחב אזור הפנים שזוהה
            for x in range(min_x_forehead_region, max_x_forehead_region + 1):
                y = int(poly_func(x))
                # ודא שהנקודות נשארות בתוך גבולות התמונה
                if 0 <= y < h:
                    smooth_hairline_points.append((x, y))

            # 5. ציור קו השיער המזוהה על התמונה
            for i in range(1, len(smooth_hairline_points)):
                cv2.line(output_image, smooth_hairline_points[i - 1], smooth_hairline_points[i], (0, 255, 0), 2)

            # 6. ניתוח צורת המצח (מעוגל/ריבועי)
            # נשתמש במקדם המוביל של הפולינום (a) כדי להעריך את הקימור.
            # עבור פולינום y = ax^2 + bx + c, המקדם a קובע את הקימור.
            # אם a חיובי, הפרבולה פתוחה כלפי מעלה. אם y גדל כלפי מטה בתמונה,
            # אז קו שיער מעוגל כלפי מעלה יתאים ל-a חיובי.
            a_coeff = coeffs[0] # המקדם של x^2

            # הגדרת סף לקימור. זהו ערך ניסיוני שיש לכוונן.
            # ערך זה תלוי ברזולוציית התמונה ובטווח ערכי ה-Y.
            # ערך גדול יותר של abs(a_coeff) מצביע על קימור רב יותר.
            curvature_threshold = 0.0005 # סף לדוגמה, ייתכן שיהיה צורך לכייל

            if abs(a_coeff) > curvature_threshold:
                forehead_shape = "מעוגל"
            else:
                forehead_shape = "ריבועי"
            
            # הצגת צורת המצח על התמונה
            cv2.putText(output_image, f"צורת מצח: {forehead_shape}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(output_image, f"מקדם קימור (a): {a_coeff:.5f}", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1, cv2.LINE_AA)

            return output_image

# --- דוגמה לשימוש בקוד ---
# שנה את הנתיב לקובץ התמונה שלך
# image_path = r"C:\Users\This User\Desktop\saved_images\captured_image_20250510_231719.png"
# השתמש באחת מהתמונות שהעלית לדוגמה:
image_path =r"C:\Users\This User\Desktop\fase\24.png"

detected_image = detect_hairline_and_forehead_shape(image_path)

if detected_image is not None:
    cv2.imshow("Hairline Detection and Forehead Shape", detected_image)
    cv2.waitKey(0) # המתן ללחיצת מקש כלשהי
    cv2.destroyAllWindows() # סגור את כל החלונות של OpenCV
