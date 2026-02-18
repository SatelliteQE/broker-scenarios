"""Generate metadata.yaml from all scenario files in the repository.

This script is intended to be run by automation only (see .github/workflows/update-metadata.yml).
It walks the repository tree, collects metadata from each scenario YAML file, and writes a
deterministically sorted metadata.yaml to the repository root.

Do not run this manually in a contributor PR — the pre-commit hook will block any manual
modification of metadata.yaml.
"""

import datetime
import pathlib
import sys

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

EXCLUDED_DIRS = {".github", "scripts", ".git"}
EXCLUDED_FILES = {"metadata.yaml"}


def find_scenario_files(root):
    results = []
    for path in sorted(root.rglob("*.yaml")) + sorted(root.rglob("*.yml")):
        rel = path.relative_to(root)
        parts = rel.parts
        if any(part in EXCLUDED_DIRS for part in parts):
            continue
        if path.name in EXCLUDED_FILES:
            continue
        results.append(path)
    return sorted(results, key=lambda p: str(p.relative_to(root)))


def extract_scenario_entry(path, root):
    rel = path.relative_to(root)
    parts = rel.parts

    provider = parts[0] if len(parts) >= 1 else None
    category = parts[1] if len(parts) >= 3 else None
    name = path.stem

    try:
        with open(path) as f:
            data = yaml.safe_load(f) or {}
    except Exception as exc:
        print(f"Warning: could not parse {rel}: {exc}", file=sys.stderr)
        data = {}

    entry = {
        "path": str(rel),
        "name": name,
    }
    if provider:
        entry["provider"] = provider
    if category:
        entry["category"] = category
    if "description" in data:
        entry["description"] = data["description"]

    return entry


def generate_metadata(root):
    files = find_scenario_files(root)
    scenarios = [extract_scenario_entry(f, root) for f in files]

    metadata = {
        "schema_version": 1,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "scenarios": scenarios,
    }
    return metadata


def write_metadata(root, metadata):
    out_path = root / "metadata.yaml"
    header = (
        "# This file is generated and maintained exclusively by automation.\n"
        "# Do NOT edit it manually — your changes will be overwritten on the next push to master.\n"
        "# See .github/workflows/update-metadata.yml for the generation trigger.\n\n"
    )
    content = yaml.dump(
        metadata,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=True,
    )
    with open(out_path, "w") as f:
        f.write(header)
        f.write(content)
    print(f"Wrote {out_path} ({len(metadata['scenarios'])} scenarios)")


if __name__ == "__main__":
    metadata = generate_metadata(REPO_ROOT)
    write_metadata(REPO_ROOT, metadata)
