import pandas as pd

def checkOneValue(log):
    #check that the columns only have one value if NumberOfOffers is 1
    columns_to_check = ['FirstWithdrawalAmount','NumberOfTerms', 'MonthlyCost', 'CreditScore', 'Accepted', 'Selected', 'OfferedAmount', 'OfferID']
    offer_1_df = log[log['NumberOfOffers'] == 1]
    unique_values_per_caseid = offer_1_df.groupby('case:concept:name')[columns_to_check].nunique()
    cases_with_multiple_unique_values = unique_values_per_caseid[unique_values_per_caseid.gt(1).any(axis=1)]
    if cases_with_multiple_unique_values.empty:
        return True
    else:
        return False


def fillOneOffer(log):
    check = checkOneValue(log)
    if check == True:
        list = ['FirstWithdrawalAmount', 'NumberOfTerms', 'MonthlyCost', 'CreditScore', 'Accepted', 'Selected', 'OfferedAmount', 'OfferID']
        for i in list:
            mask = (log['NumberOfOffers'] == 1) & (log[i].notna())
            # Create a mapping of concept:name to the corresponding non-NaN value in NumberOfTerms
            mapping = log.loc[mask].set_index('case:concept:name')[i].to_dict()
            
            # Use the mapping to fill NaN values based on concept:name and Offer condition
            log[i] = log.apply(lambda row: mapping.get(row['case:concept:name']) if pd.isna(row[i]) and row['NumberOfOffers'] == 1 else row[i], axis=1)
        return log
    else:
        print("More than one unique value for one Case Offer")

def fillNa(log):
    filledlog = fillOneOffer(log)
    return filledlog