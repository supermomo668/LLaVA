import gradio as gr
from transformers import pipeline
from time import time
# using datetime module
import datetime;

controller_addr="http://localhost:21001"
worker_addr="http://localhost:10000"
image_path = "<add path here>"

p = pipeline("automatic-speech-recognition")

start = 0 

import gradio as gr


import argparse
import json

import requests

from llava.conversation import default_conversation
from PIL import Image

def format_and_get_images(input_pil_images, return_pil=False,image_process_mode="Pad"):
    images = []
    for i, image in enumerate(input_pil_images):
        if i % 2 == 0:
            import base64
            from io import BytesIO
            from PIL import Image
            if image_process_mode == "Pad":
                def expand2square(pil_img, background_color=(122, 116, 104)):
                    width, height = pil_img.size
                    if width == height:
                        return pil_img
                    elif width > height:
                        result = Image.new(pil_img.mode, (width, width), background_color)
                        result.paste(pil_img, (0, (width - height) // 2))
                        return result
                    else:
                        result = Image.new(pil_img.mode, (height, height), background_color)
                        result.paste(pil_img, ((height - width) // 2, 0))
                        return result
                image = expand2square(image)
            elif image_process_mode == "Crop":
                pass
            elif image_process_mode == "Resize":
                image = image.resize((336, 336))
            else:
                raise ValueError(f"Invalid image_process_mode: {image_process_mode}")
            max_hw, min_hw = max(image.size), min(image.size)
            aspect_ratio = max_hw / min_hw
            max_len, min_len = 800, 400
            shortest_edge = int(min(max_len / aspect_ratio, min_len, min_hw))
            longest_edge = int(shortest_edge * aspect_ratio)
            W, H = image.size
            if H > W:
                H, W = longest_edge, shortest_edge
            else:
                H, W = shortest_edge, longest_edge
            image = image.resize((W, H))
            if return_pil:
                images.append(image)
            else:
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_b64_str = base64.b64encode(buffered.getvalue()).decode()
                images.append(img_b64_str)
    return images



def prompt_llava(prompt_message,images,model_name="llava-llama-2-13b-chat-lightning-preview",max_new_tokens=300):
    conv = default_conversation.copy()
    conv.append_message(conv.roles[0], prompt_message)
    prompt = conv.get_prompt()

    headers = {"User-Agent": "LLaVA Client"}
    pload = {
        "model": model_name,
        "prompt": prompt,
        "max_new_tokens": max_new_tokens,
        "temperature": 0.7,
        "stop": conv.sep,
        "images": images
    }
    response = requests.post(worker_addr + "/worker_generate_stream", headers=headers,
            json=pload, stream=True)

    print(prompt.replace(conv.sep, "\n"), end="")
    final_output=""
    for chunk in response.iter_lines(chunk_size=8192, decode_unicode=False, delimiter=b"\0"):
        if chunk:
            data = json.loads(chunk.decode("utf-8"))
            output = data["text"].split(conv.sep)[-1]
            final_output = final_output + output
            print(output, end="\r")
    
    return final_output

def transcribe(audio,video):
    duration = time() - start 
    ct = datetime.datetime.now()
    text = p(audio)["text"]
    return text


with gr.Blocks() as demo:
    gr.Markdown("Start typing below and then click **Run** to see the output.")
    with gr.Row():
        audio_inp = gr.Audio(source="microphone", type="filepath")
        video_inp = gr.Video(source="upload")
        out = gr.Textbox()
    btn = gr.Button("Run")
    start = time()
    btn.click(fn=transcribe, inputs=[audio_inp,video_inp], outputs=out)
    pil_img = Image.open(image_path)
    transcript_text = out.value
    format_images = format_and_get_images([pil_img])
    transcript_text = "what is the product about"
    llava_output = prompt_llava(transcript_text,format_images)
    out.value = llava_output
    print("llava out",llava_output)



demo.launch()


