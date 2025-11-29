import threading
import time
import os
import shutil
from server import StorageServer
from client import Client
from config import SERVERS

def clean_dirs():
    for name in SERVERS:
        d = f"storage_{name.replace(' ', '_')}"
        if os.path.exists(d):
            shutil.rmtree(d)
    if os.path.exists("client_cache_9000"):
        shutil.rmtree("client_cache_9000")

def run_server(name):
    s = StorageServer(name)
    s.start()

def test_integration():
    clean_dirs()
    
    # Start Servers
    threads = []
    for name in SERVERS:
        t = threading.Thread(target=run_server, args=(name,), daemon=True)
        t.start()
        threads.append(t)
        
    time.sleep(1) # Wait for servers to start
    
    # Start Client
    # We won't use the interactive loop, just the class methods
    c = Client(9000)
    # Start listener in background
    threading.Thread(target=c.listen_for_notifications, daemon=True).start()
    c.register_with_servers()
    
    print("\n--- TEST: Write file1.txt (Primary: New York) ---")
    c.write_file("file1.txt", "Hello Distributed World!")
    
    time.sleep(1) # Wait for replication
    
    # Verify Replication
    print("\n--- VERIFICATION ---")
    for name in SERVERS:
        d = f"storage_{name.replace(' ', '_')}"
        f = os.path.join(d, "file1.txt")
        if os.path.exists(f):
            with open(f, "r") as file:
                print(f"[{name}] Content: {file.read()}")
        else:
            print(f"[{name}] File NOT found!")

    print("\n--- TEST: Read file1.txt (Should be cached) ---")
    c.read_file("file1.txt")
    
    # Verify Cache
    if os.path.exists("client_cache_9000/file1.txt"):
        print("Client Cache: EXISTS")
    else:
        print("Client Cache: MISSING")

    print("\n--- TEST: Update file1.txt (Should invalidate cache) ---")
    c.write_file("file1.txt", "Updated Content")
    
    time.sleep(1) # Wait for invalidation
    
    if not os.path.exists("client_cache_9000/file1.txt"):
        print("Client Cache: INVALIDATED (Success)")
    else:
        print("Client Cache: STILL EXISTS (Failure)")

if __name__ == "__main__":
    test_integration()
