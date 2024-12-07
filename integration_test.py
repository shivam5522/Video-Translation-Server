import os
import subprocess
import threading
import time

from dotenv import load_dotenv

from client.rest_client import RestClient
from client.ws_client import WebSocketClient

# Load the env variables from the .env file
load_dotenv()


def start_server():
    """
    Starts the Flask server.
    """
    subprocess.Popen(["python", "server/app.py"])


def test_rest_client():
    """
    Integration test for the REST client.
    """
    client = RestClient(
        base_url=f"http://{os.getenv("BASE_URL")}", api_key=os.getenv("API_KEY")
    )
    job_id = "job123"

    print("Starting job...")
    client.start_job(job_id)

    print("Waiting for job to complete...")
    status = client.wait_for_completion(job_id)
    print(f"Final job status: {status}")


def test_websocket_client():
    """
    Integration test for the WebSocket client.
    """
    client = WebSocketClient(
        ws_url=f"ws://{os.getenv("BASE_URL")}/status", api_key=os.getenv("API_KEY")
    )
    client.connect()


if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Allow server to initialize
    time.sleep(2)

    print("Testing REST Client...")
    test_rest_client()

    # print("\nTesting WebSocket Client...")
    # test_websocket_client()
