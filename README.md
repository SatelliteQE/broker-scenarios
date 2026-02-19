# broker-scenarios

Community scenario repository for [Broker](https://github.com/SatelliteQE/broker).

Scenarios are reusable YAML workflows that drive broker actions such as checking out hosts, running commands over SSH, collecting inventory, and more. This repository provides a curated, validated collection of scenarios organized by category.

The scenarios in this repo can either be copied locally or imported via `broker scenarios import` in the near future.

---

## Importing Scenarios (Not Yet Implemented)

Import scenarios directly into your local broker installation:

```bash
# Import all scenarios from a provider directory
broker scenarios import SatelliteQE/broker-scenarios/ansibletower

# Import the full community repo
broker scenarios import SatelliteQE/broker-scenarios

# List available remote scenarios without downloading
broker scenarios import SatelliteQE/broker-scenarios --list

# Filter by category
broker scenarios import SatelliteQE/broker-scenarios --category container

# Update previously imported scenarios
broker scenarios import SatelliteQE/broker-scenarios --update

# Show previously imported scenario history
broker scenarios import --list-imported
```

Scenarios are stored locally in your broker directory (usually `~/.broker/`), preserving the provider/category directory structure.

---

## Repo Directory Layout

```
broker-scenarios/
├── README.md
├── metadata.yaml                       # Bot-managed — do not edit manually
├── ansibletower/
│   ├── post_deploy/                    # Scenarios that perform post-deploy actions
│   └── maintenance/                    # Tower maintenance and cleanup
├── container/
│   └── testing/                        # Container smoke tests and validation
├── common/                             # Multi-provider or utility scenarios
└── examples/                           # Tutorial-focused introductory scenarios
```

Each provider scenario lives at one of:
- `<provider>/<category>/<scenario-name>.yaml`
- `<provider>/<scenario-name>.yaml` (provider-root scenarios)

Imported scenarios mirror this path under `~/{BROKER_DIRECTORY}/scenarios/`.

---

## Contributing

1. **Fork** this repository and create a feature branch.
2. **Add** your scenario YAML file in the appropriate provider/category directory.
4. **Install pre-commit hooks** (first time only):
   ```bash
   pip install pre-commit
   pre-commit install
   ```
5. **Commit** — hooks will run YAML hygiene checks and validate changed scenarios automatically.
6. **Open a PR** — CI will re-validate all changed scenarios and ensure `metadata.yaml` has not been manually modified.

### Scenario Format

A scenario file requires at minimum a `steps` key. Full documentation for all available fields and actions is in the [broker wiki](https://github.com/SatelliteQE/broker/wiki/Scenarios-Tutorial).

```yaml
steps:
  - name: Checkout a host with AnsibleTower
    action: checkout
    arguments:
      workflow: my-workflow

  - name: Run a command
    action: ssh
    with:
      hosts: scenario_inventory
    arguments:
      command: "uname -a"
```

### Notes for Contributors

- `metadata.yaml` is generated automatically on every push to `master`. **Do not edit it manually** — your changes will be overwritten and the PR check will block the merge.
- Scenario files may optionally include a top-level `description` key; this is surfaced in `metadata.yaml` and `broker scenarios import --list`.
- If `broker scenarios validate` reports an error you consider acceptable for your use case, note it clearly in the PR description.
