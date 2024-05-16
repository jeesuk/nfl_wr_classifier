import numpy as np
import pandas as pd

def drop_rename_cols(df, drop_cols=None, rename_cols=None):
    '''
    1. Description
    Cleans a pandas df by dropping specified columns and renaming specified columns.

    2. Parameters:
    df = a Pandas DataFrame
    drop_cols (list, optional): A list of column names to drop from the DataFrame. Defaults to None.
    rename_cols (list, optional): A list of column names to rename. Defaults to None.
    
    3. Returns:
    pd.DataFrame: The cleaned DataFrame with specified dropped columns and specified renamed columns.
    '''

    if drop_cols is not None:
        df = df.drop(columns=drop_cols, errors='ignore')
    if rename_cols is not None:
        df = df.rename(columns=rename_cols)
    return df

def fetch_data(game_ids, api_key):
    '''
    1. Description
    Fetch play-by-play data for a list of NFL games using the SportRadar API.

    This function takes a list of game IDs and an API key to fetch play-by-play data
    for each game from the SportRadar API. It returns a list of JSON objects containing
    the play-by-play data for each game.

    2. Parameters:
    game_ids (list of str): A list of game IDs for which to fetch play-by-play data.
    api_key (str): The API key to authenticate the request to the SportRadar API.

    3. Returns:
    list of dict: A list of JSON objects, where each object contains the play-by-play data for a game.

    Example:
    >>> game_ids = ['game1_id', 'game2_id', 'game3_id']
    >>> api_key = 'your_api_key_here'
    >>> data = fetch_data(game_ids, api_key)
    >>> print(data)

    Notes:
    - The function makes a separate HTTP GET request for each game ID.
    - It handles HTTP status code 200 for successful requests and prints an error message
      for any other status codes.
    - There is a 1-second delay between each request to avoid hitting the API rate limit of 1 query per second.
    - In case of an exception during the requests, an error message is printed and the connection
      is closed properly.

    '''

    all_games_data = []
    conn = http.client.HTTPSConnection("api.sportradar.us")

    try:
        for game in game_ids:
            url = f"/nfl/official/trial/v7/en/games/{game}/pbp.json?api_key={api_key}"
            conn.request("GET", url)
            res = conn.getresponse()
            if res.status == 200:
                data = res.read()
                json_data = json.loads(data.decode("utf-8"))
                all_games_data.append(json_data)
            else:
                print(f'Error fetching data for game {game}: {res.status} {res.reason}')
            time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

    return season_all_games


def concat_df(left_df, right_df):

    '''
    1. Description
    Concatenate two DataFrames horizontally and reset their indices.

    This function takes two pandas DataFrames, resets their indices, and concatenates
    them along the columns (axis=1). The resulting DataFrame will have the columns
    from both input DataFrames.

    2. Parameters:
    left_df (pandas.DataFrame): The first DataFrame to concatenate.
    right_df (pandas.DataFrame): The second DataFrame to concatenate.

    3. Returns:
    pandas.DataFrame: A new DataFrame resulting from the horizontal concatenation
                      of the input DataFrames.

    Example:
    >>> import pandas as pd
    >>> df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    >>> df2 = pd.DataFrame({'C': [5, 6], 'D': [7, 8]})
    >>> combined_df = concat_df(df1, df2)
    >>> print(combined_df)
       A  B  C  D
    0  1  3  5  7
    1  2  4  6  8

    Notes:
    - The indices of both DataFrames are reset before concatenation to ensure
      they align correctly.
    - The concatenation is performed along the columns (axis=1), so the resulting
      DataFrame will have all the columns from both input DataFrames.
    '''

    left_df = left_df.reset_index(drop = True)
    right_df = right_df.reset_index(drop = True)

    combined_df = pd.concat([left_df, right_df], axis=1)
    return combined_df



def calculate_covariance(one, two):
    '''
    1. Description
    Calculate the covariance between two features.

    This function computes the covariance between two numeric feature vectors.
    Covariance is a measure of how much two random variables vary together.
    It is calculated as the sum of the product of the differences of each pair
    of values from their respective means, divided by the number of observations
    minus one.
    
    2. Parameters:
    one (array-like): A numeric feature vector.
    two (array-like): Another numeric feature vector.

    3. Returns:
    float: The covariance between the two feature vectors.

    Example:
    >>> import numpy as np
    >>> one = np.array([1, 2, 3, 4, 5])
    >>> two = np.array([5, 4, 3, 2, 1])
    >>> cov = calculate_covariance(one, two)
    >>> print(cov)
    -2.5

    Notes:
    - The function assumes that the input vectors `one` and `two` are of the same length.
    - Covariance is positive if the variables tend to increase together, negative if one tends to increase when the other decreases, and zero if they are uncorrelated.
    '''
    mean_one = np.mean(one) # Mean of feature one vector
    mean_two = np.mean(two) # Mean of feature two vector
    covariance = sum((one[i] - mean_one) * (two[i] - mean_two) for i in range(len(one))) / (len(one) - 1) # Sum of each value in feature vector less its mean, divided by (n-1)
    return covariance



def knn(features, train_input, test_input, train_output, k):
    '''
    1. Description
    Perform k-nearest neighbors (k-NN) classification.

    This function implements the k-NN algorithm to predict the label of a test input
    based on the labels of the k nearest neighbors in the training data. The distance
    metric used is the Euclidean distance.

    2. Parameters:
    features (list of str): List of feature names used for distance calculation.
    test_input (dict): A dictionary representing the test input with feature values.
    k (int): The number of nearest neighbors to consider for the prediction.

    3. Returns:
    object: The predicted label for the test input.

    Example:
    >>> features = ['feature1', 'feature2']
    >>> test_input = {'feature1': 1.5, 'feature2': 2.5}
    >>> k = 3
    >>> prediction = knn(features, test_input, k)
    >>> print(prediction)
    'class_label'

    Notes:
    - The function computes the Euclidean distance between the test input and each instance
      in the training data.
    - The label of the test input is predicted as the mode of the labels of the k nearest neighbors.
    '''
    squared_distance = 0
    for feature in features:
        squared_distance += (train_input[feature] - test_input[feature])**2
    train_input['distance'] = squared_distance**(1/2)
    
    prediction = train_output[train_input['distance'].nsmallest(n=k).index].mode()[0]
    return prediction