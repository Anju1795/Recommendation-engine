import numpy as np
from utils.random_output_from_a_list import random_output_from_a_list

#THE OUTPUT OF THIS FUNCTION IS A NUMBER INDICATING THE STAR RATING FOR EACH EXERCISE BY A PARTICULAR USER
def extract_satisfaction(executions):
    if isinstance(executions, dict):
        satisfaction = []
        '''Iterate through each execution to find the satisfaction. Gets a list of ratings
        of a particular exercise for different executions'''
        for date, details in executions.items():
            try:
                rating = details.get('feedback', {}).get('exerciseRating', {}).get('satisfaction')
                if rating is not None:
                    satisfaction.append(rating)
            except KeyError:
                continue
        satisfaction = normalize_satisfaction_values(satisfaction)
        return satisfaction if satisfaction else None
    else:
        return None

def extract_execution_count(executions):
    if isinstance(executions, dict):
        execution_count = 0
        #ITERATE THROUGH EACH EXECUTION TO FIND THE SATISFACTION.
        # GETS A LIST OF RATINGS OF A PARTICULAR EXERCISE FOR DIFFERENT EXECUTIONS
        for date, details in executions.items():
            try:
                execution_count += 1

            except KeyError:
                continue
        return execution_count
    else:
        return 0

#INPUT: A LIST OF RATING VALUES OF AN EXERCISE
#OUTPUT : A NUMBER INDICATING THE MEAN STAR RATING FOR THAT EXERCISE
def normalize_satisfaction_values(satisfaction):
    if satisfaction is not None:
        satisfaction = [replace_value(x) for x in satisfaction if x is not None]
        satisfaction = mean_satisfaction(satisfaction)
        return satisfaction
    else:
        return 0

#FUNCTION TO NORMALIZE THE STAR RATING VALUES TO A NUMBER
def replace_value(x):
    value_map = {
        '5 stars': 5,
        '4 stars': 4,
        '3 stars': 3,
        '2 stars': 2,
        '1 stars': 1
    }
    value = value_map.get(x, None)
    return int(value) if value is not None else None

#FUNCTION TO RETURN THE MEAN OF RATINGS FROM THE LIST
def mean_satisfaction(satisfaction):
    satisfaction = [s for s in satisfaction if s is not None]
    if satisfaction:
        return int(np.mean(satisfaction))
    return 0

#FUNCTION TO SELECT THE EXERCISES WHICH ARE RATED 4 OR 5 STARS
def select_top_rated_exercise(rating_df):
    if 'UserID' in rating_df.columns:
        for user in rating_df['UserID'].unique():
            top_rated = rating_df[((rating_df['satisfaction'] == 5) | (rating_df['satisfaction'] == 4)) & (rating_df['UserID'] == user) & (~rating_df['exerciseID'].str.startswith('10.'))]
            top_rated_ex = top_rated[['UserID','exerciseID','satisfaction','executionCount']]
            top_rated_ex = top_rated_ex.sort_values(by='executionCount',ascending=False)
            top_3_executed_ex= top_rated_ex.head(3)
            top_exercise_list = top_3_executed_ex['exerciseID'].tolist()
            random_exercise = random_output_from_a_list(top_exercise_list)
            if random_exercise is not None:
                return random_exercise