import streamlit as st
import moviepy as mp
import tempfile
import os

st.set_page_config(page_title="Media Mixer", page_icon="🎬")

# Minimal CSS to clean up the interface
st.markdown("""
    <style>
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .st-emotion-cache-1kyxreq {justify-content: center;}
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Media Mixer")

# Step 1: Uploads with Icons
v_file = st.file_uploader("📁 Step 1: Upload Video (Sound Source)", type=["mp4", "mov", "avi"])
img_files = st.file_uploader("🖼️ Step 2: Upload Photo(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if st.button("🚀 Create Video"):
    if v_file and img_files:
        status = st.empty()
        bar = st.progress(0)
        
        try:
            # Save temporary video
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_vid:
                t_vid.write(v_file.read())
                v_path = t_vid.name

            status.text("⚙️ Processing...")
            
            # Load Audio
            video_clip = mp.VideoFileClip(v_path)
            audio = video_clip.audio
            total_duration = audio.duration
            
            # Logic: Split time equally between photos
            num_photos = len(img_files)
            duration_per_photo = total_duration / num_photos
            
            clips = []
            for img_file in img_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as t_img:
                    t_img.write(img_file.read())
                    i_path = t_img.name
                
                # Create a clip for each photo with calculated duration
                clip = mp.ImageClip(i_path).with_duration(duration_per_photo)
                clips.append(clip)
                # Note: We don't delete i_path yet as moviepy needs it for the final render

            # Concatenate all photos into one sequence
            final_slideshow = mp.concatenate_videoclips(clips, method="compose")
            final_video = final_slideshow.with_audio(audio)
            
            out_file = "result.mp4"
            final_video.write_videofile(out_file, fps=24, codec="libx264", audio_codec="aac")
            
            bar.progress(100)
            status.success("✅ Done!")

            st.video(out_file)
            with open(out_file, "rb") as f:
                st.download_button("💾 Save Video", f, file_name="slideshow.mp4")

            # Cleanup
            video_clip.close()
            final_video.close()
            os.remove(v_path)
            # (In a real production app, you'd clean up the temp image paths here too)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please upload both a video and at least one photo!")
