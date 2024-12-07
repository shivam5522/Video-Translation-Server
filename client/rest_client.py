import time

import requests


class RestClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def start_job(self, job_id):
        """
        Starts a new translation job.
        """
        response = requests.post(
            f"{self.base_url}/start_job", json={"job_id": job_id}, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_status(self, job_id):
        """
        Gets the status of a translation job.
        """
        response = requests.get(
            f"{self.base_url}/status", params={"job_id": job_id}, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def wait_for_completion(self, job_id, initial_delay=2, max_delay=10):
        """
        Waits for a job to complete using adaptive polling.
        """
        delay = initial_delay
        while True:
            status = self.get_status(job_id)["status"]
            print(f"Job {job_id} status: {status}")

            if status in {"completed", "error"}:
                return status

            time.sleep(delay)
            delay = min(delay * 2, max_delay)
