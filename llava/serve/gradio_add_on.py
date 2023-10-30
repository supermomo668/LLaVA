import gradio as gr
import speech_recognition as sr
import webrtcvad
import numpy as np
from moviepy.editor import *

def process_audio_video(audio, video):
    # Setup VAD
    vad = webrtcvad.Vad(3)
    raw_audio = np.frombuffer(audio.raw_data, np.int16)

    frame_duration = 0.01  # 10ms
    samples_per_frame = int(audio.rate * frame_duration)

    speech_segments = []
    start = None
    for i in range(0, len(raw_audio), samples_per_frame):
        frame = raw_audio[i:i+samples_per_frame]
        if len(frame) < samples_per_frame:
            break
        is_speech = vad.is_speech(frame.tobytes(), sample_rate=audio.rate)

        if start is None and is_speech:
            start = i / audio.rate
        elif start is not None and not is_speech:
            end = i / audio.rate
            speech_segments.append((start, end))
            start = None

    # Assuming you want to process the longest speech segment
    longest_segment = max(speech_segments, key=lambda x: x[1] - x[0], default=None)
    
    transcript = "No speech detected"
    if longest_segment:
        start_time, end_time = longest_segment
        start_sample = int(start_time * audio.rate)
        end_sample = int(end_time * audio.rate)
        segment_audio_data = raw_audio[start_sample:end_sample]

        with sr.AudioData(segment_audio_data.tobytes(), audio.rate, audio.sample_width) as segment_source:
            r = sr.Recognizer()
            try:
                transcript = r.recognize_google(segment_source)
            except sr.UnknownValueError:
                transcript = "Could not understand the audio."
            except sr.RequestError:
                transcript = "API unavailable or unresponsive."

    # Extract video subclip based on the longest audio segment
    clip = VideoFileClip(video.name)
    
    if longest_segment:
        video_subclip = clip.subclip(*longest_segment)
        output_path = "video_based_on_longest_segment.mp4"
        video_subclip.write_videofile(output_path, codec="libx264")
        video_message = f"Video subclip saved at: {output_path}"
    else:
        video_message = "No speech detected, so no video subclip created."

    return (
        f"Audio Duration: {len(audio) / audio.rate:.2f} seconds", 
        f"Video Duration: {len(video) / video.fps:.2f} seconds", 
        f"Transcription of longest segment: {transcript}",
        video_message
    )

# Define the Gradio interface
iface = gr.Interface(
    fn=process_audio_video, 
    inputs=[
        gr.inputs.Audio(type="file"), 
        gr.inputs.Video(type="file")
    ], 
    outputs=[
        "text", 
        "text",
        "text",
        "text"
    ]
)

iface.launch()


