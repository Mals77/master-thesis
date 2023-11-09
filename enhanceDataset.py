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
        if  list(df['NumberOfOffers'])[0] <= 2:
            df['treatment'] = "notTreated"  # T=1
        else:
            df['treatment'] = "treated" # T=0
        return df
    # add new treatment for each case based on number of offers
    # cases with only one offer should be treated
    treatedLog = log.groupby('case:concept:name').apply(check_NoOfOffers)
    treatedLog = treatedLog.reset_index(drop=True)
    return treatedLog

def addSuccessColumns(log):
    # if case includes A_Pending than column successful = 1, else 0
    log['successful'] = log.groupby('case:concept:name')['concept:name'].transform(lambda x: 1 if 'A_Pending' in x.values else 0)
    # make column treatmentSuccess, here treated and if successfull Yes, else No
    log['treatmentSuccess'] = log.apply(lambda row: 'Yes' if row['treatment'] == 'treated' and row['successful'] == 1 else 'No' if row['treatment'] == 'treated' and row['successful'] == 0 else '', axis=1)
    #log['treatmentSuccess'] = log.groupby('case:concept:name').apply(lambda group: "Yes" if ('treated' in group['treatment'].values) and ('successful' == 1) else "No" if ('treated' in group['treatment'].values) else '').reset_index(level=0, drop=True)
    return log

def enhancement(finishedCases):
    offersLog = add_No_Of_Offers(finishedCases)
    treatedLog = addTreatment(offersLog)
    sucessLog = addSuccessColumns(treatedLog)
    return sucessLog