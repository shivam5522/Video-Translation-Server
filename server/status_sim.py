import time

class JobStatusSimulator:
    @staticmethod
    def simulate_job_status(job_id, delay, store):
        # This simulates job status transitions from 'pending' to either 'completed' or 'error'.
        store[job_id] = "pending"
        time.sleep(delay)
        store[job_id] = "completed"  # Default transition
