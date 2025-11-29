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
1. Start the 3 servers.
2. Run the client to perform operations.
# DFMS
