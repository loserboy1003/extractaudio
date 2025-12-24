import streamlit as st
import moviepy as mp
import tempfile
import os

st.set_page_config(page_title="mixer", page_icon="🎬", layout="wide")

# custom "pro" styling
st.markdown("""
    <style>
    /* background and text */
    .stApp { background: #0e1117; color: #ffffff; }
    * { text-transform: lowercase !important; font-family: 'monospace'; }
    
    /* hide streamlit clutter */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    
    /* glow effect for containers */
    div[data-testid="stVerticalBlock"] > div:has(div.stFileUploader) {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
    }

    /* customize buttons */
    div.stButton > button {
        border-radius: 50px;
        background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        padding: 10px 40px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 mixer.pro")

# setup layout
left_col, right_col = st.columns(2, gap="large")

with left_col:
    st.markdown("### 🔈 sound source")
    v_file = st.file_uploader("1", type=["mp4", "mov", "avi"], label_visibility="collapsed")
    if v_file:
        st.info("video loaded")

with right_col:
    st.markdown("### 🖼️ visual layer")
    img_files = st.file_uploader("2", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="collapsed")
    if img_files:
        st.success(f"{len(img_files)} images ready")

st.markdown("---")

# centered processing area
c1, c2, c3 = st.columns([1,2,1])
with c2:
    if st.button("generate"):
        if v_file and img_files:
            progress_container = st.empty()
            
            try:
                # 1. temp save
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_vid:
                    t_vid.write(v_file.read())
                    v_path = t_vid.name

                progress_container.text("🧬 rendering...")
                
                # 2. engine
                video_clip = mp.VideoFileClip(v_path)
                audio = video_clip.audio
                
                duration_per_photo = audio.duration / len(img_files)
                
                clips = []
                for img_file in img_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as t_img:
                        t_img.write(img_file.read())
                        i_path = t_img.name
                    
                    clip = (mp.ImageClip(i_path)
                            .with_duration(duration_per_photo)
                            .with_effects([mp.vfx.CrossFadeIn(0.4)]))
                    clips.append(clip)

                # 3. export
                final_video = mp.concatenate_videoclips(clips, method="compose").with_audio(audio)
                out_file = "mix.mp4"
                final_video.write_videofile(out_file, fps=24, codec="libx264", audio_codec="aac", bitrate="5000k")
                
                progress_container.text("✨ ready")
                st.video(out_file)
                
                with open(out_file, "rb") as f:
                    st.download_button("download", f, file_name="mix.mp4", use_container_width=True)

                # 4. cleanup
                video_clip.close()
                final_video.close()
                os.remove(v_path)

            except Exception as e:
                st.error("failed")
        else:
            st.warning("missing files")
