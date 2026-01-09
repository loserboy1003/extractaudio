import streamlit as st
import moviepy as mp
import tempfile
import os

st.set_page_config(page_title="Mixer", page_icon="🎬")

st.markdown("""
    <style>
    /* Mesh Gradient Background */
    .stApp {
        background-color: #0e1117;
        background-image: 
            radial-gradient(at 0% 0%, rgba(52, 152, 219, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(46, 204, 113, 0.15) 0px, transparent 50%);
    }
    
    /* Clean UI */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Big Colorful Text for Mom */
    .hindi-label { font-size: 22px; font-weight: bold; margin-bottom: 10px; }
    .blue { color: #3498db; }
    .green { color: #2ecc71; }

    /* Centered Minimal Button */
    div.stButton > button {
        background: white;
        color: black;
        border: none;
        border-radius: 10px;
        padding: 15px;
        width: 100%;
        font-weight: bold;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Media Mixer")

st.markdown('<p class="hindi-label blue">🎥 1. वीडियो चुनें </p>', unsafe_allow_html=True)
v_file = st.file_uploader("v", type=["mp4", "mov", "avi"], label_visibility="collapsed")

st.write("---")

st.markdown('<p class="hindi-label green">🖼️ 2. फोटो चुनें</p>', unsafe_allow_html=True)
img_files = st.file_uploader("p", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")

if st.button("वीडियो बनाएँ"):
    if v_file and img_files:
        status = st.empty()
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_vid:
                t_vid.write(v_file.read())
                v_path = t_vid.name

            status.info("काम चालू है... कृपया इंतज़ार करें")
            
            video_clip = mp.VideoFileClip(v_path)
            audio = video_clip.audio
            
            num_photos = len(img_files)
            duration_per_photo = audio.duration / num_photos
            
            clips = []
            for img_file in img_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as t_img:
                    t_img.write(img_file.read())
                    i_path = t_img.name
                
                clip = (mp.ImageClip(i_path)
                        .with_duration(duration_per_photo)
                        .with_effects([mp.vfx.CrossFadeIn(0.5)]))
                clips.append(clip)

            final_video = mp.concatenate_videoclips(clips, method="compose").with_audio(audio)
            
            out_file = "final.mp4"
            final_video.write_videofile(out_file, fps=24, codec="libx264", audio_codec="aac")
            
            status.success("आपका वीडियो तैयार है!")
            st.video(out_file)
            
            with open(out_file, "rb") as f:
                st.download_button("💾 फोन में सेव करें", f, file_name="video.mp4")

            video_clip.close()
            final_video.close()
            os.remove(v_path)

        except Exception as e:
            st.error("कुछ गलती हुई है")
    else:
        st.warning("कृपया पहले फाइल डालें")

