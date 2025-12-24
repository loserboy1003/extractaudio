import streamlit as st
import moviepy as mp  # New way to import
import tempfile
import os

# Page Config
st.set_page_config(page_title="Video Audio Tool", page_icon="🎬")

st.title("🎬 Simple Video Maker")
st.write("Extract audio from a video and put it on a photo.")

# Step 1: Uploads
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Pick your Video")
    uploaded_video = st.file_uploader("Upload video for sound", type=["mp4", "mov", "avi"])

with col2:
    st.subheader("2. Pick your Photo")
    uploaded_image = st.file_uploader("Upload background photo", type=["jpg", "jpeg", "png"])

# Step 2: Action
if st.button("✨ Create My New Video ✨"):
    if uploaded_video and uploaded_image:
        status = st.empty()
        bar = st.progress(0)
        
        try:
            # Create temp files
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_vid:
                t_vid.write(uploaded_video.read())
                v_path = t_vid.name
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as t_img:
                t_img.write(uploaded_image.read())
                i_path = t_img.name

            status.text("Working on your video...")
            bar.progress(50)

            # --- PROCESS WITH MOVIEPY 2.0 SYNTAX ---
            video_clip = mp.VideoFileClip(v_path)
            audio = video_clip.audio
            
            img_clip = mp.ImageClip(i_path).with_duration(audio.duration) # .with_duration is the new way
            final_video = img_clip.with_audio(audio)
            
            out_file = "final_creation.mp4"
            # Setting fps to 24 and using a common codec
            final_video.write_videofile(out_file, fps=24, codec="libx264", audio_codec="aac")
            
            bar.progress(100)
            status.success("Done! See your video below.")

            # Display and Download
            st.video(out_file)
            with open(out_file, "rb") as f:
                st.download_button("📥 Save Video to Phone/PC", f, file_name="my_video.mp4")

            # Clean up files
            video_clip.close()
            final_video.close()
            os.remove(v_path)
            os.remove(i_path)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload both files first!")
