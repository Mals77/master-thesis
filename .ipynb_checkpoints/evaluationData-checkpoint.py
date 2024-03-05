import random
import numpy as np
import pandas as pd

def bpi2017Features(df_final):
    treatment=df_final['treatmentOffer']
    features = df_final[['NumberOfOffers', 'Action', 'org:resource',
       'concept:name', 'EventOrigin', 'lifecycle:transition', 'time:timestamp',
       'case:LoanGoal', 'case:ApplicationType', 'case:RequestedAmount',
       'FirstWithdrawalAmount', 'NumberOfTerms', 'Accepted', 'MonthlyCost',
       'CreditScore', 'OfferedAmount', 'offerNumber','timeApplication', 'weekdayApplication']]
    y=df_final['offerSuccess']
    return features, treatment, y

def placeboTreatment(data):
    """Replaces the treatment variable with a new variable randomly generated."""
    inference_features, treatment_col, outcome_col = bpi2017Features(data)
    #num_rows = data.shape[0]
    #data['treatmentOffer'] = np.random.randint(2, size=num_rows)

    unique_case_ids = data['case:concept:name'].unique()
    random_values = np.random.randint(2, size=len(unique_case_ids))
    case_random_map = dict(zip(unique_case_ids, random_values))
    data['treatmentOffer'] = data['case:concept:name'].map(case_random_map)

    X = inference_features
    treatment_new = data['treatmentOffer']
    y = outcome_col

    data = pd.concat([inference_features, treatment_new, y], axis=1)

    return data, X, y, treatment_new



def randomCause(data):
    inference_features, treatment_col, outcome_col = bpi2017Features(data)
    """Adds an irrelevant random covariate to the dataframe."""
    # num_rows = data.shape[0]
    # new_data = np.random.randn(num_rows)
    # inference_features['random covariate'] = new_data

    num_unique_cases = len(data['case:concept:name'].unique())
    # Generate random data for each unique caseID
    new_data = np.random.randn(num_unique_cases)
    # Map random data to each caseID
    inference_features['random covariate'] = data['case:concept:name'].map(dict(zip(sorted(data['case:concept:name'].unique()),new_data)))

    X_new = inference_features
    treatment = treatment_col
    y = outcome_col

    data = pd.concat([treatment_col, outcome_col, X_new], axis=1)

    return data, X_new, y, treatment


def randomReplace(data):
    """Replaces a random covariate with an irrelevant variable."""
    inference_features, treatment_col, outcome_col = bpi2017Features(data)
    
    replaced_feature_index = np.random.randint(len(inference_features.columns))
    replaced_feature = inference_features.columns[replaced_feature_index]
    random_value = np.random.randint(0, 100)
    inference_features.iloc[:, replaced_feature_index] = random_value

    new_df = pd.concat([inference_features, treatment_col, outcome_col], axis=1)

    X_new = inference_features
    treatment_new = treatment_col
    y_new = outcome_col

    return new_df, X_new, y_new, treatment_new, replaced_feature


    
def randomSubsetData(data):
    """Takes a random subset of size sample_size of the data."""
    #sample_size is between 0.4 and 0.85 of orginal dataset
    sample_size = random.uniform(0.4, 0.85)
    df_new = data.sample(frac=sample_size).copy()

    inference_features, treatment_col, outcome_col = bpi2017Features(df_new)

    X_new = inference_features
    treatment_new = treatment_col
    y_new = outcome_col

    return df_new, X_new, y_new, treatment_new

def makeReplacedDatasets(n, df):
    for i in range(1, n + 1):
        replaced_df, X, y, t, f  = randomReplace(df)
        replaced_df.to_csv(f'./evaluationDatasets/Replace/randomReplacedDataset{i}.csv', index=False)

def makeSubsetDatasets(n, df):
    for i in range(1, n + 1):
        subset_df, X, y, t = randomSubsetData(df)
        subset_df.to_csv(f'./evaluationDatasets/Subset/randomSubsetDataset{i}.csv', index=False)

def makePlaceborDatasets(n, df):
    for i in range(1, n + 1):
        placebo_df, X, y, t  = placeboTreatment(df)
        placebo_df.to_csv(f'./evaluationDatasets/Placebo/placeboDataset{i}.csv', index=False)

def makeCauseDataset(n, df):
    for i in range(1, n + 1):
        cause_df, X, y, t  = placeboTreatment(df)
        cause_df.to_csv(f'./evaluationDatasets/Cause/addRandomCauseDataset{i}.csv', index=False)

if __name__ == '__main__':
    #make the random evaluation datasets and save them as csv
    #1 for placebo, 1 for randomCause, 10 for randomReplace, 10 for randomSubset
    df = pd.read_csv("bpi2017_final.csv")
    makeSubsetDatasets(10, df)
    makeReplacedDatasets(10, df)
    makePlaceborDatasets(2, df)
    makeCauseDataset(2, df)
    
