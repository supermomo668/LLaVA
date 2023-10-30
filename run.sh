Help(){
  echo "Instructions to start Llava APIs without the web server. Activate your virtual environment with required packages first."
}
cd LLaVA
default_start_cmd="cd $PWD && conda activate vision-cap"
start_cmd="${1:-$default_start_cmd}"
model="${2:-'liuhaotian/llava-llama-2-13b-chat-lightning-preview'}"

tmux new-session -d -s "control"
tmux new-session -d -s "worker"
echo "Creating session 'control' & 'worker' to support API inference"
tmux send-keys -t control "$start_cmd" C-m
tmux send-keys -t worker "$start_cmd" C-m

tmux \
  send-keys -t control "python -m llava.serve.controller --host 0.0.0.0 --port 10000" C-m
tmux \
  send-keys -t worker "python -m llava.serve.model_worker --host 0.0.0.0 --controller http://localhost:10000 --port 40000 --worker http://localhost:40000 --model-path $model --load-4bit" C-m


# run webserver
python -m llava.serve.gradio_web_server --controller http://localhost:10000 --model-list-mode reload
