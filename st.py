import streamlit as st
from PIL import Image
import numpy as np
import cv2
import json

def load_image(image_file):
    img = Image.open(image_file)
    return img

def get_array(inp):
    return np.array(inp)

def filter2d(inp, x):
    kernel = np.ones((5,5),np.float32) * x
    dst = cv2.filter2D(inp, -1, kernel)
    return dst

def canny_thresh(inp, thresh1, thresh2):
    inp = np.uint8(inp) * 255
    out = cv2.Canny(inp, threshold1=thresh1, threshold2=thresh2)
    return out / 255

def thresh(inp, option, thresh1, thresh2):
    funcs = ["cv2.THRESH_BINARY", "cv2.THRESH_BINARY_INV",
             "cv2.THRESH_TRUNC", "cv2.THRESH_TOZERO", "cv2.THRESH_TOZERO_INV"]
    names = ["Binary", "Binary Inverse", "Trunc", "Tozero Inverse", 
             "Tozero Inverse"]
    for n, f in zip(names, funcs):
        if option == n:
            f_used = eval(f)
            break
    thresh1 = thresh1 / 255
    thresh2 = thresh2 / 255
    ret, out = cv2.threshold(inp, thresh1, thresh2, f_used)
    return out

def main():
    st.title("OpenCV Simulator")

    with open("md.json", "rb") as outfile:
        md = json.load(outfile)
    
    with open("code.json", "rb") as outfile:
        code = json.load(outfile)

    image_file = st.file_uploader("Image Uploader", type=['png', 'jpg', 'jpeg'])

    if image_file is not None:
        img = load_image(image_file)
        inp = get_array(img)
    
        st.text("This is the original picture")
        st.image(img, width=700)

    choice = st.sidebar.selectbox("Select Functions",
                                    ("None", "Gamma Correction", "Low Pass Filter", "Threshold",
                                     "Canny Threshold"))
    
    if (choice == "Gamma Correction") & (image_file is not None):
        with st.form(key="form1"):
            with st.sidebar:
                st.header('Input the Gamma Correction')
                gamma = st.slider('Gamma Correction', 0.0, 1.0, 4.0)
                button = st.form_submit_button(label='Submit')
        inp = np.power((inp / 255), gamma)
        out = Image.fromarray(np.uint8(inp * 255)).convert('RGB')
        
    elif (choice == "Low Pass Filter") & (image_file is not None):
        with st.form(key="form1"):
            with st.sidebar:
                st.header('Input the Low Pass Filter Constant')
                lpf = st.slider('Low Pass Filter Constant', 0.0, 0.5, 1.0) 
                button = st.form_submit_button(label='Submit')
        inp = filter2d(inp, lpf)
        out = Image.fromarray(np.uint8(inp * 255)).convert('RGB')

    elif (choice == "Threshold") & (image_file is not None):
        with st.form(key="form1"):
            with st.sidebar:
                st.header('Input Threshold')
                option = st.selectbox('Threshold Type', 
                                      ("Binary", "Binary Inverse", "Trunc", 
                                       "Tozero Inverse", "Tozero Inverse"))                           
                t1_t = st.slider('Threshold 1', 0, 80, 250)
                t2_t = st.slider('Threshold 2', 0, 80, 250)
                button = st.form_submit_button(label='Submit')
        inp = thresh(inp, option, t1_t, t2_t)
        out = Image.fromarray(np.uint8(inp * 255)).convert('RGB')

    elif (choice == "Canny Threshold") & (image_file is not None):
        with st.form(key="form1"):
            with st.sidebar:
                st.header('Input Canny Threshold')
                t1_c = st.slider('Threshold_1', 0, 80, 250)
                t2_c = st.slider('Threshold_2', 0, 80, 250) 
                button = st.form_submit_button(label='Submit')
        inp = canny_thresh(inp, t1_c, t2_c)
        out = Image.fromarray(np.uint8(inp * 255)).convert('RGB')
        
    else:
        out = None

    if out is not None:
        st.text("This is the corrected picture")
        st.image(out, width=700)
        st.markdown(md[choice])
        st.code(code[choice])

if __name__ == "__main__":
    main()
