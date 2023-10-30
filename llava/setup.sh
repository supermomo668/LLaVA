env_name=$"{$1:-dl}"
conda activate $env_name
pip install --upgrade pip  # enable PEP 660 support
pip install -e .
pip install ninja
pip install flash-attn --no-build-isolation
# extra dependencies
sudo apt update && sudo apt install ffmpeg
pip install -U openai-whisper
