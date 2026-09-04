#!/usr/bin/env bash
set -euo pipefail

# List of files to explicitly exclude
EXCLUDE_FILES=(
  "metadata.yaml"
  ".pre-commit-config.yaml"
)

# Find all YAML files in the repository
yaml_files=$(find . -type f \( -name "*.yaml" -o -name "*.yml" \) | sed 's|^\./||')

for file in $yaml_files; do
  # Skip files in .github/ and scripts/ directories
  if [[ "$file" == .github/* ]] || [[ "$file" == scripts/* ]]; then
    continue
  fi

  # Skip explicitly excluded files
  skip=false
  for exclude in "${EXCLUDE_FILES[@]}"; do
    if [[ "$file" == "$exclude" ]]; then
      skip=true
      break
    fi
  done

  if [[ "$skip" == true ]]; then
    continue
  fi

  echo "Migrating: $file"
  broker scenarios migrate "$file"
done

echo "Migration complete!"
