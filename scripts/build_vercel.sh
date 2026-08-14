#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${ROOT_DIR}/dist"

echo "==> Building Cartesian School Python deployment"

rm -rf "${DIST_DIR}"
mkdir -p "${DIST_DIR}"
mkdir -p "${DIST_DIR}/downloads"
mkdir -p "${DIST_DIR}/notebooks"
mkdir -p "${DIST_DIR}/projects"

# Main educational HTML website.
cp -a "${ROOT_DIR}/site/." "${DIST_DIR}/"

# Publication downloads.
cp "${ROOT_DIR}/book/pdf/gotovaya-kniga.pdf"    "${DIST_DIR}/downloads/gotovaya-kniga.pdf"

cp "${ROOT_DIR}/book/epub/python-s-nulya.epub"    "${DIST_DIR}/downloads/python-s-nulya.epub"

# Jupyter practice.
cp -a "${ROOT_DIR}/notebooks/."       "${DIST_DIR}/notebooks/"

# Complete educational project source code.
cp -a "${ROOT_DIR}/projects/."       "${DIST_DIR}/projects/"

echo "==> Build completed"
echo "Output: ${DIST_DIR}"
