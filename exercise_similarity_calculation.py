from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

#CALCULATE THE COSINE SIMILARITY OF EXERCISES USING THE CATEGORICAL FEATURES.
def calculate_exercise_similarity(exercise_dataframe):
    cleaned_exercise_data = clean_exercise_data(exercise_dataframe)
    features = cleaned_exercise_data[['ID', 'Burnout', 'exerciseKind', 'Coaching Kind', 'Confidence', 'Depression', 'Discipline', 'Effectiveness', 'Motivation', 'Relationships', 'Stress management']]
    features.set_index('ID',inplace=True)
    categorical_features = ['Burnout', 'exerciseKind', 'Coaching Kind', 'Confidence', 'Depression', 'Discipline', 'Motivation', 'Relationships', 'Stress management']
    one_hot = pd.get_dummies(features[categorical_features])
    df_encoded = pd.concat([features.drop(columns=categorical_features), one_hot], axis=1)

    scaler = MinMaxScaler()
    df_encoded[['Effectiveness']] = scaler.fit_transform(df_encoded[['Effectiveness']])
    similarity_matrix = cosine_similarity(df_encoded)
    return pd.DataFrame(similarity_matrix, index=features.index, columns=features.index)

def clean_exercise_data(ex_dataframe):
    exercises_cleaned = process_nan_values(ex_dataframe)
    exercises_cleaned = normalize_effectiveness_value(exercises_cleaned)
    return exercises_cleaned

def process_nan_values(ex_dataframe):
    ex_dataframe.replace({'ja': 1, 'nein': 0, 'Ja': 1, 'Nein': 0,'.-': 0.5}, inplace=True)
    ex_dataframe = ex_dataframe.fillna({'exerciseKind': 'Unknown', 'Coaching Kind': 'Unknown', 'Burnout': 0, 'Confidence': 0, 'Discipline': 0, 'Effectiveness': 0, 'Motivation': 0, 'Relationships': 0, 'Stress management': 0})
    return ex_dataframe

def normalize_effectiveness_value(exercises_cleaned):
    exercises_cleaned['Effectiveness'] = exercises_cleaned['Effectiveness'].str.replace(',', '.').astype(float)
    return exercises_cleaned
