#Particle Tracker
import numpy as np
import scipy as scipy
from particle_filter import ParticleFilter
from numpy.random import randn
from ransac import RANSAC_Scoring


def create_gaussian_particles(initial_pos, std):
    particle_no=100
    particles = np.empty((particle_no, 2))
    particles[:, 0] = initial_pos[0] + (randn(particle_no) * std)
    particles[:, 1] = initial_pos[1] + (randn(particle_no) * std)
    return particles, particle_no

def weight_generator(particle_no):
     weights=np.empty(particle_no)
     weights.fill(1./particle_no)
     return weights

def trackID_checker(global_pcentroid):
    current_TrackID=[]
    for ID_extract in global_pcentroid: #checks for current Track IDs
                            current_TrackID.append(ID_extract[0])
    return current_TrackID


     
def multipf(nmin,detection_length,sorted):
    processing=[]
    frame_track=nmin #keeps track of the frames
    processing_previous_length=0
    global_pcentroid=[] #global particles of the centroid 
    global_pkeypoint9=[] #global particles of keypoint9
    global_pkeypoint10=[] #global particles of keypoint 10
    global_wcentroid=[] #global weight of centroid
    global_wkeypoint9=[] #global weight of keypoint9
    global_wkeypoint10=[] #global weight of keypoint10

    for i in range(detection_length): #Processing of the Particle Filter per state points
        if sorted[i][0]== frame_track: #sorts each track ID per frame
            processing.append(sorted[i])
        else: #if it will go to the next frame 
            if processing[0][0]== nmin: #checks if it the processing array is the first frame in the event 
                for iter in range(len(processing)): #appends the initial states- this is for distributing each particle
                    centroid=[processing[iter][6],processing[iter][7]] 
                    pcentroid,particle_no=create_gaussian_particles(centroid,115.1560000514251) #set arbritarily at 0.1; once we got the variance of the pixels we can adjust this 
                    wcentroid=weight_generator(particle_no)
                    global_pcentroid.append([processing[iter][1],pcentroid])
                    global_wcentroid.append([processing[iter][1],wcentroid])
                    keypoint9=[processing[iter][8],processing[iter][9]] 
                    pk9,particle_no2=create_gaussian_particles(keypoint9,115.1560000514251)
                    wk9=weight_generator(particle_no2)
                    global_pkeypoint9.append([processing[iter][1],pk9])
                    global_wkeypoint9.append([processing[iter][1],wk9])
                    keypoint10=[processing[iter][10],processing[iter][11]]
                    pk10,particle_no3=create_gaussian_particles(keypoint10,115.1560000514251)
                    wk10=weight_generator(particle_no3)
                    global_pkeypoint10.append([processing[iter][1],pk10])
                    global_wkeypoint10.append([processing[iter][1],wk10])
                processing=[] #since this part is already a new frame; we clear the previous array and prepare it for the new frame for processing
                processing.append(sorted[i]) #gets the new pieces of information
                frame_track=frame_track+1 #updates the frame iteration
            else: #this line of code begins the actual particle filtering of each keypoint
                current_TrackID=trackID_checker(global_pcentroid) #checks all current Track IDs
                pop_list=[]
                new=[]
                for checker in processing:
                        if checker[1] not in current_TrackID: # check if TrackID is present or not. 
                            pop_list.append(checker[1])
                            centroid=[checker[6],checker[7]]
                            pcentroid,particle_no=create_gaussian_particles(centroid,115.1560000514251) #set arbritarily at 0.1; once we got the variance of the pixels we can adjust this 
                            wcentroid=weight_generator(particle_no)
                            global_pcentroid.append([checker[1],pcentroid])
                            global_wcentroid.append([checker[1],wcentroid])
                            keypoint9=[checker[8],checker[9]]
                            pk9,particle_no2=create_gaussian_particles(keypoint9,115.1560000514251) #set arbritarily at 0.1; once we got the variance of the pixels we can adjust this 
                            wk9=weight_generator(particle_no2)
                            global_pkeypoint9.append([checker[1],pk9])
                            global_wkeypoint9.append([checker[1],wk9])
                            keypoint10=[checker[10],checker[11]]
                            pk10,particle_no3=create_gaussian_particles(keypoint10,115.1560000514251) #set arbritarily at 0.1; once we got the variance of the pixels we can adjust this 
                            wk10=weight_generator(particle_no3)
                            global_pkeypoint10.append([checker[1],pk10])
                            global_wkeypoint10.append([checker[1],wk10])
                        else:
                            continue
                    
                if len(pop_list)!=0: #filters that only those existing track IDs would be processed
                        for popper in processing:
                            if popper[1] not in pop_list:
                                new.append(popper)
                        if len(new)!=0:
                            global_pcentroid,global_wcentroid=ParticleFilter(new,global_pcentroid,global_wcentroid,1) #process Particle Filter per keypoint of the previous_processing_length
                            global_pkeypoint9,global_wkeypoint9=ParticleFilter(new,global_pkeypoint9,global_wkeypoint9,2)
                            global_pkeypoint10,global_wkeypoint10=ParticleFilter(new,global_pkeypoint10,global_wkeypoint10,3)
                            new=[]
                            processing=[]
                            processing.append(sorted[i])
                            frame_track=frame_track+1
                        else:
                            processing=[]
                            processing.append(sorted[i])
                            frame_track=frame_track+1
                else: #this means all track IDs have existing global particles 
                        global_pcentroid,global_wcentroid=ParticleFilter(processing,global_pcentroid,global_wcentroid,1) #process Particle Filter per keypoint of the previous_processing_length
                        global_pkeypoint9,global_wkeypoint9=ParticleFilter(processing,global_pkeypoint9,global_wkeypoint9,2)
                        global_pkeypoint10,global_wkeypoint10=ParticleFilter(processing,global_pkeypoint10,global_wkeypoint10,3)
                        processing=[]
                        processing.append(sorted[i])
                        frame_track=frame_track+1

                     
    return global_pcentroid,global_pkeypoint9,global_pkeypoint10
 