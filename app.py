import streamlit as st
from PIL import Image
import numpy as np
import cv2
import json

with open("assets/md.json", "rb") as outfile:
    md = json.load(outfile)
    
with open("assets/code.json", "rb") as outfile:
    code = json.load(outfile)

def load_image(image_file):
    img = Image.open(image_file)
    return img

def get_array(inp):
    return np.array(inp)

def gamma_corr(inp, x):
    out = np.power(inp * 255, x)
    return out / 255

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
    names = ["Binary", "Binary Inverse", "Trunc", "Tozero", 
             "Tozero Inverse"]
    for n, f in zip(names, funcs):
        if option == n:
            f_used = eval(f)
            break
    thresh1 = thresh1 / 255
    thresh2 = thresh2 / 255
    ret, out = cv2.threshold(inp, thresh1, thresh2, f_used)
    return out

def generate_output(choice, params, inp):
    if choice == "Gamma Correction":
        inp = gamma_corr(inp, params[0])
        out = Image.fromarray(np.uint8(inp * 255)).convert('RGB')
        
    elif choice == "Low Pass Filter":
        inp = filter2d(inp, params[0])
        out = Image.fromarray(np.uint8(inp * 255)).convert('RGB')

    elif choice == "Threshold":
        inp = thresh(inp, params[0], params[1], params[2])
        out = Image.fromarray(np.uint8(inp * 255)).convert('RGB')

    elif choice == "Canny Threshold":
        inp = canny_thresh(inp, params[0], params[1])
        out = Image.fromarray(np.uint8(inp * 255)).convert('RGB')
        
    else:
        out = Image.fromarray(np.uint8(inp * 255)).convert('RGB')

    return out

def get_params(choice):
    if choice == "Gamma Correction":
        st.sidebar.header('Input the Gamma Correction')
        gamma = st.sidebar.slider('Gamma Correction', 0.0, 1.0, 4.0)
        params = [gamma]
        
    elif choice == "Low Pass Filter":
        st.sidebar.header('Input the Low Pass Filter Constant')
        lpf = st.sidebar.slider('Low Pass Filter Constant', 0.0, 0.5, 1.0) 
        params = [lpf]

    elif choice == "Threshold":
        st.sidebar.header('Input Threshold')
        option = st.sidebar.selectbox('Threshold Type', 
                                      ("Binary", "Binary Inverse", "Trunc", 
                                       "Tozero", "Tozero Inverse"))                           
        t1_t = st.sidebar.slider('Threshold 1', 0, 80, 250)
        t2_t = st.sidebar.slider('Threshold 2', 0, 80, 250)
        params = [option, t1_t, t2_t]

    elif choice == "Canny Threshold":
        st.sidebar.header('Input Canny Threshold')
        t1_c = st.sidebar.slider('Threshold_1', 0, 80, 250)
        t2_c = st.sidebar.slider('Threshold_2', 0, 80, 250) 
        params = [t1_c, t2_c]

    else:
        params = None

    return params

def main():
    st.title("OpenCV Simulator")

    image_file = None
    inp = None
    out = None

    # input_choice = st.sidebar.selectbox("Select Input", ("Upload Picture", "Webcam"))
    input_choice = "Upload Picture"

    gray = st.sidebar.checkbox('Convert Input to Black & White')

    col1, col2 = st.columns(2)
    
    if input_choice == "Upload Picture":
        image_file = st.sidebar.file_uploader("Image Uploader", 
                                              type=['png', 'jpg', 'jpeg'])
        if image_file is not None:
            img = load_image(image_file)
            inp = get_array(img) / 255
            col1.text("This is the original picture")
            col1.image(img, width=300)
        vid = False

    # else:
    #     camera = cv2.VideoCapture(0)
    #     col1.text("This is the original picture")
    #     frame_in = col1.image([], width=500)
    #     col2.text("This is the edited picture")
    #     frame_out = col2.image([], width=500)
    #     vid = True

    choice = st.sidebar.selectbox("Select Functions",
                                    ("None", "Gamma Correction", "Low Pass Filter", "Threshold",
                                     "Canny Threshold"))
    params = get_params(choice)

    while vid:
        _, inp = camera.read()
        inp = cv2.cvtColor(inp, cv2.COLOR_BGR2RGB) / 255
        img = Image.fromarray(np.uint8(inp * 255))
        frame_in.image(img)
        if gray:
            inp = cv2.cvtColor(np.uint8(inp * 255), cv2.COLOR_RGB2GRAY) / 255
        out = generate_output(choice, params, inp)
        frame_out.image(out)


    if choice != "None":
        st.markdown(md[choice])
        if choice == "Low Pass Filter":
            kernel_img = Image.open('assets/kernel.gif')
            st.write("![Your Awsome GIF](https://media3.giphy.com/media/PUmwonv8z3yAwXImkB/giphy.gif?cid=790b7611c1b063dc686f8ccb5f453f102787993275597f14&rid=giphy.gif&ct=g)")
        st.markdown("# Code")
        st.code(code[choice])

    if inp is not None:
        if gray:
            img = cv2.cvtColor(np.uint8(inp * 255), cv2.COLOR_RGB2GRAY)
            inp = get_array(img) / 255
        out = generate_output(choice, params, inp)
        
    if out is not None:
        col2.text("This is the edited picture")
        col2.image(out, width=300)
        
if __name__ == "__main__":
    main()
