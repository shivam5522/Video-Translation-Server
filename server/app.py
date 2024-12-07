from flask import Flask, jsonify, request
from flask_httpauth import HTTPTokenAuth
import time
import threading
from config import API_KEY, SIMULATED_DELAY
from status_sim import JobStatusSimulator

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

# In-memory job status store
job_status_store = {}

# Authentication
@auth.verify_token
def verify_token(token):
    return token == API_KEY

@app.route('/status', methods=['GET'])
@auth.login_required
def get_status():
    job_id = request.args.get('job_id')
    if not job_id:
        return jsonify({"error": "Missing job_id"}), 400

    if job_id not in job_status_store:
        return jsonify({"error": "Invalid job_id"}), 404

    return jsonify({"job_id": job_id, "status": job_status_store[job_id]})

@app.route('/start_job', methods=['POST'])
@auth.login_required
def start_job():
    """
    API to start a new translation job.
    """
    job_id = request.json.get('job_id')
    if not job_id:
        return jsonify({"error": "Missing job_id"}), 400

    if job_id in job_status_store:
        return jsonify({"error": "Job already exists"}), 400

    # Start the job status simulation in a separate thread
    thread = threading.Thread(target=JobStatusSimulator.simulate_job_status, args=(job_id, SIMULATED_DELAY, job_status_store))
    thread.start()

    return jsonify({"message": "Job started", "job_id": job_id}), 202

if __name__ == '__main__':
    app.run(debug=True)
