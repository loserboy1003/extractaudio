import streamlit as st
import moviepy as mp
import tempfile
import os

st.set_page_config(page_title="mixer", page_icon="🎬", layout="centered")

# ultra-modern mesh gradient UI
st.markdown("""
    <style>
    /* hide everything unnecessary */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    /* mesh gradient background */
    .stApp {
        background-color: #0e1117;
        background-image: 
            radial-gradient(at 0% 0%, rgba(52, 152, 219, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(46, 204, 113, 0.15) 0px, transparent 50%);
    }

    /* lowercase font */
    * { text-transform: lowercase !important; font-family: 'inter', sans-serif; }

    /* frosted glass cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
    }

    /* minimal button */
    div.stButton > button {
        background: white;
        color: black;
        border: none;
        border-radius: 12px;
        padding: 10px 30px;
        font-weight: 500;
        width: 100%;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        transform: scale(1.02);
        background: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 mixer")

# step 1: video
st.markdown('<div class="glass-card">🎥 video (audio)</div>', unsafe_allow_html=True)
v_file = st.file_uploader("v", type=["mp4", "mov", "avi"], label_visibility="collapsed")

# step 2: photos
st.markdown('<div class="glass-card">🖼️ photo(s)</div>', unsafe_allow_html=True)
img_files = st.file_uploader("p", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")

# action
st.write(" ")
if st.button("start"):
    if v_file and img_files:
        status = st.empty()
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_vid:
                t_vid.write(v_file.read())
                v_path = t_vid.name

            status.text("processing...")
            
            video_clip = mp.VideoFileClip(v_path)
            audio = video_clip.audio
            
            duration_per_photo = audio.duration / len(img_files)
            
            clips = []
            for img_file in img_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as t_img:
                    t_img.write(img_file.read())
                    i_path = t_img.name
                
                # smooth fade
                clip = (mp.ImageClip(i_path)
                        .with_duration(duration_per_photo)
                        .with_effects([mp.vfx.CrossFadeIn(0.5)]))
                clips.append(clip)

            final_video = mp.concatenate_videoclips(clips, method="compose").with_audio(audio)
            
            out_file = "output.mp4"
            final_video.write_videofile(out_file, fps=24, codec="libx264", audio_codec="aac")
            
            status.text("done")
            st.video(out_file)
            
            st.download_button("save", open(out_file, "rb"), file_name="video.mp4")

            # cleanup
            video_clip.close()
            final_video.close()
            os.remove(v_path)

        except Exception as e:
            st.text("error")
    else:
        st.text("upload first")
