import streamlit as st
import mediapipe as mp
import cv2
import numpy as np
import tempfile
import time
from PIL import Image

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

st.title('Rep Count App using MediaPipe')

st.markdown(
    """
        <style>
        [data-testid=stSidebar][arial-expanded='true'] > div:first-child{
            width: 350px 
        }
        [data-testid=stSidebar][arial-expanded='false'] > div:first-child{
            width: 350px 
            margin-left : -350px
        }
        </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title('Rep Count Sidebar')
st.sidebar.subheader('Parameters')

app_mode = st.sidebar.selectbox('Choose the Exercise',
                                ['Bicep Curl', 'Overhead Press', 'Lateral Raise'])

if app_mode == 'Bicep Curl':
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)

    st.sidebar.markdown('---')

    st.markdown(
        """
            <style>
            [data-testid=stSidebar][arial-expanded='true'] > div:first-child{
                width: 350px 
            }
            [data-testid=stSidebar][arial-expanded='false'] > div:first-child{
                width: 350px 
                margin-left : -350px
            }
            </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('## Output')
    stframe = st.empty()

    vid = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while vid.isOpened():
            ret, frame = vid.read()

            # recolor image
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # make detection
            results = pose.process(image)

            # recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            stframe.image(image, channels='BGR', use_column_width=True)

    vid.release()

elif app_mode == 'Overhead Press':
    pass
elif app_mode == 'Lateral Raise':
    pass
