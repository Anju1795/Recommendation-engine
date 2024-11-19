from typing import List
from .calculate_user_similarity import calculate_user_similarity
from .get_all_users import get_all_users
from google.cloud.firestore_v1 import Client


def get_top_similar_users_for_one_user(user_id: str,db: Client, top_n=5,) -> List[str]:
    all_user = get_all_users(db)
    similarity_matrix_df = calculate_user_similarity(all_user)
    if user_id not in similarity_matrix_df.columns:
        return []
    # Find the top similar users
    try:
        similar_users = similarity_matrix_df[user_id].nlargest(top_n + 1).iloc[1:]
        return similar_users.index.tolist()
    except KeyError:
        # If user_id is not found in the similarity matrix, return an empty list
        return []
    

def get_similar_user_with_similarity_greater_than_threshold(user_id: str,db: Client) -> List[str]:
    all_user = get_all_users(db)
    similarity_matrix = calculate_user_similarity(all_user)
    try:
        similarity_user = similarity_matrix[similarity_matrix[user_id] > 0.7]
        similar_user_ids = similarity_user.index.tolist()
        similar_user_ids.remove(user_id)
        return similar_user_ids
    except KeyError:
        return []



