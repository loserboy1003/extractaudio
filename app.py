import streamlit as st
import moviepy as mp
import tempfile
import os

st.set_page_config(page_title="Media Mixer", page_icon="🎬")

st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        background-image: 
            radial-gradient(at 0% 0%, rgba(52, 152, 219, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(155, 89, 182, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(46, 204, 113, 0.15) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(231, 76, 60, 0.15) 0px, transparent 50%);
    }
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .big-font { font-size:25px !important; font-weight: bold; }
    .video-text { color: #3498db; }
    .photo-text { color: #2ecc71; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Media Mixer")

st.markdown('<p class="big-font video-text">🎥 1. Upload VIDEO (for sound)</p>', unsafe_allow_html=True)
v_file = st.file_uploader("The sound will be taken from this video", type=["mp4", "mov", "avi"], label_visibility="collapsed")

st.markdown("---")

st.markdown('<p class="big-font photo-text">🖼️ 2. Upload PHOTO(S)</p>', unsafe_allow_html=True)
img_files = st.file_uploader("Select one or more photos for the slideshow", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")

if st.button(" Create Video ", use_container_width=True):
    if v_file and img_files:
        status = st.empty()
        bar = st.progress(0)
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_vid:
                t_vid.write(v_file.read())
                v_path = t_vid.name

            status.text("⚙️ Creating your slideshow...")
            
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
            
            out_file = "final_video.mp4"
            final_video.write_videofile(out_file, fps=24, codec="libx264", audio_codec="aac")
            
            bar.progress(100)
            status.success("✅ Your video is ready!")

            st.video(out_file)
            with open(out_file, "rb") as f:
                st.download_button("💾 DOWNLOAD VIDEO", f, file_name="my_creation.mp4", use_container_width=True)

            video_clip.close()
            final_video.close()
            os.remove(v_path)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please make sure you've uploaded a video and at least one photo!")
