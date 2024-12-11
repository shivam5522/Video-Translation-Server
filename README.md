# Video Translation Server

## Introduction

The Video Translation Server is a powerful and flexible server designed to handle video translation tasks. It supports both REST and WebSocket protocols, providing real-time progress tracking and detailed status updates. This server is ideal for developers looking to integrate video translation capabilities into their applications with ease.

## Features

- **Dual Protocol Support**: Choose between REST and WebSocket protocols for communication.
- **Real-Time Progress Tracking**: Monitor the progress of video translation tasks in real-time.
- **Detailed Status Updates**: Receive step-by-step status updates for each translation task.
- **Simulation Capabilities**: Built-in job status simulation for testing and development.
- **Modular Design**: Clean and modular code structure for easy maintenance and extension.

## 🚀 Getting Started

### System Requirements
- Python 3.6 or higher
- pip package manager
- Virtual environment (recommended)

### Quick Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/shivam5522/Video-Translation-Server/tree/main
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Configure environment variables:
    - Edit the `.env` file to set the necessary environment variables.

## 💻 Usage Examples

### Running the Servers

You can run either the REST server or the WebSocket server:

- **REST server**: 
    ```sh
    python server/app.py
    ```

- **WebSocket Server**: 
    ```sh
    python server/ws_server.py
    ```

### Integration Tests

To run the integration tests, use the following commands:

- **REST Client Test**:
    ```sh
    python integration_test.py rest
    ```

- **WebSocket Client Test**:
    ```sh
    python integration_test.py ws
    ```

## 📊 Comprehensive Monitoring

### Detailed Progress Tracking
- Real-time progress percentage updates
- Step-by-step status monitoring
- Clear status transitions (pending → completed)
- Granular progress reporting

## 🏗️ Architecture Highlights

### Clean Code Structure
- Modular component design
- Clear separation between REST and WebSocket services
- Easy-to-extend codebase
- Well-documented interfaces

## 🛠️ Developer-Friendly Features

### Simulation Capabilities
- Built-in job status simulation
- Configurable delays and steps
- Perfect for testing and development
- Easy to replace with real job processing

## 📂 Project Structure

### Key Files and Their Roles

- **client/rest_client.py**: Implements the REST client.
- **client/ws_client.py**: Implements the WebSocket client.
- **integration_test.py**: Contains integration tests for both REST and WebSocket clients.
- **server/app.py**: Entry point for the REST server.
- **server/ws_server.py**: Entry point for the WebSocket server.
- **server/config.py**: Configuration settings for the servers.
- **server/status_sim.py**: Simulates job status for testing purposes.

## 🧪 Integration Tests

### REST Client Integration Test

The `test_rest_client` function in [integration_test.py](integration_test.py) performs the following steps:

1. Initializes the `RestClient` with the base URL and API key.
2. Starts a job with a unique job ID.
3. Waits for the job to complete.
4. Prints the final job status.

### WebSocket Client Integration Test

The `test_websocket_client` function in [integration_test.py](integration_test.py) performs the following steps:

1. Initializes the `WebSocketClient` with the WebSocket URL and API key.
2. Connects to the WebSocket server.
3. Starts a job via HTTP with a unique job ID.
4. Listens for job updates.
5. Prints the job status updates.