import streamlit as st
import cv2
import face_recognition
from encoding_generator import generate_encodings
import os
import numpy as np
import cvzone

def run_security():
    #import images
    img_path = '../verified_images'
    path_list = [f for f in os.listdir(img_path) if not f.startswith('.')]
    img_list = []
    id_list = []
    for img in path_list:
        img_list.append(cv2.imread(os.path.join(img_path,img)))
        id_list.append(os.path.splitext(img)[0])

    print(id_list)
    encode_list = generate_encodings(img_list)
    
    #OpenCV
    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()
    
    while True: 
        ret, frame = cap.read()

        #resize original frame to 1/4 of size
        img_scaled = cv2.resize(frame, (0,0), None, 0.25, 0.25)
        img_scaled = cv2.cvtColor(img_scaled, cv2.COLOR_BGR2RGB)
        
        #find face locations and encodings in the current frame
        current_face = face_recognition.face_locations(img_scaled)
        current_encodings = face_recognition.face_encodings(img_scaled, current_face)
        
        
        #compare current encodings with verified encodings
        for encode_face, face_loc in zip(current_encodings, current_face):
            matches = face_recognition.compare_faces(encode_list, encode_face)
            face_distance = face_recognition.face_distance(encode_list, encode_face)
            #index of the image with the lowest distance which is the best match
            match_index = np.argmin(face_distance)

            #if there is a known face match
            if matches[match_index] == True:
                top,right,bottom,left = face_loc
                top,right,bottom,left = top*4,right*4,bottom*4,left*4
                frame = cv2.rectangle(frame, (left,top), (right,bottom), (0,255,0),3)
                
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame, channels='RGB')

    cap.release()
    cv2.destroyAllWindows()