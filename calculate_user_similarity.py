from typing import Any
import numpy as np
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


"""
This file output:
id	04d8RuiRG4fAVqD03TVJEclB0hb2	08kBRIxHRyUKvz9AxYOZLYmc1iF3	0M4iez2mW7f83dkA4pfBiKJYprH2	0MOmKutBXvaW5fqm2lbUNqkgOzm1	0huTzqszsjT56ALYWJDrDrxF1du1	0iEDSw2qQfe0fN0WpE8xkQ4WXth1	0kxJ5b5P3zeqXBMrfH6biUDih7z1	0m5M22UnkPMZ8VLPz2O6sh7ICXQ2	0rOrtJ0eotXB3ERbAniFmwFun892	0s7xGuBmCbRPaAhsB2cdB2uwEXL2	...	yevGKTHH9Ehjrn166z50tfQFPob2	yg3EDXwIIoXi35roFeKL5DmqBWt1	ykeu2QJNW4WaOMZd0em1h5PUz6a2	ypGdHHrfZmTrACVLNuO0lz2ocyt2	yqOelFCPiVXcMvNjJBlOyliknWC2	z2nwvIdv8URVEpsc0zWhl24h7C43	zRSf4u1duKYm2qMOAYngsh0i2Jy1	zu1oZAOTz5YBeotQ649NIJzCHeW2	zz9JfdE4Dpak60ANlojAcbpOQe42	zzoFiGS46ecyASIUuKUX6Kl2OYl1
id																					
04d8RuiRG4fAVqD03TVJEclB0hb2	1.000000e+00	4.710091e-13	2.806012e-13	1.904079e-13	9.019323e-14	9.019323e-14	2.806012e-13	1.403006e-13	2.906226e-13	1.002147e-13	...	4.309232e-13	8.017176e-14	5.000000e-01	5.000000e-01	5.000000e-01	1.803865e-13	5.000000e-01	1.302791e-13	1.503220e-13	1.904079e-13
08kBRIxHRyUKvz9AxYOZLYmc1iF3	4.710091e-13	1.000000e+00	5.000000e-01	5.000000e-01	3.260832e-13	5.000000e-01	5.000000e-01	5.000000e-01	5.000000e-01	5.000000e-01	...	1.000000e+00	5.000000e-01	2.898517e-13	5.000000e-01	5.000000e-01	5.000000e-01	1.268101e-12	5.000000e-01	5.000000e-01	5.000000e-01
0M4iez2mW7f83dkA4pfBiKJYprH2	2.806012e-13	5.000000e-01	1.000000e+00	5.000000e-01	1.942623e-13	5.000000e-01	5.000000e-01	5.000000e-01	1.000000e+00	5.000000e-01	...	5.000000e-01	1.000000e+00	5.000000e-01	5.000000e-01	7.770493e-13	1.000000e+00	5.000000e-01	1.000000e+00	5.000000e-01	5.000000e-01
0MOmKutBXvaW5fqm2lbUNqkgOzm1	1.904079e-13	5.000000e-01	5.000000e-01	1.000000e+00	1.318209e-13	5.000000e-01	5.000000e-01	5.000000e-01	5.000000e-01	5.000000e-01	...	5.000000e-01	5.000000e-01	1.171741e-13	5.000000e-01	5.272835e-13	5.000000e-01	5.126367e-13	5.000000e-01	5.000000e-01	5.000000e-01
0huTzqszsjT56ALYWJDrDrxF1du1	9.019323e-14	3.260832e-13	1.942623e-13	
"""


