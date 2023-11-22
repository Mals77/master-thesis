import pandas as pd

def checkRequirements(log):
    no_time = log['time:timestamp'].isnull().any() or log['time:timestamp'].isna().any()
    no_activity = log['EventID'].isnull().any() or log['EventID'].isna().any()
    no_id =log['case:concept:name'].isnull().any() or log['case:concept:name'].isna().any()
    if no_time == False and no_activity == False and no_id == False:
        print("Requirements satisfied")
    else:
        print("Requirements NOT satisfied")
        if no_activity == True:
            print("Missing Activity")
        if no_time == True:
            print("Missing Time")
        if no_id == True:
            print("Missing ID")
    
def columnNames(log):
    colNames = log.columns.values
    print(colNames)

def infos(log):
    checkRequirements(log)
    columnNames(log)