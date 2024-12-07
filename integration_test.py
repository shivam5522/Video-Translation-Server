import os
import subprocess
import sys
import threading
import time

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
        base_url=f"http://{os.getenv("BASE_URL")}", api_key=os.getenv("API_KEY")
    )
    job_id = "job123"

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
    client = WebSocketClient(
        ws_url=f"ws://{os.getenv("BASE_URL")}/status", api_key=os.getenv("API_KEY")
    )
    client.connect()


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
