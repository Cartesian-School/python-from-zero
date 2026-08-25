#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="${ROOT_DIR}/dist"

if [[ -n "${PYTHON_BIN:-}" ]]; then
  PYTHON="${PYTHON_BIN}"
elif [[ -x "${ROOT_DIR}/.venv/bin/python" ]]; then
  PYTHON="${ROOT_DIR}/.venv/bin/python"
else
  PYTHON="python3"
fi

echo "==> Building Cartesian School Python deployment"

echo "==> Validating manifest/practice_manifest.json"
"${PYTHON}" "${ROOT_DIR}/scripts/validate_practice_manifest.py"

echo "==> Validating data/chapter-23-official-sources.json"
"${PYTHON}" "${ROOT_DIR}/scripts/validate_chapter23_sources.py"

echo "==> Validating projects/python/safesort/ upstream sync"
"${PYTHON}" "${ROOT_DIR}/scripts/validate_safesort_upstream_sync.py"

echo "==> Validating generated Chapter 23 academic contracts"
"${PYTHON}" "${ROOT_DIR}/scripts/validate_chapter23_outputs.py"

echo "==> Validating Chapter 23 notebooks and graders"
if [[ "${CHAPTER23_VALIDATION_MODE:-full}" == "portable" ]]; then
  "${PYTHON}" "${ROOT_DIR}/scripts/validate_chapter23_practices.py" --portable
elif [[ "${CHAPTER23_VALIDATION_MODE:-full}" == "full" ]]; then
  "${PYTHON}" "${ROOT_DIR}/scripts/validate_chapter23_practices.py"
else
  echo "Unsupported CHAPTER23_VALIDATION_MODE: ${CHAPTER23_VALIDATION_MODE}" >&2
  exit 2
fi

echo "==> Generating SEO metadata, sitemap.xml, llms-full.txt"
"${PYTHON}" "${ROOT_DIR}/scripts/build_seo_meta.py"
"${PYTHON}" "${ROOT_DIR}/scripts/build_sitemap.py"
"${PYTHON}" "${ROOT_DIR}/scripts/build_llms_full.py"

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
"${PYTHON}" "${ROOT_DIR}/scripts/validate_navigation.py" "${DIST_DIR}"

echo "==> Validating site catalogs (homepage anchors, chapters, practice, projects)"
"${PYTHON}" "${ROOT_DIR}/scripts/validate_site_catalogs.py" "${DIST_DIR}"

echo "==> Validating SEO metadata"
"${PYTHON}" "${ROOT_DIR}/scripts/validate_seo.py" "${DIST_DIR}"

echo "==> Build completed"
echo "Output: ${DIST_DIR}"
