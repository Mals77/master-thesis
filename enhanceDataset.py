import pandas as pd

# add NumberOfOffers column to the dataset based on "O_Created" Activity
def add_No_Of_Offers(log):
    tmp_df = log[log['concept:name'] == "O_Created"] 
    tmp_df2 = pd.DataFrame(tmp_df.groupby(['case:concept:name'])['concept:name'].count()).reset_index()
    tmp_df2.columns = ['case:concept:name', 'NumberOfOffers']
    offersLog = pd.merge(tmp_df2, log, on='case:concept:name')
    return offersLog

def addTreatment(log):
    # case should be marked as treated if it receives more than one offer

    def check_NoOfOffers(gr):
        df = pd.DataFrame(gr)
        
        # case should be not treated if it receives more than one offer
        if  list(df['NumberOfOffers'])[0] <= 1:
            df['treatment'] = "treat"  # T=1
        else:
            df['treatment'] = "noTreat" # T=0
        return df
    

    # add new treatment for each case based on number of offers
    # cases with only one offer should be treated
    df = log.groupby('case:concept:name').apply(check_NoOfOffers)
    df = df.reset_index(drop=True)
    return df


#TODO: add column successfull or not successful

def enhancement(finishedCases):
    offersLog = add_No_Of_Offers(finishedCases)
    addTreatment(offersLog)