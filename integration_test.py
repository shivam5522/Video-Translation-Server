import os
import subprocess
import sys
import threading
import time
import uuid

import requests
from dotenv import load_dotenv

from client.rest_client import RestClient
from client.ws_client import WebSocketClient

# Load the env variables from the .env file
load_dotenv()


# Starts up the server, passing argument rest as True will fire up the rest server or it will fire up the websocket server.
def start_server(rest=True):
    """
    Starts the Flask server.
    """
    if rest:
        subprocess.Popen(["python", "server/app.py"])
    else:
        subprocess.Popen(["python", "server/ws_server.py"])


# test_rest_client() tests the Rest implementation by initializing the client and checks for the job status
def test_rest_client():
    """
    Integration test for the REST client.
    """
    client = RestClient(
        base_url=f"http://{os.getenv("BASE_URL")}:5000", api_key=os.getenv("API_KEY")
    )
    job_id = str(uuid.uuid4())

    print("Starting job...")
    client.start_job(job_id)

    print("Waiting for job to complete...")
    status = client.wait_for_completion(job_id)
    print(f"Final job status: {status}")


# test_websocket_client() tests the Websocket implementation by initializing the client and checks for the job status
def test_websocket_client():
    """
    Integration test for the WebSocket client.
    """
    ws_url = f"ws://{os.getenv('BASE_URL')}:5002"  # Base WebSocket URL
    client = WebSocketClient(ws_url=ws_url, api_key=os.getenv("API_KEY"))

    print("Connecting to WebSocket...")
    client.connect()

    # Start the job via HTTP
    job_id = str(uuid.uuid4())
    print(f"Starting job with ID: {job_id}...")

    response = requests.post(
        f"http://{os.getenv('BASE_URL')}:5002/start_job",
        json={"job_id": job_id},
        headers={"Authorization": f"Bearer {os.getenv('API_KEY')}"},
    )
    if response.status_code == 202:
        print(f"Job {job_id} started successfully.")
    else:
        print(f"Failed to start job. Error: {response.text}")
        return

    print("Listening for job updates...")
    client.listen()


if __name__ == "__main__":
    # Check for command-line arguments
    if len(sys.argv) != 2 or sys.argv[1] not in ["rest", "ws"]:
        print("Usage: python integration_test.py [rest|ws]")
        sys.exit(1)

    # Determine if we should start the REST or WebSocket server
    is_rest = sys.argv[1] == "rest"

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, args=(is_rest,), daemon=True)
    server_thread.start()

    # Allow server to initialize
    time.sleep(2)

    if is_rest:
        print("Testing REST Client...")
        test_rest_client()
    else:
        print("\nTesting WebSocket Client...")
        test_websocket_client()
