import pandas as pd
from .extract_satisfaction import extract_satisfaction,extract_execution_count

def fetch_user_exercise_rating(db,user):
    user_data = []
    exercise_ref = db.collection('users').document(user).collection('exerciseResults')
    exercise_docs = exercise_ref.stream()
    for exercise in exercise_docs:
        doc_dict = exercise.to_dict()
        if 'executions' in doc_dict and doc_dict['executions'] is not None:
            exercise_fields = {
                'UserID': user,
                'exerciseID': doc_dict.get('exerciseId'),
                'executions': doc_dict.get('executions')
            }
        else:
            exercise_fields = {
                'UserID': user,
                'exerciseID': doc_dict.get('exerciseId'),
                'executions': None  # or any default value you prefer
            }
        user_data.append(exercise_fields)

    user_exercise_rating_df = pd.DataFrame(user_data)
    '''call function to get the satisfaction field of each exercise'''
    if 'executions' in user_exercise_rating_df.columns:
        user_exercise_rating_df['satisfaction'] = user_exercise_rating_df['executions'].apply(extract_satisfaction)
        user_exercise_rating_df['executionCount'] = user_exercise_rating_df['executions'].apply(extract_execution_count)
        user_exercise_rating_df = user_exercise_rating_df[['UserID','exerciseID','satisfaction','executionCount']]
        user_exercise_rating_df = user_exercise_rating_df.dropna(subset='satisfaction')
    return user_exercise_rating_df
