import requests

DEFAULT_PLOAD_PARAM = {
  "model": "llava-llama-2-13b-chat-lightning-preview",
  "max_new_tokens": 512,
  "temperature": 0.2,
  "top_p": 0.7,
  "stop": '</s>',
}
# PLOAD Schema
  # {
  #   "Key:stop\n\t: Value</s>\n\tType:<class 'str'>", 
  # "Key:temperature\n\t: Value0.2\n\tType:<class 'float'>", 
  # "Key:top_p\n\t: Value0.7\n\tType:<class 'float'>", 
  # "Key:model\n\t: Valuellava-llama-2-13b-chat-lightning-preview\n\tType:<class 'str'>", 

if __name__=="__main__":
  headers = {"User-Agent": "LLaVA Client"} 
  port=40000
  DEFAULT_IMG="serve_images/2023-10-05/b939abf2c4553ce07e642170aee3a3d7.jpg"
  import argparse
  from PIL import Image
  parser = argparse.ArgumentParser(description="Your Script Description")
  worker_addr = f"http://localhost:{port}"
  

  # Add command-line arguments for server IP and port
  parser.add_argument(
    "--prompt", type=str, default="Say only the word 'Hello' regardless of anything. ")
  parser.add_argument(
    "--image", type=str, default=DEFAULT_IMG)
  args = parser.parse_args()
  
  pload = {
    "prompt": args.prompt,
    "images": [Image.open(args.image)]
  }

  # {
  #   'model': 'llava-llama-2-13b-chat-lightning-preview', 
  #   'prompt': '[INST] <<SYS>>\nYou are a helpful language and vision assistant. You are able to understand the visual content that the user provides, and assist the user with a variety of tasks using natural language.\n<</SYS>>\n\n<image>\nWhat is unusual about this image? [/INST]',
  #  'temperature': 0.2, 'top_p': 0.7, 'max_new_tokens': 512, 'stop': '</s>', 'images': "List of 1 images: ['b939abf2c4553ce07e642170aee3a3d7']"
  # }
  response = requests.post(
    f"{worker_addr}/worker_generate_stream", 
    headers=headers,
    json=pload, stream=True
  )