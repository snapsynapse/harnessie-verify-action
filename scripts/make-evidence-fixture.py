#!/usr/bin/env python3
"""Create a deterministic CI-only evidence bundle outside the checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", required=True, type=Path)
    parser.add_argument("--evidence-root", required=True, type=Path)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()

    args.evidence_root.mkdir(parents=True, exist_ok=True)
    proof = args.evidence_root / "fixture-output.txt"
    proof.write_text("hello\n", encoding="utf-8")
    proof_sha256 = hashlib.sha256(proof.read_bytes()).hexdigest()

    bundle = {
        "schema_version": 1,
        "workspace": {"revision": args.revision, "dirty": False},
        "evidence": [{
            "id": "fixture-output",
            "path": proof.name,
            "sha256": proof_sha256,
            "media_type": "text/plain",
        }],
        "claims": [{
            "id": "fixture-says-hello",
            "statement": "The fixture output contains hello.",
            "evidence": ["fixture-output"],
        }],
    }
    args.bundle.parent.mkdir(parents=True, exist_ok=True)
    args.bundle.write_text(
        json.dumps(bundle, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
