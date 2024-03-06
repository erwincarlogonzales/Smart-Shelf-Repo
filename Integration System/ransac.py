from dot_projector import bin_thresholds
from sklearn.linear_model import LinearRegression, RANSACRegressor
import numpy as np 

def x_unpacker(filtered_id):
    xdata=[]
    for xunpack in range(len(filtered_id)):
        x_data=filtered_id[x_unpacker][0]
        xdata.append(x_data)
    return xdata

def MAD(coordinates_inside_rectangle): #Returns the MAD for the model generator
    ydata=[]
    xdata=[]
    for unpacker in range(len(coordinates_inside_rectangle)):
        y_data=coordinates_inside_rectangle[unpacker][1]
        ydata.append(y_data)
    
    for unpacker2 in range(len(coordinates_inside_rectangle)):
        x_data=coordinates_inside_rectangle[unpacker2][0]
        xdata.append(x_data)


    mad=np.mean(np.absolute(ydata-np.mean(ydata)))

    return mad, ydata, xdata

def RANSAC_model_generator(coordinates_inside_rectangle):
    mad,xdata,ydata=MAD(coordinates_inside_rectangle)
    data=np.column_stack((xdata,ydata))
    ransac_model_wbin=RANSACRegressor(LinearRegression(),min_samples=2,residual_threshold=mad) #get the RANSAC model of the Weight Bin
    ransac_model_wbin.fit(data[:,0].reshape(-1,1),data[:,1])
    return ransac_model_wbin, mad

def RANSAC_data_evaluator(data,ransac_model,mad):
    results=[]
    for iter, point in enumerate(data):
        predicted_value = ransac_model.predict(point[0].reshape(1, -1))
        if np.abs(predicted_value - point[1]) < mad:
            results.append(1) #Inliers
        else:
            results.append(0) #Outliers
    num_inliers = results.count(1)
    return num_inliers

def RANSAC_Scoring(weight_bin,global_pcentroid,global_pkeypoint9,global_pkeypoint10):
    coordinates_inside_rectangle=bin_thresholds(weight_bin)
    ransac_model,mad=RANSAC_model_generator(coordinates_inside_rectangle)
    ransac_scores=[]
    for cscoring in range(len(global_pcentroid)):
        craw=global_pcentroid[cscoring][1]
        craw2=global_pkeypoint9[cscoring][1]
        craw3=global_pkeypoint10[cscoring][1]
        combi=np.append(craw, craw2, axis=0)
        for_process=np.append(combi,craw3, axis=0)
        num_inliers=RANSAC_data_evaluator(for_process,ransac_model,mad)
        ransac_scores.append([global_pcentroid[cscoring][0],num_inliers])

    return ransac_scores


