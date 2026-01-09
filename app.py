import gradio as gr
import moviepy as mp
import tempfile
import os

def mix_media(video_input, image_inputs):
    if not video_input or not image_inputs:
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as t_out:
        out_path = t_out.name

    video_clip = mp.VideoFileClip(video_input)
    audio = video_clip.audio
    total_duration = audio.duration
    
    num_photos = len(image_inputs)
    duration_per_photo = total_duration / num_photos
    
    clips = []
    for img_path in image_inputs:
        clip = (mp.ImageClip(img_path)
                .with_duration(duration_per_photo)
                .with_effects([mp.vfx.CrossFadeIn(0.5)]))
        clips.append(clip)

    final_slideshow = mp.concatenate_videoclips(clips, method="compose")
    final_video = final_slideshow.with_audio(audio)
    
    final_video.write_videofile(out_path, fps=24, codec="libx264", audio_codec="aac")
    
    video_clip.close()
    final_video.close()
    
    return out_path

custom_css = """
body {
    background-color: #0e1117;
    background-image: 
        radial-gradient(at 0% 0%, rgba(52, 152, 219, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(155, 89, 182, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(46, 204, 113, 0.15) 0px, transparent 50%),
        radial-gradient(at 0% 100%, rgba(231, 76, 60, 0.15) 0px, transparent 50%);
    background-attachment: fixed;
}
.gradio-container {
    border: none !important;
}
button.primary {
    background: linear-gradient(90deg, #3498db, #2ecc71) !important;
    border: none !important;
    color: white !important;
}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎬 Media Mixer Pro")
    
    with gr.Row():
        with gr.Column():
            video_in = gr.Video(label="🎥 1. Upload Video (Sound Source)")
            images_in = gr.File(label="🖼️ 2. Upload Photo(s)", file_count="multiple", file_types=["image"])
        
        with gr.Column():
            video_out = gr.Video(label="✅ Result")
            generate_btn = gr.Button("Create Video", variant="primary")

    generate_btn.click(
        fn=mix_media,
        inputs=[video_in, images_in],
        outputs=video_out
    )

if __name__ == "__main__":
    demo.launch()
