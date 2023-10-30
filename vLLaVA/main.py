from fastapi import FastAPI
import subprocess
import time
import requests

# Function to start a Flask server in a subprocess
def start_flask_server(port, server_name):
    subprocess.Popen(["python", "your_flask_app.py", f"--port={port}", f"--name={server_name}"])

app = FastAPI()

# Example route that returns a JSON response
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
  

if __name__ == "__main__":
  import uvicorn, argparse
  # Wait for a while to ensure the servers are up and running
  time.sleep(2)

  # Start the first Flask server on port 5000 with a name "server1"
  start_flask_server(5000, "server1")

  # Start the second Flask server on port 5001 with a name "server2"
  start_flask_server(5001, "server2")

  uvicorn.run(app, host="0.0.0.0", port=8000)
