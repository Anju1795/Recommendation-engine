from datetime import datetime,timedelta
import pytz
from utils.random_output_from_a_list import random_output_from_a_list
from userData.user_recommendation_data import get_a_certain_type_of_recommendation_data
from dataObject.recommendation_type import RecommendationType


#FUNCTION TO CHECK IF THE EXERCISE IS ALREADY RECOMMENDED THIS WEEK
def check_already_recommended_exercise(db, user_id, exercise_recommendation):
    current_date = datetime.now(pytz.UTC)
    recommended_exercises = get_a_certain_type_of_recommendation_data(user_id, db, RecommendationType.EXERCISE)
    if recommended_exercises.empty:
        return False
    seven_days_ago = current_date - timedelta(days=7)
    recent_exercise_data = recommended_exercises[recommended_exercises['createdAt'] >= seven_days_ago]
    
    if exercise_recommendation in recent_exercise_data["exerciseID"].tolist():
        print(f"{exercise_recommendation} already recommended this week")
        return True
    
    return False

#FUNCTION TO CHOOSE ANOTHER EXERCISE FROM THE LIST IF ALREADY RECOMMENDED THIS WEEK
def choose_another_from_ex_list(db,user_id,exercise_recommendation,ex_list):
    if exercise_recommendation in ex_list:
        ex_list.remove(exercise_recommendation)
    ex_list = [ex for ex in ex_list if not check_already_recommended_exercise(db, user_id, ex)]

    return random_output_from_a_list(ex_list) if ex_list else None

