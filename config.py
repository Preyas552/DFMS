
# Configuration for Distributed File Storage System

# Server Details
SERVERS = {
    "New York": {"host": "localhost", "port": 8000},
    "Toronto": {"host": "localhost", "port": 8001},
    "London":   {"host": "localhost", "port": 8002}
}

# File to Primary Server Mapping
# In a real system, this might be a hash ring. Here it's static as per requirements.
FILE_MAPPING = {
    "file1.txt": "New York",
    "file2.txt": "Toronto",
    "file3.txt": "London"
}

# System Constants
QUORUM_SIZE = 2
REPLICA_COUNT = 3
BUFFER_SIZE = 4096
