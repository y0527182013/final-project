import json
with open(r"C:\Users\This User\Desktop\Final project\server\points_data.json", encoding="utf-8") as f:
    points_data = json.load(f)
def compute_trait(val, trait_key):
    avg_min, avg_max = points_data[trait_key]['averages']
    denominator = abs(avg_max - avg_min)
    if denominator == 0:
        return 0  # או ערך ברירת מחדל אחר שיתאים לך
    # אם מחוץ לטווח – החזר את הערך הקרוב יותר
    normalized_val = (val - avg_min) / (avg_max - avg_min)
    return normalized_val if avg_min < abs(val) < avg_max else int((val-avg_min)) / (abs(avg_max-avg_min))