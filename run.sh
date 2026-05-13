#!/bin/bash

echo "========================================"
echo "  SentinelLog v2.0"
echo "  Real-time Threat Detection System"
echo "========================================"
echo ""

echo "[1/3] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found!"
    echo "Please install Python 3.8+"
    exit 1
fi
python3 --version
echo ""

echo "[2/3] Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies!"
    exit 1
fi
echo ""

echo "[3/3] Starting SentinelLog server..."
echo ""
echo "========================================"
echo "  Server running at:"
echo "  http://localhost:8000"
echo ""
echo "  Press Ctrl+C to stop"
echo "========================================"
echo ""

python3 main.py
