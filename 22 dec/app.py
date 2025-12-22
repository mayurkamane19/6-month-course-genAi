import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time

# =========================
# Page Config
# =========================
st.set_page_config(page_title="Advanced Image Processing App", layout="wide")
st.title("🧠 Advanced Image Processing App")

# =========================
# IMAGE UPLOAD
# =========================
uploaded = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded is not None:
    image = Image.open(uploaded)
    img = np.array(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(image, use_column_width=True)

    # =========================
    # SIDEBAR CONTROLS
    # =========================
    st.sidebar.header("🎛 Controls")

    filter_type = st.sidebar.selectbox(
        "Choose Filter",
        ["None", "Grayscale", "Sepia", "Cartoon", "Edge Detection"]
    )

    blur_k = st.sidebar.slider("Blur", 1, 31, 5, step=2)
    brightness = st.sidebar.slider("Brightness", -100, 100, 0)
    contrast = st.sidebar.slider("Contrast", 50, 300, 100)

    # =========================
    # FILTER LOGIC
    # =========================
    result = img.copy()

    if filter_type == "Grayscale":
        result = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)

    elif filter_type == "Sepia":
        kernel = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ])
        result = cv2.transform(result, kernel)
        result = np.clip(result, 0, 255).astype(np.uint8)

    elif filter_type == "Cartoon":
        gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
        blur = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(
            blur, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 9, 9
        )
        color = cv2.bilateralFilter(result, 9, 300, 300)
        result = cv2.bitwise_and(color, color, mask=edges)

    elif filter_type == "Edge Detection":
        gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
        result = cv2.Canny(gray, 50, 150)

    # =========================
    # BRIGHTNESS / CONTRAST
    # =========================
    if len(result.shape) == 2:
        result = cv2.convertScaleAbs(
            result, alpha=contrast / 100, beta=brightness
        )
        result_rgb = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    else:
        result_rgb = cv2.convertScaleAbs(
            result, alpha=contrast / 100, beta=brightness
        )

    # =========================
    # BLUR
    # =========================
    result_rgb = cv2.GaussianBlur(
        result_rgb, (blur_k, blur_k), 0
    )

    with col2:
        st.subheader("Processed Image")
        st.image(result_rgb, use_column_width=True)

    # =========================
    # IMAGE COMPARISON SLIDER
    # =========================
    st.subheader("🔀 Image Comparison Slider")

    slider = st.slider(
        "Slide to compare",
        0,
        img.shape[1],
        img.shape[1] // 2
    )

    comparison = img.copy()
    comparison[:, :slider] = result_rgb[:, :slider]

    st.image(comparison, use_column_width=True)

    # =========================
    # DOWNLOAD
    # =========================
    st.subheader("⬇️ Download Processed Image")

    result_pil = Image.fromarray(result_rgb)
    st.download_button(
        label="Download Image",
        data=result_pil.tobytes(),
        file_name="processed_image.png",
        mime="image/png"
    )

# =========================
# WEBCAM LIVE EDGE DETECTION
# =========================
st.subheader("📷 Webcam Live Edge Detection")

run_cam = st.checkbox("Start Webcam")

if run_cam:
    cam = cv2.VideoCapture(0)
    frame_box = st.empty()

    while run_cam:
        ret, frame = cam.read()
        if not ret:
            st.error("Webcam not accessible")
            break

        edges = cv2.Canny(frame, 100, 200)
        frame_box.image(edges, channels="GRAY")
        time.sleep(0.03)

    cam.release()
