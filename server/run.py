#!/usr/bin/env python
"""
Entry point for running the OCR server
"""
import sys
import os

# Add parent directory to path so we can import src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import create_app

if __name__ == '__main__':
    app = create_app()
    print('Starting OCR Flask server on port 3000...')
    app.run(host='0.0.0.0', port=3000, debug=False)
