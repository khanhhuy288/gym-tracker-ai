import cv2
import streamlit as st


@st.cache()
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image

    r = width / float(w)
    if width is None:
        dim = (int(w * r), height)
    else:
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    return resized
