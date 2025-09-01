def bmr_calculate(age, gender, current_weight, height):
    if gender == "Male":
        bmr = 66.5 + (13.75 * current_weight) + (5.003 * height) - (age * 6.755)
    else:
        bmr = 655.1 + (9.563 * current_weight) + (1.850 * height) - (age * 4.676)
    return bmr


def calories_min(bmr, activity_level):  
    if activity_level == "Sedentary":
        calories = bmr * 1.2
    elif activity_level == "Light":
        calories = bmr * 1.375
    elif activity_level == 'Moderate':
        calories = bmr * 1.55
    else:
        calories = bmr * 1.725
    return calories


def calories_deficit(calories, weekly_goal):
    calories_diff = 0
    if weekly_goal == 0.25:
        calories_diff = calories * 0.1
    elif weekly_goal == 0.5:
        calories_diff = calories * 0.21
    elif weekly_goal == 1:
        calories_diff = calories * 0.41
    return calories_diff


def calories_target(calories, calories_diff, goal_weight, current_weight):
    if goal_weight >= current_weight:
        target_calories = calories + calories_diff
    else:
        target_calories = calories - calories_diff
    return int(target_calories) 