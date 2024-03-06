#Particle Filter

import numpy as np
from numpy.random import randn
import scipy as scipy
import scipy.stats
from filterpy.monte_carlo import systematic_resample


def classifier(keypoint_classifier): #Classifies the ParticleFilter according to state
    if keypoint_classifier==1: #Particle Filter for Centroid 
        x= 6
        y= 7
    elif keypoint_classifier==2: #Particle Filter Keypoint 9
        x=8
        y=9
    elif keypoint_classifier==3: #Particle Filter Keypoint 10
        x=10
        y=11
    else: #If entered the wrong classifier 
        x=0
        y=0
    
    return x,y 


def predict(particles,u,std): #move your particles set std muna to 1, pero the std will come from vision sub system
     particle_length=len(particles)
     distance= (u[1]*1.)+(randn(particle_length)*std)
     particles[:,0] += distance
     particles[:,1] += distance
     return particles

def update(particles,weights,track_ID_to_landmarks,camera_std, landmarks):

    for u_iterate, landmark in enumerate(landmarks):
          distance= np.linalg.norm(particles[:,0:1]-landmark,axis=1)
          weights *= scipy.stats.norm(distance,camera_std).pdf(track_ID_to_landmarks[u_iterate])
    
    weights += 1.e-300 #no zero conditions
    weights /=sum(weights) #normalization 
    return weights
         
def neff(weights):
     return 1. / np.sum(np.square(weights))

def resample_from_index(particles, weights, indexes): #Importance Resampling- prioritize those particles with higher weights
    particles[:] = particles[indexes]
    weights[:] = weights[indexes]
    weights.fill(1.0 / len(weights))

def estimate(particles,weights):
    pos = particles[:, 0:1]
    mean = np.average(pos, weights=weights, axis=0)
    var  = np.average((pos - mean)**2, weights=weights, axis=0)
    return mean, var

def ParticleFilter(processing,global_particles,global_weights,keypoint_classifier): #processing= data; initial_state= which state we are tracking
    std=115.1560000514251 #abritrary muna gawa ng may gagawing code sa vision
    for i in range(len(processing)):
        # landmarks=np.array([[344,76],[341,117],[334,156],[347,216],[343,254],[343,297],[259,69],[249,98],[248,139],[257,215],[256,241],[257,285]]) # coordinates of the centroid of each weight bin- 30 minute Intervals
        landmarks=np.array([[382,64],[382,100],[381,133],[377,199],[376,235],[376,274],[279,55],[278,86],[275,121],[289,202],[287,231],[286,271]]) # coordinates of the centroid of each weight bin- CCTV continous
        landmarks_length=len(landmarks)
        x,y=classifier(keypoint_classifier)
        TrackID=processing[i][1] #ensures that the proper TrackID is extracted
        for trackID_matcher in range(len(global_particles)):
            if TrackID== global_particles[trackID_matcher][0]: #matches the right particles of the previous weights based on TrackID
                particles=global_particles[trackID_matcher][1]
                particle_no=len(particles)
            else:
                continue
        for trackID_matcher2 in range(len(global_weights)):
            if TrackID== global_weights[trackID_matcher2][0]: #matches the right particles of the previous weights based on TrackID
                weights=global_weights[trackID_matcher2][1]
            else:
                continue    
        current_pos= [processing[i][x],processing[i][y]]
        dist_to_landmarks=(np.linalg.norm(landmarks-current_pos,axis=1))+((np.random.randn(landmarks_length))*(std))

        particles=predict(particles,u=(0.00,1.414),std=115.1560000514251) #1.414 moving each points diagonally (Pythagorean)
        weights=update(particles,weights,dist_to_landmarks,camera_std=115.1560000514251,landmarks=landmarks) #updates the particles 
        if neff(weights) < particle_no/2: #systemic resampling 
            indexes = systematic_resample(weights)
            resample_from_index(particles, weights, indexes)
            assert np.allclose(weights, 1/particle_no)
        # mu, var = estimate(particles, weights)
        for particle_update in range(len(global_particles)): #updates the new particles 
            if TrackID== global_particles[particle_update][0]:
                global_particles[particle_update][1]=particles
            else:
                continue
        for weight_update in range(len(global_weights)): #updates the new weights 
            if TrackID== global_weights[weight_update][0]:
                global_weights[weight_update][1]=weights
   
    return global_particles, global_weights