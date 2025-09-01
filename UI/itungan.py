def bmr_calculate(weight, height, age, gender):
    if gender == "male":
        bmr = 66.5 + (13.75 * weight) + (5.003 * height) - (age * 6.755)
    else:
        bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (age * 4.676)
    return bmr

def calories_min(bmr, activity):  
    if activity == "Sedentary":
        calories = bmr * 1.2
    elif activity == "Light":
        calories = bmr * 1.375
    elif activity == 'Moderate':
        calories = bmr * 1.55
    else:
        calories = bmr * 1.725
    return calories

def calories_deficit(calories, target_gain):
    calories_diff = 0
    if target_gain == "0.25":
        calories_diff = calories * 0.1
    elif target_gain == "0.5":
        calories_diff = calories * 0.21
    elif target_gain == "1":
        calories_diff = calories * 0.41
    return calories_diff

def calories_target(calories, calories_diff, diff):
    if diff == "gain":
        calories_total_perday = calories + calories_diff
    else:
        calories_total_perday = calories - calories_diff

