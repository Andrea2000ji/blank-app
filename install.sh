#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installation complete. Run the app with:"
echo "  streamlit run streamlit_app.py"
