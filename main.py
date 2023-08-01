import streamlit as st
import cv2

from live_feed_streamlit import run_live_feed


#sidebar component
with st.sidebar:
    st.title('Automated Home Security')
    choice = st.radio('Navigation',['Live Feed',
                                    'Verified People',
                                    'Config'])

if choice == 'Live Feed':
    
    view = st.checkbox('View Security Feed')
    st.write(view)
    if view:
        run_live_feed()
    else:
        pass



