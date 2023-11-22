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

def fillCreateOffer(log):
    #set Offer_ID of a create offer to the Offer_ID in O_Created below
    mask = log['concept:name'] == 'O_Create Offer'
    log.loc[mask, 'OfferID'] = log['OfferID'].shift(-1)
    return log

def fillTopCase(df):
    cases_with_multiple_offers = df[df['NumberOfOffers'] > 1]
    start_index = cases_with_multiple_offers.groupby('case:concept:name').head(1).index
    stop_offers = cases_with_multiple_offers.groupby('case:concept:name')['OfferID'].first()
    stop_offers = stop_offers.to_list()
    stop_index =  []
    for offer in stop_offers:
        first_appearance_index = (df['OfferID'] == offer).idxmax()
        stop_index.append(first_appearance_index)
    for start, stop, offer in zip(start_index, stop_index, stop_offers):
        df.loc[start:stop, 'OfferID'] = offer
    return df

def fillOfferID(log):
    log['OfferID'].fillna(method='ffill', inplace=True)
    return log

def fillAllValues(log):
    # Filter rows with concept "O_Create Offer" to create a mapping DataFrame
    offer_mapping = log[log['concept:name'] == 'O_Create Offer'][['OfferID', 'FirstWithdrawalAmount', 'NumberOfTerms', 'MonthlyCost', 'CreditScore', 'Accepted', 'Selected', 'OfferedAmount']]
    
    # Merge the original DataFrame with the offer_mapping DataFrame based on OfferID
    df = pd.merge(log, offer_mapping, on='OfferID', how='left', suffixes=('', '_offer'))
    
    # Fill the specified columns with values from the mapped columns
    columns_to_fill = ['FirstWithdrawalAmount', 'NumberOfTerms', 'MonthlyCost', 'CreditScore', 'Accepted', 'Selected', 'OfferedAmount']
    for column in columns_to_fill:
        df[column].fillna(df[f'{column}_offer'], inplace=True)
    
    # Drop the columns with "_offer" suffix as they are no longer needed
    df.drop(columns=[f'{column}_offer' for column in columns_to_fill], inplace=True)
    return df


def fillNaN(log):
    filledOneOffer = fillOneOffer(log)
    filledCreateOffer = fillCreateOffer(filledOneOffer)
    filledTop = fillTopCase(filledCreateOffer)
    filledOfferID = fillOfferID(filledTop)
    filledlog = fillAllValues(filledOfferID)
    return filledlog