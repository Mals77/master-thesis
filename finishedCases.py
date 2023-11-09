import pandas as pd


def deleteUnfinishedCases(eventLog):
    eventLog
    mask = eventLog.groupby('case:concept:name')['concept:name'].transform(
        lambda x: any(status in x.values for status in ['A_Pending', 'A_Denied', 'A_Cancelled'])
    )

    finishedCases = eventLog[mask]
    #finishedCases.to_csv("bpi2017_finishedCases.csv", sep=",", index=False)
    count_unfinished_cases = set(eventLog['case:concept:name'].unique()) - set(finishedCases['case:concept:name'].unique())

    print("Number of relevant (finished) cases: ", len(set(finishedCases['case:concept:name'].unique())))
    print("Number of unfinished cases: ", len(count_unfinished_cases))
    return finishedCases