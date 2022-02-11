import streamlit as st
import mediapipe as mp
import cv2
import time

from angles_calculation import calculate_lm_angle, bicep_curl_counter, overhead_press_counter, lateral_raise_counter
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

st.sidebar.title('Settings')
app_mode = st.sidebar.selectbox('Choose the Exercise', ['Bicep Curl', 'Overhead Press', 'Lateral Raise'])

# tab for tracking bicep curl
if app_mode == 'Bicep Curl':
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
    st.sidebar.markdown('---')

    detection_confidence = st.sidebar.slider('Min Detection Confidence', min_value=0.0, max_value=1.0, value=0.5)
    tracking_confidence = st.sidebar.slider('Min Tracking Confidence', min_value=0.0, max_value=1.0, value=0.5)
    st.sidebar.markdown('---')

    show_angle = st.sidebar.checkbox("Show angles", value=True)
    show_skeleton = st.sidebar.checkbox("Show skeleton", value=True)
    st.sidebar.markdown('---')

    st.title('Bicep Curl')
    kpi1, kpi2 = st.columns(2)
    stframe = st.empty()
    st.markdown("<hr/>", unsafe_allow_html=True)

    vid = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

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

    with mp_pose.Pose(min_detection_confidence=detection_confidence,
                      min_tracking_confidence=tracking_confidence) as pose:
        prevTime = 0

        while vid.isOpened():
            ret, frame = vid.read()

            # recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # make detection
            results = pose.process(image)

            # recolor image to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # detect bicep curl
                angle_left_elbow = calculate_lm_angle(image, mp_pose, landmarks, 'LEFT_SHOULDER', 'LEFT_ELBOW'
                                                      , 'LEFT_WRIST', show_angle)
                angle_right_elbow = calculate_lm_angle(image, mp_pose, landmarks, 'RIGHT_SHOULDER', 'RIGHT_ELBOW',
                                                       'RIGHT_WRIST', show_angle)
                counter, stage = bicep_curl_counter(counter, stage, angle_left_elbow, angle_right_elbow)

            except:
                pass

            # render detections
            if show_skeleton:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )

            # FPS counter logic
            currTime = time.time()
            fps = 1 / (currTime - prevTime)
            prevTime = currTime

            # resize image
            image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)
            image = image_resize(image=image, width=640)
            stframe.image(image, channels='BGR', use_column_width=True)

            # create dashboard
            kpi1_text.write(f"<h1 style='text-align: center; color: red;'>{int(fps)}</h1>", unsafe_allow_html=True)
            kpi2_text.write(f"<h1 style='text-align: center; color: red;'>{counter}</h1>", unsafe_allow_html=True)

    vid.release()

# tab to tracking overhead press
elif app_mode == 'Overhead Press':
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
    st.sidebar.markdown('---')

    detection_confidence = st.sidebar.slider('Min Detection Confidence', min_value=0.0, max_value=1.0, value=0.5)
    tracking_confidence = st.sidebar.slider('Min Tracking Confidence', min_value=0.0, max_value=1.0, value=0.5)
    st.sidebar.markdown('---')

    show_angle = st.sidebar.checkbox("Show angles", value=True)
    show_skeleton = st.sidebar.checkbox("Show skeleton", value=True)
    st.sidebar.markdown('---')

    st.title('Overhead Press')
    kpi1, kpi2 = st.columns(2)
    stframe = st.empty()
    st.markdown("<hr/>", unsafe_allow_html=True)

    vid = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

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

    with mp_pose.Pose(min_detection_confidence=detection_confidence,
                      min_tracking_confidence=tracking_confidence) as pose:
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

                # detect overhead press
                angle_left_shoulder = calculate_lm_angle(image, mp_pose, landmarks, 'LEFT_HIP', 'LEFT_SHOULDER',
                                                         'LEFT_ELBOW', show_angle)
                angle_right_shoulder = calculate_lm_angle(image, mp_pose, landmarks, 'RIGHT_HIP', 'RIGHT_SHOULDER',
                                                          'RIGHT_ELBOW', show_angle)

                angle_left_elbow = calculate_lm_angle(image, mp_pose, landmarks, 'LEFT_SHOULDER', 'LEFT_ELBOW',
                                                      'LEFT_WRIST', show_angle)
                angle_right_elbow = calculate_lm_angle(image, mp_pose, landmarks, 'RIGHT_SHOULDER', 'RIGHT_ELBOW',
                                                       'RIGHT_WRIST', show_angle)

                counter, stage = overhead_press_counter(counter, stage, angle_left_shoulder, angle_right_shoulder,
                                                        angle_left_elbow, angle_right_elbow)

            except:
                pass

            # render detections
            if show_skeleton:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )

            # FPS counter logic
            currTime = time.time()
            fps = 1 / (currTime - prevTime)
            prevTime = currTime

            # resize image
            image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)
            image = image_resize(image=image, width=640)
            stframe.image(image, channels='BGR', use_column_width=True)

            # create dashboard
            kpi1_text.write(f"<h1 style='text-align: center; color: red;'>{int(fps)}</h1>", unsafe_allow_html=True)
            kpi2_text.write(f"<h1 style='text-align: center; color: red;'>{counter}</h1>", unsafe_allow_html=True)

    vid.release()

# tab for tracking lateral raise
elif app_mode == 'Lateral Raise':
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)
    st.sidebar.markdown('---')

    detection_confidence = st.sidebar.slider('Min Detection Confidence', min_value=0.0, max_value=1.0, value=0.5)
    tracking_confidence = st.sidebar.slider('Min Tracking Confidence', min_value=0.0, max_value=1.0, value=0.5)
    st.sidebar.markdown('---')

    show_angle = st.sidebar.checkbox("Show angles", value=True)
    show_skeleton = st.sidebar.checkbox("Show skeleton", value=True)
    st.sidebar.markdown('---')

    st.title('Lateral Raise')
    kpi1, kpi2 = st.columns(2)
    stframe = st.empty()
    st.markdown("<hr/>", unsafe_allow_html=True)

    vid = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

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

    with mp_pose.Pose(min_detection_confidence=detection_confidence,
                      min_tracking_confidence=tracking_confidence) as pose:
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

                # detect lateral raise
                angle_left_shoulder = calculate_lm_angle(image, mp_pose, landmarks, 'LEFT_HIP', 'LEFT_SHOULDER',
                                                         'LEFT_ELBOW', show_angle)
                angle_right_shoulder = calculate_lm_angle(image, mp_pose, landmarks, 'RIGHT_HIP', 'RIGHT_SHOULDER',
                                                          'RIGHT_ELBOW', show_angle)

                counter, stage = lateral_raise_counter(counter, stage, angle_left_shoulder, angle_right_shoulder)

            except:
                pass

            # render detections
            if show_skeleton:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )

            # FPS counter logic
            currTime = time.time()
            fps = 1 / (currTime - prevTime)
            prevTime = currTime

            # resize image
            image = cv2.resize(image, (0, 0), fx=0.8, fy=0.8)
            image = image_resize(image=image, width=640)
            stframe.image(image, channels='BGR', use_column_width=True)

            # create dashboard
            kpi1_text.write(f"<h1 style='text-align: center; color: red;'>{int(fps)}</h1>", unsafe_allow_html=True)
            kpi2_text.write(f"<h1 style='text-align: center; color: red;'>{counter}</h1>", unsafe_allow_html=True)

    vid.release()

