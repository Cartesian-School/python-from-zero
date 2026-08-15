#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${ROOT_DIR}/dist"

echo "==> Building Cartesian School Python deployment"

echo "==> Validating manifest/practice_manifest.json"
python3 "${ROOT_DIR}/scripts/validate_practice_manifest.py"

echo "==> Generating SEO metadata, sitemap.xml, llms-full.txt"
python3 "${ROOT_DIR}/scripts/build_seo_meta.py"
python3 "${ROOT_DIR}/scripts/build_sitemap.py"
python3 "${ROOT_DIR}/scripts/build_llms_full.py"

rm -rf "${DIST_DIR}"
mkdir -p "${DIST_DIR}"
mkdir -p "${DIST_DIR}/book/pdf"
mkdir -p "${DIST_DIR}/book/epub"
mkdir -p "${DIST_DIR}/notebooks"
mkdir -p "${DIST_DIR}/projects"

# Main educational HTML website — this also carries the interactive practice
# system (site/practice/<lesson-id>/, site/assets/js/practice.bundle.js,
# site/assets/js/python-worker.mjs), since those are generated/committed under
# site/ the same way site/chapters/*.html are. No separate build step needed
# here; see scripts/build_practice_pages.py and web/ for how they're produced.
cp -a "${ROOT_DIR}/site/." "${DIST_DIR}/"

# Publication downloads — paths must match the relative links already used in
# site/index.html ("../book/pdf/..." and "../book/epub/..."), which resolve to
# /book/pdf/... and /book/epub/... once site/ is deployed at the domain root.
cp "${ROOT_DIR}/book/pdf/готовая книга.pdf"      "${DIST_DIR}/book/pdf/готовая книга.pdf"
cp "${ROOT_DIR}/book/epub/python-s-nulya.epub"    "${DIST_DIR}/book/epub/python-s-nulya.epub"

# Jupyter practice — referenced from chapter pages via "../../../notebooks/...".
cp -a "${ROOT_DIR}/notebooks/."       "${DIST_DIR}/notebooks/"

# Complete educational project source code — referenced via "../../../projects/...".
cp -a "${ROOT_DIR}/projects/."       "${DIST_DIR}/projects/"

echo "==> Validating navigation (local links, fragments, canonical hosts)"
python3 "${ROOT_DIR}/scripts/validate_navigation.py" "${DIST_DIR}"

echo "==> Validating site catalogs (homepage anchors, chapters, practice, projects)"
python3 "${ROOT_DIR}/scripts/validate_site_catalogs.py" "${DIST_DIR}"

echo "==> Validating SEO metadata"
python3 "${ROOT_DIR}/scripts/validate_seo.py" "${DIST_DIR}"

echo "==> Build completed"
echo "Output: ${DIST_DIR}"
