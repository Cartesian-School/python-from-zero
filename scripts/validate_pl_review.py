#!/usr/bin/env python3
"""Validate PL review evidence for every route that has recorded one (fail closed).

Unlike the M02-I01/I02 foundation gate (evidence_path existence only),
this checks the evidence record's actual content: schema shape, that it
binds the CURRENT RU source hash and the CURRENT PL content file bytes,
that terminology is current, and that the recorded decision is a legitimate
one. A route whose evidence fails any of these must not publish.

This is a release-gating validator (invoked from scripts/build_vercel.sh on
every build), so it uses explicit `raise` statements rather than `assert`:
assertions disappear under `python -O`, which would silently turn this into
a no-op gate. Tests may still use `assert`; this module may not.

Governance model (reviewer vs. decision actor):

  reviewer.reviewer_type   -- who performed the linguistic/technical QA pass;
                               "ai_assistant" is allowed here.
  decision.status           -- "reviewed" (QA complete, pending Product Owner
                               approval), "approved", "rejected", or
                               "needs_rework".
  decision.decider_type     -- who made that decision; "ai_assistant" or
                               "human".

  Binding invariant: decision.status == "approved" REQUIRES
  decision.decider_type == "human". An AI assistant may move evidence to
  "reviewed" but is never allowed to grant final "approved" status -- that
  would be an AI approving its own (or another AI's) work as production-
  ready, which this validator must reject regardless of what routes.json
  currently claims for a page's own `status` field (that field governs
  whether a route is *wired into* the site's routing/switcher/SEO output,
  which is a separate, narrower concept from this human sign-off gate; see
  docs/LOCALIZATION-RU-PL.md).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from jsonschema import Draft202012Validator, FormatChecker
from localization import MANIFEST_DIR, ROOT, Routes, read_json, sha256

SCHEMA_PATH = ROOT / "manifest" / "schemas" / "pl_review.schema.json"
TERMINOLOGY_PATH = MANIFEST_DIR / "pl_terminology.json"

# decision.status values whose evidence may still validate successfully.
# "rejected"/"needs_rework" content must fail closed rather than pass silently.
ACCEPTABLE_DECISION_STATUSES = frozenset({"reviewed", "approved"})


class PLReviewValidationError(ValueError):
    """Raised when PL review evidence is missing, stale, or fails governance."""


def validate() -> int:
    schema = read_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    routes = Routes()
    terminology_sha256 = sha256(TERMINOLOGY_PATH)
    checked = 0

    for page_id, page in routes.pages.items():
        variant = page["variants"].get("pl")
        if not variant or not variant.get("evidence_path"):
            continue

        record_path = ROOT / variant["evidence_path"]
        record = read_json(record_path)
        validator.validate(record)

        if record["page_id"] != page_id:
            raise PLReviewValidationError(
                f"{record_path}: page_id {record['page_id']!r} != route {page_id!r}")
        if record["unit"]["source_path"] != page["source"]["path"]:
            raise PLReviewValidationError(
                f"{record_path}: unit.source_path does not match route source path")
        if record["unit"]["source_sha256"] != page["source"]["sha256"]:
            raise PLReviewValidationError(
                f"{record_path}: evidence source_sha256 is stale against the current RU source")
        if record["unit"]["target_source_path"] != variant["source_path"]:
            raise PLReviewValidationError(
                f"{record_path}: unit.target_source_path does not match route source_path")

        target_file = ROOT / record["unit"]["target_source_path"]
        if not target_file.is_file():
            raise PLReviewValidationError(f"{record_path}: target_source_path does not exist")
        if sha256(target_file) != record["unit"]["target_sha256"]:
            raise PLReviewValidationError(
                f"{record_path}: PL content file changed since this evidence was recorded "
                f"({record['unit']['target_source_path']})"
            )
        if record["unit"]["rendered_output_path"] != variant["path"]:
            raise PLReviewValidationError(
                f"{record_path}: unit.rendered_output_path does not match route path")

        if record["terminology"]["contract_sha256"] != terminology_sha256:
            raise PLReviewValidationError(
                f"{record_path}: terminology contract hash is stale against pl_terminology.json")

        if not all(v == "pass" for v in record["checks"].values()):
            raise PLReviewValidationError(f"{record_path}: not every check is 'pass'")
        for section in record.get("sections", []):
            if section["status"] != "pass":
                raise PLReviewValidationError(
                    f"{record_path}: section {section['name']!r} is not 'pass'")

        decision = record["decision"]
        if decision["status"] not in ACCEPTABLE_DECISION_STATUSES:
            raise PLReviewValidationError(
                f"{record_path}: decision.status is {decision['status']!r} "
                f"(must be one of {sorted(ACCEPTABLE_DECISION_STATUSES)})")
        if decision["status"] == "approved" and decision.get("decider_type") != "human":
            raise PLReviewValidationError(
                f"{record_path}: decision.status is 'approved' but decider_type is "
                f"{decision.get('decider_type')!r} -- AI final approval is not allowed; "
                f"only a human decider may set decision.status to 'approved'"
            )

        checked += 1

    print(f"PASS: PL review evidence valid for {checked} page(s)")
    return checked


if __name__ == "__main__":
    validate()
