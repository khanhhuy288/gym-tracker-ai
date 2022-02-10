import numpy as np
import cv2
import streamlit as st


@st.cache()
def calculate_angle(a, b, c):
    a = np.array(a)  # first
    b = np.array(b)  # mid
    c = np.array(c)  # end

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


# calculate landmark angle
def calculate_lm_angle(image, mp_pose, landmarks, lm_1, lm_2, lm_3, show_angle=True):
    # get coordinates
    lm_coord_1 = [landmarks[mp_pose.PoseLandmark[lm_1].value].x, landmarks[mp_pose.PoseLandmark[lm_1].value].y]
    lm_coord_2 = [landmarks[mp_pose.PoseLandmark[lm_2].value].x, landmarks[mp_pose.PoseLandmark[lm_2].value].y]
    lm_coord_3 = [landmarks[mp_pose.PoseLandmark[lm_3].value].x, landmarks[mp_pose.PoseLandmark[lm_3].value].y]

    angle = calculate_angle(lm_coord_1, lm_coord_2, lm_coord_3)

    # visualize angle
    if show_angle:
        cv2.putText(image, str(angle),
                    tuple(np.multiply(lm_coord_2, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    return angle


@st.cache()
# count bicep curl
def bicep_curl_counter(counter, stage, angle_left_elbow, angle_right_elbow):
    if angle_left_elbow > 160 and angle_right_elbow > 160:
        stage = 'down'
    if angle_left_elbow < 30 and angle_right_elbow < 30 and stage == 'down':
        stage = 'up'
        counter += 1

    return counter, stage


@st.cache()
# count overhead press
def overhead_press_counter(counter, stage, angle_left_shoulder, angle_right_shoulder, angle_left_elbow,
                           angle_right_elbow):
    if angle_left_shoulder < 30 and angle_right_shoulder < 30 \
            and angle_left_elbow < 30 and angle_right_elbow < 30:
        stage = 'down'

    if angle_left_shoulder > 160 and angle_right_shoulder > 160 \
            and angle_left_elbow > 160 and angle_right_elbow > 160 and stage == 'down':
        stage = 'up'
        counter += 1

    return counter, stage


@st.cache()
# count lateral raise
def lateral_raise_counter(counter, stage, angle_left_shoulder, angle_right_shoulder):
    if angle_left_shoulder < 20 and angle_right_shoulder < 20:
        stage = 'down'
    if angle_left_shoulder > 80 and angle_right_shoulder > 80 and stage == 'down':
        stage = 'up'
        counter += 1

    return counter, stage


@st.cache()
def render_rep_data(image, counter, stage):
    # setup status box
    cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)

    # rep data
    cv2.putText(image, 'REPS', (15, 12), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 255, 255), 2, cv2.LINE_AA)

    # stage data
    cv2.putText(image, 'STAGE', (65, 12), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, stage, (60, 60), cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 255, 255), 2, cv2.LINE_AA)
