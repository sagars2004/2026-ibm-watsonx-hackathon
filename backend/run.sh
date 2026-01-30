#!/bin/bash
# Start the Silent Bottleneck Detector backend server

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the Flask app
export FLASK_ENV=development
export USE_MOCK_AI=true
python app.py
