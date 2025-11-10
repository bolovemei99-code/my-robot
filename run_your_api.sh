#!/bin/bash

# Install dependencies
pip install -q -r requirements.txt

# Run the Flask app in the background
python main.py &

# Wait for the API to be ready
echo "Waiting for API to start..."
for i in {1..30}; do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "API is ready!"
        exit 0
    fi
    sleep 1
done

echo "Warning: API may not be fully ready, but continuing..."
exit 0
