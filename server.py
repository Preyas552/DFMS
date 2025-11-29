import socket
import threading
import json
import os
import sys
import time
from config import SERVERS, FILE_MAPPING, QUORUM_SIZE, BUFFER_SIZE

class StorageServer:
    def __init__(self, name):
        self.name = name
        self.host = SERVERS[name]["host"]
        self.port = SERVERS[name]["port"]
        self.storage_dir = f"storage_{name.replace(' ', '_')}"
        self.clients = set() # Set of (host, port) for invalidation
        
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"[{self.name}] Server started on {self.host}:{self.port}")
        
        while True:
            client_sock, addr = server_socket.accept()
            # print(f"[{self.name}] Connection from {addr}")
            threading.Thread(target=self.handle_connection, args=(client_sock, addr)).start()

    def handle_connection(self, conn, addr):
        try:
            data = conn.recv(BUFFER_SIZE).decode()
            if not data:
                return
            
            request = json.loads(data)
            command = request.get("command")
            
            response = {"status": "ERROR", "message": "Unknown command"}
            
            if command == "READ":
                response = self.handle_read(request)
            elif command == "WRITE":
                response = self.handle_write(request)
            elif command == "REPLICATE":
                response = self.handle_replicate(request)
            elif command == "REGISTER":
                self.clients.add((request["host"], request["port"]))
                response = {"status": "OK", "message": "Registered for invalidation"}
            
            conn.send(json.dumps(response).encode())
        except Exception as e:
            print(f"[{self.name}] Error: {e}")
            conn.send(json.dumps({"status": "ERROR", "message": str(e)}).encode())
        finally:
            conn.close()

    def handle_read(self, request):
        filename = request["filename"]
        filepath = os.path.join(self.storage_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
            return {"status": "OK", "content": content}
        else:
            return {"status": "ERROR", "message": "File not found"}

    def handle_write(self, request):
        filename = request["filename"]
        content = request["content"]
        
        # Check if I am the primary
        primary = FILE_MAPPING.get(filename)
        if primary != self.name:
            return {"status": "ERROR", "message": f"I am not the primary for {filename}. Primary is {primary}"}
        
        # 1. Write locally (Prepare)
        self._write_to_disk(filename, content)
        
        # 2. Replicate to others (Quorum)
        acks = 1 # Count myself
        
        for server_name, server_info in SERVERS.items():
            if server_name == self.name:
                continue
                
            if self._send_replicate(server_info, filename, content):
                acks += 1
        
        if acks >= QUORUM_SIZE:
            # 3. Notify Clients (Invalidation)
            self._notify_clients(filename)
            return {"status": "OK", "message": f"Write successful. Quorum met ({acks}/{len(SERVERS)})"}
        else:
            return {"status": "ERROR", "message": "Quorum failed"}

    def handle_replicate(self, request):
        filename = request["filename"]
        content = request["content"]
        self._write_to_disk(filename, content)
        return {"status": "OK"}

    def _write_to_disk(self, filename, content):
        filepath = os.path.join(self.storage_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"[{self.name}] Wrote {filename}")

    def _send_replicate(self, server_info, filename, content):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server_info["host"], server_info["port"]))
            msg = {"command": "REPLICATE", "filename": filename, "content": content}
            s.send(json.dumps(msg).encode())
            resp = json.loads(s.recv(BUFFER_SIZE).decode())
            s.close()
            return resp.get("status") == "OK"
        except Exception as e:
            print(f"[{self.name}] Replication failed to {server_info['port']}: {e}")
            return False

    def _notify_clients(self, filename):
        # In a real app, we'd connect to registered clients.
        # For this simulation, we'll just print or try to connect if we had client info.
        # We'll assume clients are listening on a specific range or we skip actual push for now 
        # unless the user asks for the full push implementation.
        # The requirement says "Cached copies at client devices are invalidated."
        # I'll implement a simple broadcast if I have registered clients.
        for client_host, client_port in self.clients:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((client_host, client_port))
                msg = {"command": "INVALIDATE", "filename": filename}
                s.send(json.dumps(msg).encode())
                s.close()
            except:
                pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <Server Name>")
        sys.exit(1)
    
    server_name = sys.argv[1]
    if server_name not in SERVERS:
        print(f"Invalid server name. Choose from: {list(SERVERS.keys())}")
        sys.exit(1)
        
    server = StorageServer(server_name)
    server.start()
