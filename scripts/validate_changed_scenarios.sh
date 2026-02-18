#!/usr/bin/env bash
set -euo pipefail

changed=$(git diff --cached --name-only --diff-filter=AM | grep -E '\.ya?ml$' || true)

for file in $changed; do
  # Skip bot-managed and repo-config files — not broker scenarios
  if [[ "$file" == "metadata.yaml" ]]; then
    continue
  fi
  if [[ "$file" == ".pre-commit-config.yaml" ]]; then
    continue
  fi
  if [[ "$file" == .github/* ]] || [[ "$file" == scripts/* ]]; then
    continue
  fi
  broker scenarios validate "$file"
done
