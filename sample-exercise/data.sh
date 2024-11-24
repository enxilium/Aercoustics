#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"


python -m pip install zenodo-get

python -m zenodo_get 10.5281/zenodo.7244360 -m -e -k

LABEL_ZIP_FILE="${SCRIPT_DIR}/development_annotation.zip"
unzip "$LABEL_ZIP_FILE" -d "${SCRIPT_DIR}/data/"

AUDIO_ZIP_FILE="${SCRIPT_DIR}/development_audio.zip"
unzip "$AUDIO_ZIP_FILE" -d "${SCRIPT_DIR}/data/"

rm "$AUDIO_ZIP_FILE"
rm "$LABEL_ZIP_FILE"
rm "${SCRIPT_DIR}/LICENSE.txt"
rm "${SCRIPT_DIR}/md5sums.txt"

python maestro_real.py

rm -rf "${SCRIPT_DIR}/data/development_annotation"
rm -rf "${SCRIPT_DIR}/data/development_audio"

echo "Done with the Train, Val, Test"
