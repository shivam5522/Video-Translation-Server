import threading
import time

from config import API_KEY, SIMULATED_DELAY
from flask import Flask, jsonify, request
from flask_httpauth import HTTPTokenAuth
from status_sim import JobStatusSimulator

app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")

# Stores the Status of jobs in a key value pair, where key = JOB_ID and value is the status of the job ie: Pending, Completed.
job_status_store = {}


# Auth method to make sure that the user who is making the call is the correct and authorized user.
@auth.verify_token
def verify_token(token):
    return token == API_KEY


# The endpoint /status gives the status of the job. This is a get request, job id is passed as an argument in the get request url.
@app.route("/status", methods=["GET"])
@auth.login_required  # Makes sure that the user who is making the request is valid.
def get_status():
    job_id = request.args.get("job_id")
    if not job_id:  # Checks if a job id is passed in the GET request
        return jsonify({"error": "Missing job_id"}), 400

    if (
        job_id not in job_status_store
    ):  # Checks if the job ID is not being processed (ie: is unique)
        return jsonify({"error": "Invalid job_id"}), 404

    return jsonify({"job_id": job_id, "status": job_status_store[job_id]})


# The endpoint /start_job is used by the client to initialize and run the job. This creates a thread to simulate the processing of the video translation.
@app.route("/start_job", methods=["POST"])
@auth.login_required
def start_job():
    """
    API to start a new translation job.
    """
    job_id = request.json.get("job_id")
    if not job_id:
        return jsonify({"error": "Missing job_id"}), 400

    if job_id in job_status_store:
        return jsonify({"error": "Job already exists"}), 400

    # Start the job status simulation in a separate thread
    thread = threading.Thread(
        target=JobStatusSimulator.simulate_job_status,
        args=(job_id, SIMULATED_DELAY, job_status_store),
    )
    thread.start()

    return jsonify({"message": "Job started", "job_id": job_id}), 202


if __name__ == "__main__":
    app.run(debug=True)
