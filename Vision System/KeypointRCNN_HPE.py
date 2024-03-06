import torch
import cv2
import argparse
from testutils import utils
from time import time
from PIL import Image
from torchvision.transforms import transforms as transforms
from testmodels.models import get_model
import numpy as np
from strongsortt.utils.parser import get_config
from strongsortt.strong_sort import StrongSORT
from strongsortt.sort.tracker import Tracker
from pathlib import Path
import matplotlib
import os
import pandas as pd
import datetime

# transform to convert the image to tensor
transform = transforms.Compose([
    transforms.ToTensor() 
])

# set the computation device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# load the modle on to the computation device and set to eval mode
model = get_model(min_size=800).to(device).eval()
SSORT= StrongSORT(model_weights=Path('/Users/cjbertumen/Downloads/PACK-RMPF-Smart-Shelf-System-for-Customer-Behavior-Tracking-in-Supermarkets-main/Vision System/osnet_x0_25_msmt17.pt'),device=device,fp16=False, max_age=2000) #change to directory

#videos
cap= cv2.VideoCapture(0) #webcam

#parameter for the Locations
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Adjust the codec as needed
fps=15
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

video_output = cv2.VideoWriter('/Users/cjbertumen/Documents/sampler.mp4', fourcc, fps, (width, height)) #change to directory 

VisionResults=[]
frame_idx=0
edges = [
    (0, 1), (0, 2), (2, 4), (1, 3), (6, 8), (8, 10),
    (5, 7), (7, 9), (5, 11), (11, 13), (13, 15), (6, 12),
    (12, 14), (14, 16), (5, 6)
]

cap.set(cv2.CAP_PROP_FPS,5)

