from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from client import Client
from config import FILE_MAPPING, SERVERS
import threading
import time
import os

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebClient(Client):
    def __init__(self, port):
        super().__init__(port)
        self.logs = []

    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")
        # Keep last 50 logs
        if len(self.logs) > 50:
            self.logs.pop(0)

    def handle_invalidation(self, filename):
        # Call original to remove file
        super().handle_invalidation(filename)
        # Add log
        self.log(f"Cache Invalidated: {filename}")

# Initialize the client on port 9000 (Web Client Port)
client_instance = WebClient(9000)

@app.on_event("startup")
def startup_event():
    client_instance.start_background_services()
    client_instance.log("Web Client Started")

class WriteRequest(BaseModel):
    filename: str
    content: str

@app.get("/api/status")
def get_status():
    return {
        "status": "Online", 
        "servers": [
            {"name": name, "host": info["host"], "port": info["port"]} 
            for name, info in SERVERS.items()
        ]
    }

@app.get("/api/files")
def get_files():
    # Return list of files. 
    # In a real system, we'd query the servers. 
    # Here we use the static mapping from config.
    return {"files": list(FILE_MAPPING.keys())}

@app.get("/api/files/{filename}")
def read_file(filename: str):
    content, source = client_instance.read_file(filename)
    if source == "ERROR" or content is None:
        raise HTTPException(status_code=404, detail="File not found or error")
    
    client_instance.log(f"Read {filename} from {source}")
    return {"filename": filename, "content": content, "source": source}

@app.post("/api/files")
def write_file(req: WriteRequest):
    resp = client_instance.write_file(req.filename, req.content)
    if resp and resp.get("status") == "OK":
        client_instance.log(f"Wrote {req.filename} (Quorum Met)")
        return resp
    else:
        msg = resp.get("message") if resp else "Unknown Error"
        client_instance.log(f"Write Failed: {req.filename} - {msg}")
        raise HTTPException(status_code=500, detail=msg)

@app.get("/api/logs")
def get_logs():
    return {"logs": client_instance.logs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
