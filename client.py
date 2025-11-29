import socket
import threading
import json
import os
import sys
import time
from config import SERVERS, FILE_MAPPING, BUFFER_SIZE

class Client:
    def __init__(self, port):
        self.host = "localhost"
        self.port = port
        self.cache_dir = f"client_cache_{port}"
        
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            
    def start(self):
        self.start_background_services()
        self.interactive_loop()

    def start_background_services(self):
        # Start listener for invalidations
        threading.Thread(target=self.listen_for_notifications, daemon=True).start()
        print(f"Client started on port {self.port}")
        
        # Register with all servers
        self.register_with_servers()

    def register_with_servers(self):
        for name, info in SERVERS.items():
            try:
                self._send_request(name, {"command": "REGISTER", "host": self.host, "port": self.port})
            except:
                pass # Server might be down

    def listen_for_notifications(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        
        while True:
            conn, addr = s.accept()
            data = conn.recv(BUFFER_SIZE).decode()
            if data:
                req = json.loads(data)
                if req.get("command") == "INVALIDATE":
                    self.handle_invalidation(req["filename"])
            conn.close()

    def handle_invalidation(self, filename):
        filepath = os.path.join(self.cache_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"\n[Notification] Cache invalidated for {filename}")

    def interactive_loop(self):
        print("\nCommands: READ <filename>, WRITE <filename> <content>, EXIT")
        while True:
            try:
                cmd = input("> ").strip().split(" ", 2)
                if not cmd: continue
                
                op = cmd[0].upper()
                
                if op == "EXIT":
                    break
                elif op == "READ":
                    if len(cmd) < 2:
                        print("Usage: READ <filename>")
                        continue
                    content, source = self.read_file(cmd[1])
                    if content:
                        print(f"[{source}] Content: {content}")
                elif op == "WRITE":
                    if len(cmd) < 3:
                        print("Usage: WRITE <filename> <content>")
                        continue
                    resp = self.write_file(cmd[1], cmd[2])
                    if resp:
                        print(f"Response: {resp.get('message')}")
                else:
                    print("Unknown command")
            except KeyboardInterrupt:
                break

    def read_file(self, filename):
        # 1. Check Cache
        filepath = os.path.join(self.cache_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return f.read(), "CACHE HIT"

        # 2. Fetch from Primary (or any)
        print("[CACHE MISS] Fetching from server...")
        primary = FILE_MAPPING.get(filename)
        if not primary:
            print("Unknown file (no primary mapping)")
            return None, "ERROR"

        response = self._send_request(primary, {"command": "READ", "filename": filename})
        
        if response and response["status"] == "OK":
            content = response["content"]
            # Update Cache
            with open(filepath, "w") as f:
                f.write(content)
            return content, "SERVER"
        else:
            print(f"Error: {response.get('message', 'Unknown error')}")
            return None, "ERROR"

    def write_file(self, filename, content):
        primary = FILE_MAPPING.get(filename)
        if not primary:
            print("Unknown file (no primary mapping)")
            return {"status": "ERROR", "message": "Unknown file"}
            
        print(f"Sending write to Primary ({primary})...")
        return self._send_request(primary, {"command": "WRITE", "filename": filename, "content": content})

    def _send_request(self, server_name, data):
        info = SERVERS.get(server_name)
        if not info: return None
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((info["host"], info["port"]))
            s.send(json.dumps(data).encode())
            resp = json.loads(s.recv(BUFFER_SIZE).decode())
            s.close()
            return resp
        except Exception as e:
            print(f"Connection failed to {server_name}: {e}")
            return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python client.py <Client Port>")
        sys.exit(1)
        
    port = int(sys.argv[1])
    client = Client(port)
    client.start()
