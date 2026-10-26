#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = json.loads((ROOT / ".embeddedville-workspace.json").read_text())
ACTIVITIES = IDENTITY["activities"]
ACTIVITY_DIRECTORIES = IDENTITY["activityDirectories"]


def fail(message: str, code: int = 2) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def activity(value: str | None) -> str:
    if not value or value not in ACTIVITIES:
        fail("choose one activity: " + ", ".join(ACTIVITIES))
    return value


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(command))
    return subprocess.run(command, cwd=ROOT, text=True, check=check)


def git_value(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    return result.stdout.strip() if result.returncode == 0 else "uncommitted-workspace"


def digest_tree(path: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(file.relative_to(ROOT).as_posix().encode())
        digest.update(b"\0")
        digest.update(file.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def doctor() -> None:
    problems = []
    if Path.cwd().resolve() != ROOT:
        problems.append(f"run from {ROOT}")
    gcc = shutil.which("gcc-13") or shutil.which("gcc")
    make = shutil.which("make")
    if not gcc: problems.append("GCC 13 is missing")
    if not make: problems.append("GNU Make is missing")
    if gcc:
        version = subprocess.run([gcc, "-dumpfullversion"], text=True, capture_output=True).stdout.strip()
        if not version.startswith("13."): problems.append(f"expected GCC 13, found {version}")
    if IDENTITY["courseId"] != "embedded-dsa-foundations": problems.append("wrong course identity")
    if problems:
        for problem in problems: print(f"FAIL: {problem}")
        raise SystemExit(1)
    print(f"PASS: {IDENTITY['courseId']} {IDENTITY['starterVersion']}")
    print("PASS: GCC 13, GNU Make, C11 workspace identity")
    if IDENTITY["refStatus"].startswith("pending"):
        print("NOTICE: review candidate uses an intended immutable ref; release tag is not yet authorized")


def build(item: str | None) -> None:
    run(["make", ACTIVITY_DIRECTORIES[item]] if item else ["make", "all"])


def execute(item: str, sanitizer: str | None = None) -> None:
    directory = ACTIVITY_DIRECTORIES[item]
    env = os.environ.copy()
    if sanitizer:
        run(["make", "clean"])
        run(["make", sanitizer])
    elif not (ROOT / "build" / directory).exists():
        build(item)
    result = subprocess.run([str(ROOT / "build" / directory)], cwd=ROOT, env=env, text=True)
    if result.returncode:
        print("NOT COMPLETE: public checks did not pass. Preserve your work and inspect the first failed invariant.")
        raise SystemExit(result.returncode)


def submit(item: str) -> None:
    execute(item)
    lab_dir = ROOT / "labs" / ACTIVITY_DIRECTORIES[item]
    manifest = {
        "schemaVersion": 1,
        "courseId": IDENTITY["courseId"],
        "activityId": item,
        "starterVersion": IDENTITY["starterVersion"],
        "repository": IDENTITY["repository"],
        "intendedImmutableRef": IDENTITY["intendedImmutableRef"],
        "commitSha": git_value("rev-parse", "HEAD"),
        "sourceDigest": digest_tree(lab_dir),
        "workingTreeDirty": bool(git_value("status", "--porcelain")),
        "localChecks": "pass",
        "protectedEvaluation": "pending-platform-upload"
    }
    out = ROOT / "evidence" / f"{item}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Evidence manifest written to {out.relative_to(ROOT)}")


def reset(item: str, confirmed: bool) -> None:
    target = ROOT / "labs" / ACTIVITY_DIRECTORIES[item]
    print(f"Reset target: {target}")
    print("This discards uncommitted changes in that activity. Commit or export work first.")
    if not confirmed:
        fail("rerun with --confirm RESET after reviewing the target", 1)
    run(["git", "restore", "--source=HEAD", "--", str(target.relative_to(ROOT))])


def main() -> None:
    if len(sys.argv) < 2:
        fail("usage: ./lab doctor|build|run|test|submit|reset [activity]")
    command = sys.argv[1]
    item = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
    if command == "doctor": doctor()
    elif command == "build": build(item)
    elif command in {"run", "test"}: execute(activity(item))
    elif command == "submit": submit(activity(item))
    elif command == "reset": reset(activity(item), "--confirm" in sys.argv and "RESET" in sys.argv)
    else: fail(f"unknown command {command}")


if __name__ == "__main__":
    main()

