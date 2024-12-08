import socketio


class WebSocketClient:
    def __init__(self, ws_url, api_key):
        self.sio = socketio.Client()
        self.api_key = api_key
        self.ws_url = ws_url

        # Register event handlers
        self.sio.on("connect", self.handle_connect)
        self.sio.on("status_update", self.handle_status_update)
        self.sio.on("disconnect", self.handle_disconnect)

    def handle_connect(self):
        print("WebSocket connection opened.")
        # Subscribe to the /get_status endpoint after connecting
        self.sio.emit("subscribe", {"endpoint": "/get_status"})

    def handle_status_update(self, data):
        print(f"Status update received: {data}")
        self.sio.disconnect()

    def handle_disconnect(self):
        print("WebSocket connection closed.")

    def connect(self):
        """
        Establish the WebSocket connection with the server.
        """
        try:
            self.sio.connect(
                self.ws_url, headers={"Authorization": f"Bearer {self.api_key}"}
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
