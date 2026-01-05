#!/bin/bash
# Script to download Vosk models for speech recognition
# Models: Russian (vosk-model-small-ru-0.22), Kazakh (vosk-model-small-kz-0.15)
#
# Usage:
#   chmod +x download_models.sh
#   ./download_models.sh
#
# For Windows: Use Git Bash or WSL to run this script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
MODELS_DIR="$PROJECT_ROOT/../models"

echo "=== Vosk Models Downloader ==="
echo "Models directory: $MODELS_DIR"
echo ""

# Create models directory
mkdir -p "$MODELS_DIR"
cd "$MODELS_DIR"

# Russian model
RUSSIAN_MODEL="vosk-model-small-ru-0.22"
RUSSIAN_URL="https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip"

if [ -d "$RUSSIAN_MODEL" ]; then
    echo "[OK] Russian model already exists: $RUSSIAN_MODEL"
else
    echo "[DOWNLOADING] Russian model: $RUSSIAN_MODEL"
    wget -q --show-progress "$RUSSIAN_URL" -O "${RUSSIAN_MODEL}.zip"
    echo "[EXTRACTING] $RUSSIAN_MODEL..."
    unzip -q "${RUSSIAN_MODEL}.zip"
    rm "${RUSSIAN_MODEL}.zip"
    echo "[OK] Russian model installed"
fi

echo ""

# Kazakh model
KAZAKH_MODEL="vosk-model-small-kz-0.15"
KAZAKH_URL="https://alphacephei.com/vosk/models/vosk-model-small-kz-0.15.zip"

if [ -d "$KAZAKH_MODEL" ]; then
    echo "[OK] Kazakh model already exists: $KAZAKH_MODEL"
else
    echo "[DOWNLOADING] Kazakh model: $KAZAKH_MODEL"
    # Note: Kazakh model may not be available at this URL
    # Check https://alphacephei.com/vosk/models for available models
    if wget -q --spider "$KAZAKH_URL" 2>/dev/null; then
        wget -q --show-progress "$KAZAKH_URL" -O "${KAZAKH_MODEL}.zip"
        echo "[EXTRACTING] $KAZAKH_MODEL..."
        unzip -q "${KAZAKH_MODEL}.zip"
        rm "${KAZAKH_MODEL}.zip"
        echo "[OK] Kazakh model installed"
    else
        echo "[WARNING] Kazakh model not available at: $KAZAKH_URL"
        echo "         Check https://alphacephei.com/vosk/models for available Kazakh models"
        echo "         You may need to download it manually"
    fi
fi

echo ""
echo "=== Download Complete ==="
echo "Models installed in: $MODELS_DIR"
ls -la "$MODELS_DIR"
