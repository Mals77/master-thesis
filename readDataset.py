import pandas as pd
import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.conversion.log import converter as xes_converter
from pm4py.objects.log.exporter.xes import exporter as xes_exporter

def readData():
    log = xes_importer.apply("BPI_Challenge_2017.xes")

    xesDataframe = xes_converter.apply(log, variant=xes_converter.Variants.TO_DATA_FRAME)
    return xesDataframe
    #df = pd.read_csv("bpi_challenge_2017.csv")

def readfinishedLog():
    df = pd.read_csv("bpi2017_finishedCases.csv")