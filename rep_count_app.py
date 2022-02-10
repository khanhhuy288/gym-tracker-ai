import streamlit as st
import mediapipe as mp
import cv2
import numpy as np
import tempfile
import time
from PIL import Image

from angles_calculation import calculate_lm_angle, bicep_curl_counter
from helpers import image_resize

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

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

    st.title('Bicep Curl')
    # st.markdown('## Bicep Curl')
    kpi1, kpi2 = st.columns(2)
    stframe = st.empty()
    st.markdown("<hr/>", unsafe_allow_html=True)

    vid = cv2.VideoCapture(0)

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_input = int(vid.get(cv2.CAP_PROP_FPS))

    with kpi1:
        st.markdown('**Frame Rate**')
        kpi1_text = st.markdown('0')

    with kpi2:
        st.markdown('**Reps**')
        kpi2_text = st.markdown('0')

    # counter variables
    counter = 0
    stage = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        prevTime = 0

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

            # extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                angle_left_elbow = calculate_lm_angle(image, mp_pose, landmarks, 'LEFT_SHOULDER', 'LEFT_ELBOW'
                                                      , 'LEFT_WRIST')
                angle_right_elbow = calculate_lm_angle(image, mp_pose, landmarks, 'RIGHT_SHOULDER', 'RIGHT_ELBOW',
                                                       'RIGHT_WRIST')
                counter, stage = bicep_curl_counter(counter, stage, angle_left_elbow, angle_right_elbow)

            except:
                pass

            # render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            # FPS counter logic
            currTime = time.time()
            fps = 1 / (currTime - prevTime)
            prevTime = currTime

            image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)
            image = image_resize(image=image, width=640)
            stframe.image(image, channels='BGR', use_column_width=True)

            # create dashboard
            kpi1_text.write(f"<h1 style='text-align: center; color: red;'>{int(fps)}</h1>", unsafe_allow_html=True)
            kpi2_text.write(f"<h1 style='text-align: center; color: red;'>{counter}</h1>", unsafe_allow_html=True)

    vid.release()

elif app_mode == 'Overhead Press':
    pass
elif app_mode == 'Lateral Raise':
    pass
