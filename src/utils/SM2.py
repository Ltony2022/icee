import math

def SM2_validate_EF(easiness_factor:int):
    return max(easiness_factor,1.3)

def SM2_eval(user_grade:int, easiness_factor:int):
    return SM2_validate_EF(easiness_factor + (0.1-(5-user_grade)*(0.08+(5-user_grade)*0.02)))

def SM2(user_grade:int, repetition_number:int, easiness_factor:int, interval=0): # interval being optional
    if user_grade >= 3:
        if repetition_number in [0,1]:
            interval = [1,6][repetition_number]
        else:
            interval = round(interval * easiness_factor)
        repetition_number +=1
        return (repetition_number,SM2_eval(user_grade,easiness_factor),interval) 
    else:
        return (0,SM2_eval(user_grade,easiness_factor),1)


