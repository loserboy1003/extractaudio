import streamlit as st
import moviepy as mp
import tempfile
import os

st.set_page_config(page_title="mixer", page_icon="🎬")

st.markdown("""
    <style>
    * { text-transform: lowercase; }
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .video-box { border: 2px solid #3498db; padding: 10px; border-radius: 10px; }
    .photo-box { border: 2px solid #2ecc71; padding: 10px; border-radius: 10px; }
    /* minimal button style */
    div.stButton > button:first-child {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #000000;
        border-radius: 5px;
        width: 100px;
        height: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="video-box">🎥 video </div>', unsafe_allow_html=True)
v_file = st.file_uploader("video", type=["mp4", "mov", "avi"], label_visibility="collapsed")

st.write(" ")

st.markdown('<div class="photo-box">🖼️ photos</div>', unsafe_allow_html=True)
img_files = st.file_uploader("photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")

st.write(" ")

# minimal button
if st.button("start"):
    if v_file and img_files:
        status = st.empty()
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_vid:
                t_vid.write(v_file.read())
                v_path = t_vid.name

            status.text("loading...")
            
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
                
                clip = (mp.ImageClip(i_path)
                        .with_duration(duration_per_photo)
                        .with_effects([mp.vfx.CrossFadeIn(0.5)]))
                clips.append(clip)

            final_slideshow = mp.concatenate_videoclips(clips, method="compose")
            final_video = final_slideshow.with_audio(audio)
            
            out_file = "output.mp4"
            final_video.write_videofile(out_file, fps=24, codec="libx264", audio_codec="aac")
            
            status.text("done!")
            st.video(out_file)
            
            with open(out_file, "rb") as f:
                st.download_button("save", f, file_name="video.mp4")

            video_clip.close()
            final_video.close()
            os.remove(v_path)

        except Exception as e:
            st.text("error")
    else:
        st.text("upload files first")

