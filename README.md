
# Master Thesis
This is the repository for my master thesis *"Determining the Optimal Causal Inference Method for Prescriptive Process Monitoring: Applicability, Implementation, and Evaluation of Various Methods"* which looks at causal inference in PrPM.

To run the methods on Juptyer Notebook the **requirementEnvironments** folder provides the requirements of each environment needed. 

The table below gives an overview of the methods, their corresponding file and the environment file.

| Method | File | Environment File |
|--|--|--|
| Pre-Processing and Result Analysis | Datasets + Results Folder | Processing
| Matching | DoWhyMethods, PropScoreMatching  | DoWhy, Matching
| IPW | IPW, DoWhyMethods | Causallib, DoWhy
| TMLE | TMLE | Causallib
| Meta Learner | Meta-Learner | CausalML
| Uplift | XBCF, Uplift, ORF| XBCF, CausalML, DoWhy
| Deep Learning | BCAUSS, CausalEGM, Dragon+CEVEA, Meta-Learners | BCAUSS, EGM, NNCausalML, CausalML

# Quickstart
Get the [BPIC 2017 dataset](https://data.4tu.nl/articles/dataset/BPI_Challenge_2017/12696884)
Run through pre-processing in Datasets folder. Else use the preprocessed file in the ImportantDatasets.zip 

The simulation result is in an .mxml format and can be converted with the [mxml-to-xes GitHub repository](https://github.com/MaxVidgof/mxml-to-xes/tree/master). Else you can use the already converted file, *synthetic-dataset.csv* in the ImportantDataset.zip

Run the causal inference models within each CI-method notebook. 

Results can be stored in Dataframes and the *result.ipynb* shows the Figures and Plots.
