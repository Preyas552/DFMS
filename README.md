# Distributed File Storage System (DFSS)

## Overview
This project implements a simplified distributed file storage system with the following features:
- **3 Data Centers**: New York, Toronto, London.
- **Primary-Based Consistency**: Each file has a designated primary server.
- **Replication**: Updates are propagated to all replicas.
- **Quorum Consistency**: Writes require acknowledgement from 2/3 servers.
- **Client-Side Caching**: Clients cache files with invalidation on updates.

## Architecture

### Servers
- **New York**: Port 8000
- **Toronto**: Port 8001
- **London**: Port 8002

### Consistency Model
- **Writes**: Client -> Primary -> Replicas. (Quorum = 2).
- **Reads**: Client -> Cache -> Any Server.

## Project Structure
- `server.py`: The server node implementation.
- `client.py`: The client implementation with caching.
- `config.py`: Configuration (ports, mappings).
- `utils.py`: Helper functions (logging, networking).

## Usage
### CLI Mode
1. Start servers: `python3 server.py "New York"` (etc)
2. Run client: `python3 client.py 9000`

### Web UI (Recommended)
1. Run the all-in-one script:
   ```bash
   ./run_system.sh
   ```
   This will start:
   - 3 Storage Servers
   - Web Client Middleware (Port 3000)
   - React Frontend (Port 5173)
2. Open `http://localhost:5173` in your browser.

## Requirements
- Python 3
- Node.js & npm

# DFMS
