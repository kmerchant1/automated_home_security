import streamlit as st
import cv2
import face_recognition
from security import run_security
import pickle

#sidebar component
with st.sidebar:
    st.title('Automated Home Security')
    choice = st.radio('Navigation',['Live Feed',
                                    'Verified People',
                                    'Config'])

if choice == 'Live Feed':
    
    
    view = st.checkbox('Activate Security')
    st.write(view)
    
    #load encoded file
    file = open('../resources/verified_file.p', 'rb')
    encode_list_with_id = pickle.load(file)
    file.close()
    known_encode, id_list = encode_list_with_id
    #print(id_list)
    if view:
        run_security()
    else:
        pass



