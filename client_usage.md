## Client Library Usage

This client library provides an interface to interact with two different servers using WebSockets. WebSockets offer a persistent connection between the client and the server, eliminating the need for the client to make multiple HTTP requests. This results in reduced latency and more efficient communication.

### How to Use

1. **Initialize the Client:**
    - Create an instance of the client library.
    - Provide the necessary configuration, such as server URLs and authentication tokens if required.

2. **Connect to Servers:**
    - Use the provided methods to establish WebSocket connections to both servers.
    - Ensure that the connections are successfully established before proceeding with further operations.

3. **Send and Receive Messages:**
    - Utilize the methods to send messages to the servers.
    - Implement event listeners to handle incoming messages from the servers.

4. **Handle Connection Events:**
    - Monitor connection status events such as open, close, and error.
    - Implement reconnection logic if necessary to maintain a stable connection.

### Example
    - REST implementation for client
```python
client = RestClient(base_url=f"http://{os.getenv("BASE_URL")}:5000", api_key=os.getenv("API_KEY")) # This initializes a client
job_id = str(uuid.uuid4())  # Randomly creates a job ID
print("Starting job...")
client.start_job(job_id)  # Used to initiate a job
print("Waiting for job to complete...")
status = client.wait_for_completion(job_id)  #Here is waits for completion by using adaptive polling and asks for status in variable wait times
print(f"Final job status: {status}")
```

    - WebSocket implementation
```python
ws_url = f"ws://{os.getenv('BASE_URL')}:5002"
client = WebSocketClient(ws_url=ws_url, api_key=os.getenv("API_KEY"))  # Initializes a client to connect to server through websocket
print("Connecting to WebSocket...")
client.connect() # Here you connect to the server through the initialized client
job_id = str(uuid.uuid4())
print(f"Starting job with ID: {job_id}...")
client.subscribe_to_job(job_id)     # This is used so that the client binds to the job_status endpoint
response = requests.post(
    f"http://{os.getenv('BASE_URL')}:5002/start_job",
    json={"job_id": job_id},
    headers={"Authorization": f"Bearer {os.getenv('API_KEY')}"},
)    # HTTP request to initiate the job
if response.status_code == 202:
    print(f"Job {job_id} started successfully.")
else:
    print(f"Failed to start job. Error: {response.text}")
    return 
print("Listening for job updates...")
client.listen()   # Now the client finally listens to the job_status endpoint
```
