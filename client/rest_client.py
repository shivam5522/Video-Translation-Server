import time

import requests


class RestClient:
    """
    Class: RestClient (Used to invoke a client that would make calls to check the status of video translation)
    Methods: start_job , arguments = job_id
             get_status, arguments = job_id
             wait_for_completion, arguments = job_id, initial_delay (optional), max_delay (optional)
    """

    # __init__ initializes the base_url and api_key.
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    # Start job calls the POST api which creates the job and starts the processing(simulated)
    def start_job(self, job_id):
        """
        Starts a new translation job.
        """
        response = requests.post(
            f"{self.base_url}/start_job", json={"job_id": job_id}, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    # Get status gives the status of the job (ie: The video translation). It only takes the job_id to check the job status
    def get_status(self, job_id):
        """
        Gets the status of a translation job.
        """
        response = requests.get(
            f"{self.base_url}/status", params={"job_id": job_id}, headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    # This is a wrapper function to simulate the clients queries, but one intelligent thing that this uses is Adaptive Polling.
    def wait_for_completion(self, job_id, initial_delay=2, max_delay=10):
        """
        Waits for a job to complete.
        """
        delay = initial_delay
        while True:
            status = self.get_status(job_id)["status"]

            print(f"Job {job_id} status: {status}")

            if status in {"completed", "error"}:
                return status

            time.sleep(delay)
            delay = min(delay * 2, max_delay)
