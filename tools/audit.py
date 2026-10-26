#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
identity = json.loads((root / ".embeddedville-workspace.json").read_text())
errors = []
for item in identity["activities"]:
    directory = identity["activityDirectories"][item]
    if not (root / "labs" / directory / "main.c").is_file(): errors.append(f"missing {item} ({directory})")
for forbidden in ("solution", "answer-key", "protected-test", "evaluator-secret"):
    for path in root.rglob("*"):
        if path.is_file() and forbidden in path.name.lower(): errors.append(f"forbidden public asset {path}")
if errors:
    raise SystemExit("\n".join(errors))
print("Public starter audit: PASS")

