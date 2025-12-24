import streamlit as st
import moviepy as mp
import tempfile
import os

st.set_page_config(page_title="Media Mixer", page_icon="🎬", layout="centered")

# --- Advanced Animated Mesh UI ---
st.markdown("""
    <style>
    /* hide streamlit clutter */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Animated Liquid Background */
    .stApp {
        background: linear-gradient(-45deg, #121212, #1a1c2c, #0d253f, #101010);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Bold Headers */
    h1, h2, h3, p {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    /* High-End Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 30px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 25px;
        text-align: center;
    }

    /* Glow Button */
    div.stButton > button {
        background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 15px 40px;
        font-weight: bold;
        font-size: 18px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4);
        transition: 0.3s all ease;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 114, 255, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Media Mixer Pro")

# --- Step 1 ---
st.markdown('<div class="glass-card"><h3>🎥 Step 1: Video (Audio Source)</h3></div>', unsafe_allow_html=True)
v_file = st.file_uploader("video", type=["mp4", "mov", "avi"], label_visibility="collapsed")

# --- Step 2 ---
st.markdown('<div class="glass-card"><h3>🖼️ Step 2: Select Photo(s)</h3></div>', unsafe_allow_html=True)
img_files = st.file_uploader("photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")

# --- Action ---
st.write(" ")
if st.button("GENERATE VIDEO"):
    if v_file and img_files:
        status = st.empty()
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_vid:
                t_vid.write(v_file.read())
                v_path = t_vid.name

            status.info("🧬 Rendering your media...")
            
            video_clip = mp.VideoFileClip(v_path)
            audio = video_clip.audio
            
            # Split time equally
            duration_per_photo = audio.duration / len(img_files)
            
            clips = []
            for img_file in img_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as t_img:
                    t_img.write(img_file.read())
                    i_path = t_img.name
                
                # Professional Crossfade
                clip = (mp.ImageClip(i_path)
                        .with_duration(duration_per_photo)
                        .with_effects([mp.vfx.CrossFadeIn(0.6)]))
                clips.append(clip)

            final_video = mp.concatenate_videoclips(clips, method="compose").with_audio(audio)
            
            out_file = "final_output.mp4"
            final_video.write_videofile(out_file, fps=24, codec="libx264", audio_codec="aac")
            
            status.success("✨ Your video is ready!")
            st.video(out_file)
            
            st.download_button("📥 DOWNLOAD AND SAVE", open(out_file, "rb"), file_name="creation.mp4")

            # cleanup
            video_clip.close()
            final_video.close()
            os.remove(v_path)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload files first!")
