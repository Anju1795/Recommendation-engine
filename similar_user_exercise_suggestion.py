from utils.random_output_from_a_list import random_output_from_a_list
from .fetch_exercise_rating import fetch_user_exercise_rating
from .extract_satisfaction import select_top_rated_exercise
from userSimilarity.get_similar_user_ids import get_top_similar_users_for_one_user



def similar_user_condition(user_id,exercise_df,db):
    five_similar_users = get_top_similar_users_for_one_user(user_id, db)
    if five_similar_users is not None:
        #SIMILAR USERS EXIST, LOOP THROUGH EACH
        for user in five_similar_users:
            user_data = db.collection('users').document(user).get().to_dict()
            if user_data is not None:
                fav_ex_similar_user = user_data.get('favoriteExercises')
                if fav_ex_similar_user is not None and isinstance(fav_ex_similar_user, list):
                    #SELECT FAV EXERCISE OF SIMILAR USER
                    fav_ex_similar_user = [ex for ex in fav_ex_similar_user if ex.startswith('1')]
                    randomFavoriteExercise = random_output_from_a_list(fav_ex_similar_user)
                    if randomFavoriteExercise is None:
                        #IF RANDOM FAVORITE IS NONE, CHECK IF SIMILAR USER HAS RATED ANY EXERCISE
                        ex = similar_user_rated(db,user)
                        if ex is None:
                            #IF NO RATED EXERCISE, CHECK NEXT SIMILAR USER
                            continue
                        else:
                            print("Recommending an exercise which a similar user gave high rating.")
                            return ex
                    else:
                        print("Recommending an exercise which is a similar user's favourite")
                        return randomFavoriteExercise
                else:
                    #SIMILAR USER HAS NO FAVORITE EXERCISE, CHECK FOR RATED EXERCISES
                    ex = similar_user_rated(db,user)
                    if ex is None:
                        #SIMILAR USER HAS NO EXERCISES RATED. CHECK NEXT SIMILAR USER
                        continue
                    else:
                        print("Recommending an exercise which a similar user rated high.")
                        return ex
            else:
                #SIMILAR USER DATA IS NONE. CHECK EXT USER
                continue
        #ALL SIMILAR USER DATA NONE. RETURNING RANDOM SCHWACH
        print("No similar user data exist.Recommending an exercise with tRating schwach.")
        return default_exercise_selection(exercise_df)
    else:
        #NO SIMILAR USER. RETURNING RANDOM SCHWACH
        print("No similar user data exist.Recommending an exercise with tRating schwach.")
        return default_exercise_selection(exercise_df)

def similar_user_rated(db,random_similar_user):
    similar_user_exercise_rating = fetch_user_exercise_rating(db,random_similar_user)
    if not similar_user_exercise_rating.empty:
        #SIMILAR USER HAS RATING. CHECK TOP RATED EXERCISES
        randomFavoriteExercise = select_top_rated_exercise(similar_user_exercise_rating)
        if randomFavoriteExercise is None:
            #RANDOM FROM RATED EX IS NONE. RETURNING NONE
            return None
        else:
            print("Recommending an exercise which a similar user rated high.")
            return randomFavoriteExercise
    else:
        #SIMILAR USER HAS NOT RATED EX. RETURNING NONE
        return None

#FUNCTION TO RETURN EXERCISE WHICH HAS TRATING SCHWACH
def default_exercise_selection(exercise_df):
    schwach_df = exercise_df[exercise_df['tRating'] == 'Schwach']
    schwach_df = schwach_df[['ID']]
    schwach_ex_list = schwach_df.to_dict(orient='records')
    randomFavoriteExercise = random_output_from_a_list(schwach_ex_list).get('ID')
    return randomFavoriteExercise
