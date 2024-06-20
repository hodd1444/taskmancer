#!/bin/sh

# Script to quickly install all pip dependencies

# Check if python is installed
if ! [ -x "$(command -v python)" ]; then
  echo 'Error: python is not installed.' >&2
  exit 1
fi

# Check if pip is installed
if ! [ -x "$(command -v pip)" ]; then
  echo 'Error: pip is not installed.' >&2
  exit 1
fi

echo "Installing all dependencies..."
pip install --break-system-packages -r requirements.txt
