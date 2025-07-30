import json
with open("points_data.json", encoding="utf-8") as f:
    points_data = json.load(f)

def compute_trait(value,trait_key):
    # שליפת שני הממוצעים מהנתונים:
    # average_non_trait – הממוצע של אנשים שאין להם את התכונה.
    # average_trait – הממוצע של אנשים שיש להם את התכונה.
    average_non_trait, average_trait = points_data[trait_key]['averages']
    # חישוב מרחק מוחלט בין הערך שלנו לבין ממוצע האנשים עם התכונה.
    dist_trait = abs(value - average_trait)
    # חישוב מרחק מוחלט בין הערך שלנו לבין ממוצע האנשים בלי התכונה.
    dist_non_trait = abs(value - average_non_trait)
    # חישוב סך כל המרחקים – סכום שני המרחקים.
    total = dist_trait + dist_non_trait
    # אם הערך בדיוק באמצע בין שני הממוצעים (או שווה לשניהם), נחזיר 0.5 – ניקוד בינוני.
    if total == 0:
        return 0.5  # אם בדיוק באמצע — ניקוד בינוני
    # חישוב ניקוד התאמה לתכונה:
    # ככל שהמרחק ממוצע האנשים עם התכונה קטן יותר – הניקוד יהיה גבוה יותר.
    score = dist_trait / total
    # הדפסת הערכים לצורך בדיקה/מעקב: הערך, שני הממוצעים, והניקוד.
    print("ערך:", value, "חוסר התאמה:", average_non_trait, "התאמה:", average_trait, "ניקוד:", score)
    # החזרת הניקוד — מספר בין 0 ל־1 שמבטא מידת התאמה לתכונה.
    return score
