#!/bin/bash
set -e

# Setup directories
mkdir -p /opt/tesseract/bin /opt/tesseract/share/tessdata

# Architecture target detection (either from TARGETARCH environment variable or host uname)
ARCH="${TARGETARCH:-$(uname -m)}"

echo "Downloading static Tesseract binary for architecture: $ARCH..."

if [ "$ARCH" = "x86_64" ] || [ "$ARCH" = "amd64" ]; then
    curl -L -o /opt/tesseract/bin/tesseract https://github.com/DanielMYT/tesseract-static/releases/download/tesseract-5.5.2/tesseract.x86_64
elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    curl -L -o /opt/tesseract/bin/tesseract https://github.com/DanielMYT/tesseract-static/releases/download/tesseract-5.5.2/tesseract.aarch64
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

chmod +x /opt/tesseract/bin/tesseract

echo "Downloading English traineddata..."
curl -L -o /opt/tesseract/share/tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

echo "Tesseract installation completed successfully."
