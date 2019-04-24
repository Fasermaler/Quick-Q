#!/usr/bin/env bash

echo "This will now update QuQ!"

cd ~

git clone https://github.com/Fasermaler/Quick-Q

echo "Clone successful!"

echo "Attempting to initialize..."

cd ~/Quick-Q

python3 main.py