def calculate_user_similarity(all_users: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the user similarity matrix based on cleaned user data from the database.

    Steps:
    1. Clean the user data.
    2. Extract and normalize numerical data (age).
    3. Extract and encode categorical data (gender, goal).
    4. Combine the numerical and categorical data.
    5. Compute the similarity matrix using cosine similarity.

    Parameters:
    - db: Database connection object.

    Returns:
    - pd.DataFrame: A DataFrame containing the similarity matrix, with users as both rows and columns,(see above)
    """
    # Clean the user data
    cleaned_users_df = clean_user_data(all_users)
    extracted_columns_all_users = cleaned_users_df[['userId','goal',"gender",'age','language','company','dailyStreak','guideAvatar']]
    extracted_columns_all_users.set_index('userId', inplace=True)
    #print(extracted_columns_all_users)
    # Extract numerical data (age)
    numerical_data = extracted_columns_all_users[['age','dailyStreak']].values

    # Extract categorical data (gender, goal)
    categorical_data = extracted_columns_all_users[['gender', 'goal','language','company','guideAvatar']].values

    # Normalize numerical data (age) using Min-Max scaling
    scaler = MinMaxScaler()
    normalized_numerical_data = scaler.fit_transform(numerical_data)

    # Encode categorical data (gender, goal) using one-hot encoding
    encoder = OneHotEncoder()
    encoded_categorical_data = encoder.fit_transform(categorical_data).toarray()

    # Combine numerical and categorical data
    combined_data = np.hstack((normalized_numerical_data, encoded_categorical_data))

    # Compute similarity matrix using cosine similarity
    similarity_matrix = cosine_similarity(combined_data)

    # Return the similarity matrix as a DataFrame with users as both rows and columns
    return pd.DataFrame(similarity_matrix, index=extracted_columns_all_users.index, columns=extracted_columns_all_users.index)




def clean_user_data(all_users: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the user data by handling missing values and normalizing certain fields.

    Parameters:
    - all_users (DataFrame): The DataFrame containing user data.

    Returns:
    - DataFrame: The cleaned user data DataFrame with columns(userId, goal, gender, age).
    """
    # Process missing values in the user data
    all_users_cleaned = process_nan_values(all_users)

    # Normalize age values
    all_users_cleaned = normalize_age_value(all_users_cleaned)

    # Normalize goal values
    all_users_cleaned.loc[:, 'goal'] = all_users_cleaned['goal'].apply(normalize_goal_value)

    # Normalize gender values
    all_users_cleaned.loc[:, 'gender'] = all_users_cleaned['gender'].apply(normalize_gender_value)

    all_users_cleaned.loc[:,'language'] = all_users_cleaned['language'].apply(normalize_language_value)

    all_users_cleaned.loc[:,'company'] = all_users_cleaned['company'].apply(normalize_company_value)

    all_users_cleaned.loc[:,'guideAvatar'] = all_users_cleaned['guideAvatar'].apply(normalize_avatar_value)

    return all_users_cleaned

def normalize_avatar_value(guideAvatar: Any) -> str:
    if guideAvatar is np.nan:
        return "boy"
    avatar_mapping = {
        0: 'boy',
        1: 'boy',
        2: 'girl1',
        3: 'girl2',
        4: 'girl3',
        'boy-bright-skin-blue-hair-glasses': 'boy',
        'girl-bright-skin-dark-hair': 'girl1',
        'girl-dark-skin-dark-hair-hat': 'girl2',
        'girl-dark-skin-white-hair': 'girl3'
    }
    return avatar_mapping.get(guideAvatar, guideAvatar)

def normalize_company_value(company: Any) -> str:
    if isinstance(company, str):
        return "b2b"
    return "b2c"

def normalize_language_value(language: str) -> str:
    if isinstance(language, str):
        if language.lower() in {"en"}:
            return "en"
    return "de"


def normalize_goal_value(goal: str) -> str:
    """
    The data for goal field saved in firestore are vaired. Therefore, Normalize the user's goal value to a standard format,

    Parameters:
    - goal (str): The original goal value.

    Returns:
    - str: The normalized goal value.
    """
    # Mapping of original goal values to standardized format
    goal_mapping = {
        'Structure': 'structure', 'Struktur': 'structure',
        'Everyday Support': 'dailySupport', 'Alltagsunterstützung': 'dailySupport',
        'Relaxation': 'relaxation', 'Entspannung': 'relaxation',
        'Persönlichkeitsentwicklung': 'personalDevelopment', 'Personal Development': 'personalDevelopment',
        'Neugierde': 'curiosity', 'Curiosity': 'curiosity',
        '1:1 Gespräche': 'oneOnOneConversation', '1:1 Conversations': 'oneOnOneConversation',
        'Trackings': 'trackings'
    }
    # Return the normalized goal value, or the original value if not found in the mapping
    return goal_mapping.get(goal, goal)


def normalize_gender_value(gender: str) -> str:
    """
    Normalize the user's gender value to a standard format.

    Parameters:
    - gender (str): The original gender value.

    Returns:
    - str: The normalized gender value.
    """
    # Mapping of original gender values to standardized format
    gender_mapping = {
        'Männlich': 'male', 'Male': 'male', 'männlich': 'male',
        'Weiblich': 'female', 'Female': 'female', 'weiblich': 'female',
        'keine Angabe': 'nonBinary', 'Nicht-binär': 'nonBinary',
        'preferNotToSay': 'nonBinary', 'Non-binary': 'nonBinary'
    }
    # Return the normalized gender value, or the original value if not found in the mapping
    return gender_mapping.get(gender, gender)


def normalize_age_value(users_df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the 'age' column in the user DataFrame by filling missing values with the mean age and converting to integers.

    Parameters:
    - users_df (DataFrame): DataFrame containing user data.

    Returns:
    - DataFrame: The DataFrame with the 'age' column normalized.
    """
    # Fill missing values in the 'age' column with the mean age
    users_df.loc[:, 'age'] = users_df['age'].fillna(users_df['age'].mean())
    # Convert the 'age' column values to integers
    users_df.loc[:, 'age'] = users_df['age'].astype(int)

    return users_df


def process_nan_values(users_df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the user data DataFrame by handling missing values.

    Steps:
    1. Remove rows where 'goal' or 'gender' is NA.
    2. Replace NA values in the 'age' column with the mean age.

    Parameters:
    - users_df: pd.DataFrame containing user data with columns 'age', 'gender', and 'goal'.

    Returns:
    - pd.DataFrame: The cleaned user data DataFrame.
    """
    users_df = users_df.dropna(subset=['goal', 'gender'])
    users_df['age'] = users_df['age'].fillna(users_df['age'].mean())
    users_df['dailyStreak'] = users_df['dailyStreak'].fillna(0)
    return users_df