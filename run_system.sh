#!/bin/bash

# Kill background processes on exit
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

echo "Starting Storage Servers..."
./venv/bin/python3 server.py "New York" &
./venv/bin/python3 server.py "Toronto" &
./venv/bin/python3 server.py "London" &

sleep 2

echo "Starting Web Client Middleware..."
./venv/bin/python3 web_client.py &

sleep 2

echo "Starting Frontend..."
cd ui
npm run dev

wait
