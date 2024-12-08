import threading

from config import SIMULATED_DELAY
from flask import Flask, request
from flask_socketio import SocketIO, emit
from status_sim import JobStatusSimulator

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory job status store
job_status_store = {}


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
    simulator = JobStatusSimulator()
    simulator.simulate_job_status(job_id, SIMULATED_DELAY, job_status_store)
    status = job_status_store[job_id]  # Get the final status after simulation
    socketio.emit("status_update", {"job_id": job_id, "status": status})


@socketio.on("connect")
def handle_connect():
    print("WebSocket client connected.")


@socketio.on("disconnect")
def handle_disconnect():
    print("WebSocket client disconnected.")


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5002)
