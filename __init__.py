# call this root function, then return recommendation Exercises

"""
exercise:
  - getRecExercise(String userId, similarityMatrix)
    - check user favriote exercise(userId)
      - fav is not empty
         if not empty, recommendation similar ex
      - fav is empty
          - check exercise rating
             - if rating empty
                - check the similar users(take 5 similar users, check their favor exercises)
                        - if still empty
                           - random give one tRating "schwach"(maybe be use this t-rating)
             - if rating not empty
                - if exercise id starts with 3. 4. ...9 .  10.
                     -check if the recommendation exercise with highest clicked
                       then return the similar exercise with this exercise
                - else
                     recommend similar exercises
    return exerciseId 
"""