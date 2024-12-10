import threading
import time

from config import API_KEY, SIMULATED_DELAY
from flask import Flask, request
from flask_socketio import SocketIO, disconnect, emit
from status_sim import JobStatusSimulator

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory job status store
job_status_store = {}

def authenticate_socket(auth_token):
    """Verify the authentication token"""
    return auth_token == API_KEY

@socketio.on("connect")
def handle_connect():
    auth_token = request.args.get('auth_token')
    if not auth_token or not authenticate_socket(auth_token):
        print("Failed authentication attempt")
        disconnect()
        return False
    print("WebSocket client connected.")


@app.route("/start_job", methods=["POST"])
def start_job():
    """
    API to start a new translation job for WebSocket clients.
    """
    job_id = request.json.get("job_id")
    if not job_id:
        return {"error": "Missing job_id"}, 400

    if job_id in job_status_store:
        return {"error": "Job already exists"}, 400

    # Start the job status simulation in a separate thread
    thread = threading.Thread(target=simulate_job_status, args=(job_id,))
    thread.start()

    return {"message": "Job started", "job_id": job_id}, 202


def simulate_job_status(job_id):
    """
    Simulates job status transitions and sends WebSocket updates.
    """
    # Initialize the job status
    job_status_store[job_id] = {"status": "pending", "progress": 0}
    socketio.emit(f"status_update/{job_id}", {"status": job_status_store[job_id]})
    
    total_steps = 10
    step_delay = 2  # Fixed 2-second interval
    
    for i in range(total_steps):
        time.sleep(step_delay)
        job_status_store[job_id] = {
            "status": "pending",
            "progress": ((i + 1) * 100) // total_steps
        }
        # Emit progress update for specific job
        socketio.emit(f"status_update/{job_id}", {"status": job_status_store[job_id]})
    
    # Set and emit final status
    job_status_store[job_id] = {"status": "completed", "progress": 100}
    socketio.emit(f"status_update/{job_id}", {"status": job_status_store[job_id]})


@socketio.on("disconnect")
def handle_disconnect():
    print("WebSocket client disconnected.")


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5002)
