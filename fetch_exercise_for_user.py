from .exercise_recommendation import get_exercise_recommendation
from userSimilarity.get_all_users import get_all_users
from userSimilarity.calculate_user_similarity import calculate_user_similarity

#FUNCTION TO FETCH THE EXERCISE RECOMMENDATION FOR DIFFERENT CASES

def fetch_exercise_for_user(user_id,similarity_df,exercise_df,db):
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    all_users = get_all_users(db)
    # CALCULATE THE USER SIMILARITY TO CHECK FOR SIMILAR USERS
    user_similarity_df = calculate_user_similarity(all_users)
    #print("----------------User Similarity Dataframe------------------")
    #print(user_similarity_df)

    #user_data = []
    doc_dict = user_doc.to_dict()
    favorite_exercises = doc_dict.get('favoriteExercises')
    language = doc_dict.get('language')
    exercise_recommendation = get_exercise_recommendation(user_id, favorite_exercises, similarity_df, user_similarity_df, exercise_df, db, language)
    #save_ex_recommendation_to_firestore(db,user_id,exercise_recommendation)
    return exercise_recommendation

