import streamlit as st
import moviepy as mp
import tempfile
import os

st.set_page_config(page_title="mixer", page_icon="🎬", layout="centered")

# ultra-minimal glassmorphism UI
st.markdown("""
    <style>
    /* hide streamlit elements */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    /* force lowercase everywhere */
    * { text-transform: lowercase !important; font-family: 'Inter', sans-serif; }

    /* container styling */
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    .label-icon { font-size: 24px; margin-bottom: 10px; display: block; }
    
    /* minimal button */
    div.stButton > button {
        background-color: transparent;
        color: #fff;
        border: 1px solid #444;
        border-radius: 10px;
        padding: 10px 25px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        border-color: #fff;
        background: rgba(255,255,255,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 mixer")

# 🎥 video card
st.markdown('<div class="main-card"><span class="label-icon">🎥</span>video (audio)</div>', unsafe_allow_html=True)
v_file = st.file_uploader("video", type=["mp4", "mov", "avi"], label_visibility="collapsed")

# 🖼️ photo card
st.markdown('<div class="main-card"><span class="label-icon">🖼️</span>photo(s)</div>', unsafe_allow_html=True)
img_files = st.file_uploader("photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")

st.write(" ")

# centered start button
col1, col2, col3 = st.columns([1,1,1])
with col2:
    start_btn = st.button("start")

if start_btn:
    if v_file and img_files:
        status = st.empty()
        bar = st.progress(0)
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_vid:
                t_vid.write(v_file.read())
                v_path = t_vid.name

            status.text("working...")
            
            video_clip = mp.VideoFileClip(v_path)
            audio = video_clip.audio
            total_duration = audio.duration
            
            num_photos = len(img_files)
            duration_per_photo = total_duration / num_photos
            
            clips = []
            for img_file in img_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as t_img:
                    t_img.write(img_file.read())
                    i_path = t_img.name
                
                # smooth fade between images
                clip = (mp.ImageClip(i_path)
                        .with_duration(duration_per_photo)
                        .with_effects([mp.vfx.CrossFadeIn(0.5)]))
                clips.append(clip)

            final_slideshow = mp.concatenate_videoclips(clips, method="compose")
            final_video = final_slideshow.with_audio(audio)
            
            out_file = "output.mp4"
            final_video.write_videofile(out_file, fps=24, codec="libx264", audio_codec="aac")
            
            bar.progress(100)
            status.text("ready!")
            
            st.video(out_file)
            
            st.download_button("save", open(out_file, "rb"), file_name="video.mp4")

            # cleanup
            video_clip.close()
            final_video.close()
            os.remove(v_path)

        except Exception as e:
            st.text("error occurred")
    else:
        st.text("upload files first")
