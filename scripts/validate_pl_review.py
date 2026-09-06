#!/usr/bin/env python3
"""Validate PL review evidence for every approved route (fail closed).

Unlike the M02-I01/I02 foundation gate (evidence_path existence only),
this checks the evidence record's actual content: schema shape, that it
binds the CURRENT RU source hash and the CURRENT PL content file bytes,
that terminology is current, and that the recorded decision is approved.
A route whose evidence fails any of these must not publish.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jsonschema import Draft202012Validator
from localization import MANIFEST_DIR, ROOT, Routes, read_json, sha256

SCHEMA_PATH = ROOT / "manifest" / "schemas" / "pl_review.schema.json"
TERMINOLOGY_PATH = MANIFEST_DIR / "pl_terminology.json"


def validate() -> int:
    schema = read_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    routes = Routes()
    terminology_sha256 = sha256(TERMINOLOGY_PATH)
    checked = 0

    for page_id, page in routes.pages.items():
        variant = page["variants"].get("pl")
        if not variant or variant["status"] != "approved":
            continue

        record_path = ROOT / variant["evidence_path"]
        record = read_json(record_path)
        validator.validate(record)

        assert record["page_id"] == page_id, \
            f"{record_path}: page_id {record['page_id']!r} != route {page_id!r}"
        assert record["unit"]["source_path"] == page["source"]["path"], \
            f"{record_path}: unit.source_path does not match route source path"
        assert record["unit"]["source_sha256"] == page["source"]["sha256"], \
            f"{record_path}: evidence source_sha256 is stale against the current RU source"
        assert record["unit"]["target_source_path"] == variant["source_path"], \
            f"{record_path}: unit.target_source_path does not match route source_path"

        target_file = ROOT / record["unit"]["target_source_path"]
        assert target_file.is_file(), f"{record_path}: target_source_path does not exist"
        assert sha256(target_file) == record["unit"]["target_sha256"], (
            f"{record_path}: PL content file changed since this evidence was recorded "
            f"({record['unit']['target_source_path']})"
        )
        assert record["unit"]["rendered_output_path"] == variant["path"], \
            f"{record_path}: unit.rendered_output_path does not match route path"

        assert record["terminology"]["contract_sha256"] == terminology_sha256, \
            f"{record_path}: terminology contract hash is stale against pl_terminology.json"

        assert all(v == "pass" for v in record["checks"].values()), \
            f"{record_path}: not every check is 'pass'"
        for section in record.get("sections", []):
            assert section["status"] == "pass", \
                f"{record_path}: section {section['name']!r} is not 'pass'"

        assert record["decision"]["status"] == "approved", \
            f"{record_path}: decision.status is not 'approved'"

        checked += 1

    print(f"PASS: PL review evidence valid for {checked} approved page(s)")
    return checked


if __name__ == "__main__":
    validate()
