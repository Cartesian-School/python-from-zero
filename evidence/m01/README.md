# M01 review evidence

Completed unit review records belong in `evidence/m01/reviews/` and must conform
to the binding rubric and schema defined by M01-I02.

Use one immutable JSON record per unit revision. Recommended filename:

```text
<inventory-ref-normalized>-rNNN.json
```

Do not place placeholders, partially completed records, or fabricated approvals in
the reviews directory. Work-in-progress notes belong outside the authoritative
evidence collection.

Validate records with:

```bash
python scripts/validate_ru_content_review.py --require-records \
  evidence/m01/reviews/<record>.json
```

The directory intentionally contains no review records after M01-I02. The first
authoritative records will be created by the Chapter 1 pilot in M01-I03.
