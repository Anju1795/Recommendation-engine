import pandas as pd
from .extract_satisfaction import select_top_rated_exercise
from .fetch_exercise_rating import fetch_user_exercise_rating
from .check_recommended_exercises import check_already_recommended_exercise,choose_another_from_ex_list
from .similar_user_exercise_suggestion import similar_user_condition
from utils.random_output_from_a_list import random_output_from_a_list


#FOR EACH USER ID , THIS FUNCTION RETURNS THE ID OF THE RECOMMENDED EXERCISE
def get_exercise_recommendation(user_id, favorite_exercise, similarity_df, exercise_df,  db,language):
    #FIRST CHECK FOR USERS FAVORITE EXERCISE
    if favorite_exercise is not None and isinstance(favorite_exercise, list):
        #FILTER FAVOURITE EXERCISE TO EXCLUDE JOURNEY EXERCISES
        favorite_exercise = [ex for ex in favorite_exercise if ex.startswith('1.')]
        randomFavoriteExercise = random_output_from_a_list(favorite_exercise)
        if randomFavoriteExercise:
            #CHOOSE A SIMILAR EXERCISE LIKE FAVORITE EXERCISE AND CHECK IF THE SIMILAR EXERCISE ALREADY RECOMMENDED IN THIS WEEK
            similar_exercise,similar_exercise_list = find_similar_exercise(randomFavoriteExercise,similarity_df)
            if similar_exercise and not check_already_recommended_exercise(db,user_id,similar_exercise):
                print("Recommending a similar exercise to the favourite exercise")
                return similar_exercise
            #CHOOSE ANOTHER EXERCISE FROM THE SIMILAR EXERCISE LIST
            similar_exercise = choose_another_from_ex_list(db,user_id,similar_exercise,similar_exercise_list)
            return similar_exercise if similar_exercise else check_rating_conditions(db, user_id, exercise_df, similarity_df)
    #RANDOMLY CHOSEN FROM FAVORITE EXERCISE IS NONE. CHECK EXERCISE RATING CONDITION
    return check_rating_conditions(db,user_id,exercise_df,similarity_df)

#FUNCTION TO RETURN TOP 7 SIMILAR EXERCISES AND ONE RANDOM FROM THE LIST
def find_similar_exercise(exercise,similarity_df):
    exercise_list = similarity_df.columns.tolist()
    if exercise in exercise_list:
        similar_exercises = similarity_df[exercise].nlargest(8).iloc[1:].index.tolist()
        similar_exercise = random_output_from_a_list(similar_exercises) if similar_exercises else None
        return similar_exercise,similar_exercises
    else:
        return None,[]

#FUNCTION TO RETURN SIMILAR EXERCISES LIKE TOP RATED(4/5 STARS) EXERCISES BY USER
def check_rating_conditions(db,user_id,exercise_df,similarity_df):
    user_exercise_rating = fetch_user_exercise_rating(db,user_id)
    if not user_exercise_rating.empty:
        #CASE:USER HAS RATED EXERCISES
        randomFavoriteExercise = select_top_rated_exercise(user_exercise_rating)
        if randomFavoriteExercise:
            print(f"Recommending a random exercise from the most used and rated : {randomFavoriteExercise}")
            #CHECK THE EXERCISE RECOMMENDATION CLICK COUNT IF EXERCISE ID STARTS WITH 3. TO 9.
            if not randomFavoriteExercise.startswith('1.'):
                similar_exercise = calculate_exercise_click_count(db,user_id,similarity_df,exercise_df)
                return similar_exercise
            #USER HAS 4/5 STAR RATED EXERCISES
            similar_exercise,similar_exercise_list = find_similar_exercise(randomFavoriteExercise,similarity_df)
            if similar_exercise and not check_already_recommended_exercise(db,user_id,similar_exercise):
                print("Recommending an exercise similar to the top rated exercise.")
                return similar_exercise
            similar_exercise = choose_another_from_ex_list(db,user_id,similar_exercise,similar_exercise_list)
            return similar_exercise if similar_exercise else similar_user_condition(user_id, exercise_df, db)
        return similar_user_condition(user_id,exercise_df,db)
    return similar_user_condition(user_id,exercise_df,db)

#CALCULATE THE EXERCISE ID WITH THE MOST CLICKS FROM THE RECOMMENDATION_MESSAGES COLLECTION
def calculate_exercise_click_count(db,user_id,similarity_df,exercise_df):
    recommendation_message_docs = db.collection('users').document(user_id).collection("recommendation_messages").stream()
    recommendation_messages = []
    for doc in recommendation_message_docs:
        doc_dict = doc.to_dict()
        #print(doc_dict)
        if(doc_dict.get('recommendationType') == 'EXERCISE'):
            data_fields ={
                'recommendationType': doc_dict.get('recommendationType'),
                'Clicked': doc_dict.get('clicked'),
                'exerciseID': doc_dict.get('exerciseID'),
                'exerciseFinished': doc_dict.get('finished')

            }
            recommendation_messages.append(data_fields)
    if not recommendation_messages:
        print("No exercise recommendation in the collection")
        return None
    recommendation_messages_df = pd.DataFrame(recommendation_messages)
    #print(recommendation_messages_df)
    exercise_df_clicked = recommendation_messages_df[recommendation_messages_df['Clicked'] == True]
    print(exercise_df_clicked)
    if exercise_df_clicked.empty:
        print("No exercise recommendations clicked")
        return None
    most_clicked_exercise = exercise_df_clicked['exerciseID'].value_counts().idxmax()
    print(most_clicked_exercise)
    #FETCH EXERCISE SIMILAR TO THE MOST CLICKED EXERCISE
    similar_exercise,similar_exercise_list = find_similar_exercise(most_clicked_exercise,similarity_df)
    if similar_exercise and not check_already_recommended_exercise(db,user_id,similar_exercise):
        print("Recommending an exercise similar to most clicked from recommendation_messages collection")
        return similar_exercise
    similar_exercise = choose_another_from_ex_list(db,user_id,similar_exercise,similar_exercise_list)
    return similar_exercise if similar_exercise else similar_user_condition(user_id, exercise_df, db)