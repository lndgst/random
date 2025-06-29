#!/bin/bash
set -e
pyinstaller --onefile --windowed \
  --name Giffer \
  --add-data "gif_app/templates:gif_app/templates" \
  gif_app/app.py
