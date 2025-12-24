import streamlit as st
from moviepy.editor import VideoFileClip, ImageClip
import tempfile
import os

# Page Config
st.set_page_config(page_title="Video Audio Tool", page_icon="🎬")

# Simple Styling
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Simple Video Maker")
st.write("Follow these two steps to put your music/audio onto a photo!")

# Step 1: Uploads
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Pick your Video")
    uploaded_video = st.file_uploader("The video with the sound you like", type=["mp4", "mov", "avi"])

with col2:
    st.subheader("2. Pick your Photo")
    uploaded_image = st.file_uploader("The photo you want people to see", type=["jpg", "jpeg", "png"])

if uploaded_image:
    st.image(uploaded_image, caption="This photo will be shown", width=300)

# Step 2: Action
if st.button("✨ Create My New Video ✨"):
    if uploaded_video and uploaded_image:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("Reading files...")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_vid:
                t_vid.write(uploaded_video.read())
                v_path = t_vid.name
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as t_img:
                t_img.write(uploaded_image.read())
                i_path = t_img.name

            progress_bar.progress(30)
            status_text.text("Extracting audio and mixing...")

            # Processing
            video_clip = VideoFileClip(v_path)
            audio = video_clip.audio
            
            img_clip = ImageClip(i_path).set_duration(audio.duration)
            final_video = img_clip.set_audio(audio)
            
            out_file = "final_creation.mp4"
            final_video.write_videofile(out_file, fps=24, codec="libx264")
            
            progress_bar.progress(100)
            status_text.text("Done! Look below! 👇")

            # Result
            st.video(out_file)
            with open(out_file, "rb") as f:
                st.download_button("📥 Click here to save to your phone/PC", f, file_name="my_video.mp4")

            # Clean up
            video_clip.close()
            final_video.close()
            os.remove(v_path)
            os.remove(i_path)

        except Exception as e:
            st.error("Something went wrong. Make sure the files aren't too large!")
    else:
        st.warning("Please make sure you have uploaded both a video and a photo first!")
