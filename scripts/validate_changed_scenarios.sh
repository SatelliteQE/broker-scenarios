#!/usr/bin/env bash
set -euo pipefail

changed=$(git diff --cached --name-only --diff-filter=AM | grep -E '\.ya?ml$' || true)

for file in $changed; do
  # validate only scenario files, skip top-level generated metadata
  if [[ "$file" == "metadata.yaml" ]]; then
    continue
  fi
  broker scenarios validate "$file"
done
