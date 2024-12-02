import os
import pandas as pd
from .exercise_recommendation import get_exercise_recommendation
from userSimilarity.get_all_users import get_all_users
from config import set_path

#FUNCTION TO FETCH THE EXERCISE RECOMMENDATION FOR DIFFERENT CASES

target_directory = set_path()

def fetch_exercise_for_user(user_id,db):
    try:
        exercise_file = os.path.abspath(os.path.join(target_directory, f'exercise_data.json')).replace("\\","/")
        exercise_df = pd.read_json(exercise_file, orient='records', lines=True)
        ex_similarity_file = os.path.abspath(os.path.join(target_directory, f'exercise_similarity.csv')).replace("\\","/")
        ex_similarity_df = pd.read_csv(ex_similarity_file, index_col=0)

        doc_dict = fetch_user_data(db, user_id)
        if not doc_dict:
            raise ValueError(f"User with ID {user_id} does not exist.")

        favorite_exercises = doc_dict.get('favoriteExercises')
        language = doc_dict.get('language')

        exercise_recommendation = get_exercise_recommendation(user_id, favorite_exercises, ex_similarity_df, exercise_df, db, language)
        exercise_df['ID'] = exercise_df['ID'].astype(str)
        exercise_recommendation = str(exercise_recommendation)
        print(f"Exercise recommendation for user {user_id} : {exercise_recommendation}")
        exercise_description = exercise_df[exercise_df['ID'] == exercise_recommendation]['description'].iloc[0]
        #save_ex_recommendation_to_firestore(db,user_id,exercise_recommendation)
        return exercise_recommendation, exercise_description
    except Exception as e:
        print(f"An error occurred while fetching exercise recommendation for user {user_id}: {e}")
        return None, None

def fetch_user_data(db,user_id):
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    return user_doc.to_dict() if user_doc.exists else None