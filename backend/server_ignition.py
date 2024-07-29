import subprocess
import time 
from celery import celery
import requests

def startServer():
    return subprocess.Popen(["daphne", "your_project_name.asgi:application"])


def waitIgnition():
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


def startCeleryWorker():
    subprocess.Popen(["celery", "-A", "backend_server", "worker", "-l info"])

if __name__ == "__main__":
    server_process = start_server()
    waitIgnition()
    startCeleryWorker()

    # Keep the script running so it doesn't exit
    try:
        server_process.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        server_process.terminate()
