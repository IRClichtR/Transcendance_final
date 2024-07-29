import subprocess
import time
import sys
import os
import requests

# Add the directory containing celery.py to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend_server/backend_server/'))

def start_server():
    return subprocess.Popen(["daphne", "backend_server.asgi:application"])

def wait_ignition():
    print("Waiting for server to be ready...")
    url = "http://0.0.0.0:8001"
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Server is up!")
                break
        except requests.exceptions.RequestException as err:
            print(f"Error connecting to server: {err}")
        time.sleep(1)

def start_celery_worker():
    subprocess.Popen(["celery", "-A", "backend_server", "worker", "-l", "info"])

if __name__ == "__main__":
    server_process = start_server()
    wait_ignition()
    start_celery_worker()

    # Keep the script running so it doesn't exit
    try:
        server_process.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        server_process.terminate()
