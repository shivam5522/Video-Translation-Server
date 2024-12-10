import socketio


# The WebSocketClient is used to implement the client side implementation for using websockets and receiving the status from the server.
class WebSocketClient:
    def __init__(self, ws_url, api_key):
        self.sio = socketio.Client()
        self.api_key = api_key
        self.ws_url = ws_url
        self.job_id = None

        # Register event handlers
        self.sio.on("connect", self.handle_connect)
        self.sio.on("disconnect", self.handle_disconnect)

    def subscribe_to_job(self, job_id):
        """
        Subscribe to updates for a specific job
        """
        self.job_id = job_id
        self.sio.on(f"status_update/{job_id}", self.handle_status_update)

    def handle_connect(self):
        print("WebSocket connection opened.")
        # Subscribe to the /get_status endpoint after connecting
        self.sio.emit("subscribe", {"endpoint": "/get_status"})

    def handle_status_update(self, data):
        print(f"Status update received for job {self.job_id}: {data}")
        if data["status"]["status"] == "completed":
            self.sio.disconnect()

    def handle_disconnect(self):
        print("WebSocket connection closed.")

    def connect(self):
        """
        Establish the WebSocket connection with the server.
        """
        try:
            self.sio.connect(
                f"{self.ws_url}?auth_token={self.api_key}"
            )
        except Exception as e:
            print(f"Error connecting to WebSocket: {e}")
            raise

    def listen(self):
        """
        Keep the WebSocket client listening for messages.
        """
        try:
            self.sio.wait()
        except KeyboardInterrupt:
            print("Stopping WebSocket listener.")
            self.sio.disconnect()
