# Implementation Plan - Distributed File Storage Web UI

This plan outlines the steps to add a modern, premium web interface to the Distributed File Storage System (DFSS). The web interface will act as a "Client" in the distributed system, communicating with the existing storage servers via a Python middleware.

## Architecture
- **Frontend**: React (Vite) for a dynamic, responsive UI.
- **Middleware**: Python FastAPI server. This acts as the "Client Device". It holds the local cache and communicates with the Storage Servers (New York, Toronto, London) using the existing socket protocol.
- **Backend**: Existing `server.py` instances (unchanged).

## User Interface Design
- **Visual Style**: Dark mode, glassmorphism, vibrant accent colors (Neon Blue/Purple).
- **Components**:
    - **Network Status**: Visual indicators for the 3 Data Centers (Online/Offline).
    - **File Explorer**: Grid/List view of files.
    - **Activity Log**: A scrolling terminal-like view showing "Quorum reached", "Replicating to London", "Cache Invalidated", etc.
    - **Actions**: "Upload File" (Write) and "Open File" (Read).

## Proposed Steps

### Phase 1: Middleware (Python API)
1.  **Create `web_client.py`**: A modified version of `client.py` that runs as a FastAPI app.
    -   Remove `interactive_loop`.
    -   Expose endpoints:
        -   `GET /api/status`: Check connection to servers.
        -   `GET /api/files`: List files (from cache or query primary).
        -   `GET /api/files/{name}`: Read file content (Read operation).
        -   `POST /api/files`: Write file content (Write operation).
        -   `GET /api/logs`: Stream or poll for logs/events (Cache invalidation events).

### Phase 2: Frontend Setup
2.  **Initialize Vite Project**: Create a new React app in `ui/`.
3.  **Setup Styling**: Configure vanilla CSS with CSS variables for the premium theme (no Tailwind unless requested, per system rules, but I will use vanilla CSS for maximum control as per instructions).

### Phase 3: UI Implementation
4.  **Build Components**:
    -   `ServerNode`: Visual component for a data center.
    -   `FileManager`: Interface to read/write files.
    -   `LogViewer`: Display backend events.
5.  **Integrate API**: Connect React frontend to FastAPI middleware.

### Phase 4: Integration & Polish
6.  **Run Script**: Create a `run_system.sh` to launch all 3 servers, the middleware, and the frontend dev server.
7.  **Aesthetics**: Apply animations (framer-motion or CSS keyframes) for data flow visualization.

## Verification Plan
-   **Manual Test**:
    1.  Start system.
    2.  Upload `test.txt` via UI.
    3.  Verify "Quorum Met" in UI logs.
    4.  Verify file exists in `storage_New_York/`, etc.
    5.  Modify `test.txt` via UI.
    6.  Verify "Cache Invalidated" log.
