import time


class JobStatusSimulator:
    @staticmethod
    def simulate_job_status(job_id, delay, store):
        store[job_id] = {"status": "pending", "progress": 0}
        total_steps = 10
        step_delay = delay / total_steps
        
        for i in range(total_steps):
            time.sleep(step_delay)
            store[job_id] = {
                "status": "pending",
                "progress": ((i + 1) * 100) // total_steps     # This is to send the progress in terms of percentage to help the user keep track of the progress.
            }
        
        store[job_id] = {"status": "completed", "progress": 100}
