import pandas as pd
import time
import os
from datetime import datetime, timedelta
import numpy as np
import scipy.stats
from pre_process import framesort
from multi_pfOct29 import multipf
from ransac import RANSAC_Scoring
from debugger_tool import Converter
import csv


# Read CSV Files 
weightdf = pd.read_csv('/Users/cjbertumen/Desktop/Prototype Demonstration/Weight-Event-Results.csv')

# read vision csv files
visiondf = pd.read_csv("/Users/cjbertumen/Desktop/Prototype Demonstration/projectdemo-1.csv",index_col=0)

visiondf.loc[:,'Timestamp'] = pd.to_datetime(visiondf.loc[:,'Timestamp']) 
weightdf.loc[:,'Timestamp'] = pd.to_datetime(weightdf.loc[:,'endTime'])


cctvBackTracked = []
weight_action_list=[]
for idx, row in weightdf.iterrows():
    time_weight = weightdf.loc[idx,'Timestamp']
    time_cctvbacktrack = time_weight - timedelta(seconds=1.35)
    cctvBackTracked.append([visiondf[(visiondf['Timestamp']>time_cctvbacktrack) & (visiondf['Timestamp']<time_weight)]])
    weight_action_list.append([row])


# print(cctvBackTracked[19][0])
# extractor=cctvBackTracked[0][0]
# converter=extractor.to_numpy()


weightdfnp=weightdf.to_numpy()

#Filtering the detections from the merged list- We process one weight detection per time
integration=[]
high_score=[]
for j in range(len(cctvBackTracked)):
    cctv=cctvBackTracked[j][0]
    if len(cctv)!=0:
        sorted=cctv.to_numpy()
        nmin=cctv.loc[:,'Frame'].min()
        detection_length=len(cctv)
        weight_bin=weight_action_list[j][0][4]
        global_pcentroid,global_pkeypoint9,global_pkeypoint10=multipf(nmin,detection_length,sorted)
        scores=RANSAC_Scoring(weight_bin,global_pcentroid,global_pkeypoint9,global_pkeypoint10)
        high_score= max(scores, key=lambda x: x[1])
        integration.append([weightdfnp[j][0],weightdfnp[j][1],weightdfnp[j][2],weightdfnp[j][3], weightdfnp[j][4], weightdfnp [j][5], weightdfnp[j][6],weightdfnp[j][7], weightdfnp[j][8], weightdfnp[j][9], weightdfnp[j][10], high_score[0]])
    else:
        false_append=[weightdfnp[j][0],weightdfnp[j][1],weightdfnp[j][2],weightdfnp[j][3], weightdfnp[j][4], weightdfnp [j][5], weightdfnp[j][6],weightdfnp[j][7], weightdfnp[j][8], weightdfnp[j][9], weightdfnp[j][10]]
        false_append.append(np.nan)
        integration.append(false_append)

Converter(integration)