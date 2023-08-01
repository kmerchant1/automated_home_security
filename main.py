import streamlit as st
import cv2














def run_live_feed():

    cap = cv2.VideoCapture(0)
    frame_placeholder = st.empty()
    stop = st.button('Stop')

    while True:
        if stop:
            break
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame, channels='RGB')

        

    cap.release()
    cv2.destroyAllWindows()