while True:
        
        ret, frame= cap.read()
        frame_idx=frame_idx+1

        if not ret: #if no more frames break the loop
            break

        timestampnowcsv = datetime.datetime.now()
        formtimestampcsv = timestampnowcsv.strftime('%m-%d-%Y %H:%M:%S.%f')

        pil_image = Image.fromarray(frame).convert('RGB')
        orig_frame = frame
        # transform the image
        image = transform(pil_image)
        # add a batch dimension
        image = image.unsqueeze(0).to(device)
        start_time=time()
        # get the detections, forward pass the frame through the model
        with torch.no_grad():
            outputs = model(image)
        detections=[]
        conf=[]
        classes=[]
        kpoints=[]
        raw=[]
        rawcf=[]
        output=outputs[0]
        for i in range(len(outputs[0]['keypoints'])): #Human Pose Estimation Module
        # get the detected bounding boxes
            boxes = outputs[0]['boxes'][i].cpu().detach().numpy()
            scores = outputs[0]['scores'][i].cpu().detach().numpy()
            keypoints=outputs[0]['keypoints'][i].cpu().detach().numpy()
            raw.append(boxes)
            rawcf.append(scores)
            if outputs[0]['scores'][i] > 0.8: # proceed if confidence is above 0.9
                detections.append(boxes)
                conf.append(scores)
                classes.append(0) #class-ID 0
                kpoints.append(keypoints)
                keypoints = keypoints[:, :].reshape(-1, 3)
                for p in range(keypoints.shape[0]):
                # draw the keypoints
                    cv2.circle(orig_frame, (int(keypoints[p, 0]), int(keypoints[p, 1])), 
                            3, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            # draw the lines joining the keypoints
                for ie, e in enumerate(edges):
                # get different colors for the edges
                    rgb = matplotlib.colors.hsv_to_rgb([
                    ie/float(len(edges)), 1.0, 1.0
                ])
                    rgb = rgb*255
                # join the keypoint pairs to draw the skeletal structure
                    cv2.line(orig_frame, (int(keypoints[e, 0][0]), int(keypoints[e, 1][0])),
                        (int(keypoints[e, 0][1]), int(keypoints[e, 1][1])),
                        tuple(rgb), 2, lineType=cv2.LINE_AA)
        detection_tracker=len(detections)
        if detection_tracker!=0:
            combi=np.insert(detections,4,conf,axis=1)
            SSORT_detections=np.insert(combi,5,classes,axis=1)
            tracks=StrongSORT.update(SSORT, SSORT_detections,frame) #detection module of SSOrt
            kpoint_length=len(kpoints)
            tracks_length=len(tracks)
            # STRONGSoRT Module
            if len(tracks)==0:
                continue
            else:
                bbox_array=np.asarray(tracks)
                integer_bbox_array=bbox_array.astype(int)
            
                length= len(integer_bbox_array)
                for IDs in range(length):
                    if IDs< length:
                        x1, y1, x2, y2=integer_bbox_array[IDs,0], integer_bbox_array[IDs,1], integer_bbox_array[IDs,2], integer_bbox_array[IDs,3]
                        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                        cropped_image=frame[x1:y1,x2:y2]
                        #calculating for centroid
                        centroid_x= int((x1+x2)/2)
                        centroid_y=int((y1+y2)/2)
                        cv2.circle(frame,(centroid_x,centroid_y),radius=0,color=(0,0,255),thickness=10)
                        if y2 <height*1:
                            tracks_location= "A"
                        elif (height*2 >y2 > height*1):
                            tracks_location= "B"
                        elif y2 > height*2:
                            tracks_location= "C"
                    
                        if kpoint_length >= tracks_length:
                            keypoint_9x=kpoints[IDs][9][0]
                            keypoint_9y=kpoints[IDs][9][1]
                            keypoint_10x=kpoints[IDs][10][0]
                            keypoint_10y=kpoints[IDs][10][1]
                            VisionResults.append([frame_idx, integer_bbox_array[IDs,4], x1, y1, x2, y2, centroid_x, centroid_y,keypoint_9x,keypoint_9y,keypoint_10x,keypoint_10y,formtimestampcsv])   
                        if kpoint_length < tracks_length and IDs < kpoint_length:
                            keypoint_9x=  kpoints [IDs][9][0]
                            keypoint_9y=  kpoints [IDs][9][1]
                            keypoint_10x= kpoints [IDs][10][0]
                            keypoint_10y= kpoints [IDs][10][1]
                            VisionResults.append([frame_idx, integer_bbox_array[IDs,4], x1, y1, x2, y2, centroid_x, centroid_y,keypoint_9x,keypoint_9y,keypoint_10x,keypoint_10y,formtimestampcsv]) 
                        if IDs > kpoint_length:
                            keypoint_9x=0 #CJ to justify if nagzero na we assume that the confidence level of the detections is low= exiting the frame na 
                            keypoint_9y=0 #Integration Notes, if may ReID tapos walang Keypoint Data, we will use the last detected keypoint nila as approximation
                            keypoint_10x=0
                            keypoint_10y=0
                            VisionResults.append([frame_idx, integer_bbox_array[IDs,4], x1, y1, x2, y2, centroid_x, centroid_y,keypoint_9x,keypoint_9y,keypoint_10x,keypoint_10y,formtimestampcsv]) 
                        cv2.putText(frame,"ID: "+str(integer_bbox_array[IDs,4]) + "Loc: " + tracks_location,(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,1.5,cv2.COLOR_BGR2RGB)   
                    else:
                        break
        else:
            VisionResults.append([frame_idx, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, formtimestampcsv])
            pass
        #Exporting Vision Test Results to CSV File:
        filename= "C:/Users/Jillian Clara TV/Desktop/cctv/processed csv/projectdemo-final.csv" #change to directory
        end_time=time()
        fps = 1/np.round(end_time- start_time, 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        timestampnow = datetime.datetime.now()
        formtimestamp = timestampnow.strftime('%m-%d-%Y %H:%M:%S.%f')

        frame = cv2.putText(frame, formtimestamp, (10, 40), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        video_output.write(frame)
        cv2.imshow("Vision Sub-System",frame)
        key= cv2.waitKey(1) #To break the video loop
        if key == 27:
            break

cap.release() 
cv2.destroyAllWindows()
#Converting the Array to CSV
df=pd.DataFrame(VisionResults)
df.columns=["Frame", "TrackID","x1","y1","w","h","x","y","Keypoint 9 (X)","Keypoint 9 (Y)", "Keypoint 10 (X)", "Keypoint 10 (Y)", "Timestamp"]
df.to_csv(filename)