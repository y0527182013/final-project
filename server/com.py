import json
with open(r"C:\Users\This User\Desktop\Final project\server\points_data.json", encoding="utf-8") as f:
    points_data = json.load(f)
# def compute_trait(val, trait_key):
#     print("ערך:", val, "מפונקציה:", trait_key)
#     if val is None:
#         return 0
#     avg_min, avg_max = points_data[trait_key]['averages']
#     denominator = (abs(avg_max) - abs(avg_min))
#     if denominator == 0:
#         return 0  # או ערך ברירת מחדל אחר שיתאים לך
#     # אם מחוץ לטווח – החזר את הערך הקרוב יותר
#     normalized_val = (val - avg_min) / (avg_max - avg_min)
#     return normalized_val if avg_min < val < avg_max else (val-avg_min)/ (abs(avg_max-avg_min))

# def compute_trait(val, trait_key):
#     if val is None:
#         return 0
#     # שליפת המוצאים לפי הגדרות – התאמה וחוסר התאמה
#     mismatch, match = points_data[trait_key]['averages']  # mismatch = חוסר התאמה, match = התאמה
#     print("ערך:", val, "מפונקציה:", trait_key, "חוסר התאמה:", mismatch, "התאמה:", match)
#     # אם מחוץ לטווח – החזר את הערך הקרוב יותר
#     # אם אין טווח – להחזיר 1 או 0 בהתאם למשמעות
#     if match == mismatch:
#         return 0
#     # נרמול – כמה קרוב לערך של התאמה (match)
#     percent = (val - mismatch) / (match - mismatch)
#     return max(0.0, min(percent, 1.0))  # לוודא שזה בין 0 ל-1

def compute_trait(value,trait_key):
    # מרחקים לשני הממוצעים
    average_non_trait,average_trait = points_data[trait_key]['averages']
    dist_trait = abs(value - average_trait)
    dist_non_trait = abs(value - average_non_trait)
    total = dist_trait + dist_non_trait
    if total == 0:
        return 0.5  # אם בדיוק באמצע — ניקוד בינוני
    score = dist_non_trait / total
    print("ערך:", value, "חוסר התאמה:", average_non_trait, "התאמה:", average_trait, "ניקוד:", score)

    return score  # מספר בין 0 ל־1