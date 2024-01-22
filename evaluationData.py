import random
import numpy as np
import pandas as pd

def bpi2017Features(df_final):
    treatment=df_final['treatmentOffer']
    features = df_final[['NumberOfOffers', 'Action', 'org:resource',
       'concept:name', 'EventOrigin', 'lifecycle:transition', 'time:timestamp',
       'case:LoanGoal', 'case:ApplicationType', 'case:RequestedAmount',
       'FirstWithdrawalAmount', 'NumberOfTerms', 'Accepted', 'MonthlyCost', 'Selected',
       'CreditScore', 'OfferedAmount', 'offerNumber','timeApplication', 'weekdayApplication']]
    y=df_final['offerSuccess']
    return features, treatment, y

def placeboTreatment(data):
    """Replaces the treatment variable with a new variable randomly generated."""
    inference_features, treatment_col, outcome_col = bpi2017Features(data)
    num_rows = data.df.shape[0]

    X = data.df[data[inference_features]].values
    treatment_new = np.random.randint(2, size=num_rows)
    y = data.df[data.outcome_col].values

    return data, X, y, treatment_new



def randomCause(data):
    inference_features, treatment_col, outcome_col = bpi2017Features(data)
    """Adds an irrelevant random covariate to the dataframe."""
    num_rows = data.df.shape[0]
    new_data = np.random.randn(num_rows)

    X = data.df[data[inference_features]].values
    treatment = data.df[data.treatment_col].values
    y = data.df[data.outcome_col].values
    X_new = np.hstack((X, new_data.reshape((-1, 1))))

    return data, X_new, y, treatment


def randomReplace(data):
    """Replaces a random covariate with an irrelevant variable."""
    inference_features, treatment_col, outcome_col = bpi2017Features(data)
    
    replaced_feature_index = np.random.randint(len(inference_features.columns))
    replaced_feature = inference_features.columns[replaced_feature_index]
    random_value = np.random.randint(0, 100)
    inference_features.iloc[:, replaced_feature_index] = random_value

    new_df = pd.concat([inference_features, treatment_col, outcome_col], axis=1)

    X_new = inference_features.values
    treatment_new = treatment_col.values
    y_new = outcome_col.values

    return new_df, X_new, y_new, treatment_new, replaced_feature


    
def randomSubsetData(data):
    inference_features, treatment_col, outcome_col = bpi2017Features(data)
    """Takes a random subset of size sample_size of the data."""
    #sample_size is between 0.7 and 0.95 of orginal dataset
    sample_size = random.uniform(0.7, 0.95)
    df_new = data.df.sample(frac=data.sample_size).copy()

    X_new = df_new[data.inference_features].values
    treatment_new = df_new[data.treatment_col].values
    y_new = df_new[data.outcome_col].values

    return df_new, X_new, y_new, treatment_new