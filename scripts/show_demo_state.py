#!/usr/bin/env python3
"""Print the current demo branch state without changing it."""

from __future__ import annotations

import subprocess


SCENARIOS = {
    "main": ("Safe baseline", "none", "pytest", True),
    "demo/single-fix": ("Targeted /ai-fix", "SF-1", "/ai-fix (inline reply)", False),
    "demo/all-categories": ("All review categories", "AC-1..AC-7", "triage findings", False),
    "demo/fix-all": ("Bulk fixing", "BF-1..BF-5", "/ai-fix all (PR comment)", False),
    "demo/lifecycle": ("Incremental lifecycle", "LC-1..LC-3", "cherry-pick prepared commits", False),
    "demo/lifecycle-step-2": ("Lifecycle preparation step 2", "LC-1, LC-3", "do not push as a PR", False),
    "demo/lifecycle-step-3": ("Lifecycle preparation step 3", "LC-1, relocated LC-3", "do not push as a PR", False),
    "demo/manual-actions": ("Manual triage", "MA-1..MA-3", "ignore / resolve / needs review", False),
}


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def main() -> None:
    branch = git("branch", "--show-current")
    short_sha = git("rev-parse", "--short", "HEAD")
    scenario, findings, command, safe = SCENARIOS.get(
        branch, ("Unknown branch", "unknown", "inspect documentation", False)
    )
    print(f"branch: {branch}")
    print(f"commit: {short_sha}")
    print(f"scenario: {scenario}")
    print(f"expected findings: {findings}")
    print(f"intended demo command: {command}")
    print(f"safe baseline: {'yes' if safe else 'no — intentionally flawed'}")


if __name__ == "__main__":
    main()

