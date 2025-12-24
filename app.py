import streamlit as st
from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip
import os
import tempfile

st.set_page_config(page_title="Audio-to-Photo Overlay", layout="centered")

st.title("🎵 Audio-to-Photo Overlay")
st.write("Extract audio from a video and attach it to a static image.")

# --- UI Components ---
uploaded_video = st.file_uploader("1. Upload Video (to extract audio)", type=["mp4", "mov", "avi", "mkv"])
uploaded_image = st.file_uploader("2. Upload Image (for the background)", type=["jpg", "jpeg", "png"])

if st.button("Generate Video"):
    if uploaded_video and uploaded_image:
        with st.spinner("Processing... this may take a moment."):
            try:
                # Create temporary files to store uploaded data
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_video:
                    t_video.write(uploaded_video.read())
                    video_path = t_video.name

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as t_image:
                    t_image.write(uploaded_image.read())
                    image_path = t_image.name

                # 1. Extract Audio
                video_clip = VideoFileClip(video_path)
                audio_clip = video_clip.audio

                # 2. Create Image Clip (set duration to match audio)
                img_clip = ImageClip(image_path).set_duration(audio_clip.duration)
                
                # 3. Combine Image and Audio
                final_clip = img_clip.set_audio(audio_clip)
                
                # 4. Save to a temporary output path
                output_path = "output_video.mp4"
                # using a fast preset for minimal UI wait time
                final_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

                # Display Success
                st.success("Video Generated Successfully!")
                st.video(output_path)

                # Download Button
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="Download Processed Video",
                        data=file,
                        file_name="combined_output.mp4",
                        mime="video/mp4"
                    )

                # Cleanup
                video_clip.close()
                final_clip.close()
                os.remove(video_path)
                os.remove(image_path)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload both a video and an image file.")