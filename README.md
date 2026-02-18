# broker-scenarios

Community scenario repository for the [broker](https://github.com/SatelliteQE/broker) provisioning framework.

Scenarios are reusable YAML workflows that drive broker actions such as checking out hosts, running commands over SSH, collecting inventory, and more. This repository provides a curated, validated collection of scenarios organized by provider.

---

## Using Scenarios (Not Yet Implemented)

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

Scenarios are stored locally under `~/.broker/scenarios/`, preserving the provider/category directory structure.

---

## Directory Layout

```
broker-scenarios/
├── README.md
├── metadata.yaml                       # Bot-managed — do not edit manually
├── ansibletower/
│   ├── provisioning/                   # Checkout and provisioning workflows
│   └── maintenance/                    # Tower maintenance and cleanup
├── container/
│   └── testing/                        # Container smoke tests and validation
├── common/                             # Multi-provider or utility scenarios
└── examples/                           # Tutorial-focused introductory scenarios
```

Each scenario lives at one of:
- `<provider>/<category>/<scenario-name>.yaml`
- `<provider>/<scenario-name>.yaml` (provider-root scenarios)

Imported scenarios mirror this path under `~/.broker/scenarios/`.

---

## Contributing

1. **Fork** this repository and create a feature branch.
2. **Add** your scenario YAML file in the appropriate provider/category directory.
3. **Validate** locally before committing:
   ```bash
   broker scenarios validate path/to/your/scenario.yaml
   ```
4. **Install pre-commit hooks** (first time only):
   ```bash
   pip install pre-commit
   pre-commit install
   ```
5. **Commit** — hooks will run YAML hygiene checks and validate changed scenarios automatically.
6. **Open a PR** — CI will re-validate all changed scenarios and ensure `metadata.yaml` has not been manually modified.

### Scenario Format

A scenario file requires at minimum a `steps` key. Full documentation for all available fields and actions is in the [broker docs](https://github.com/SatelliteQE/broker).

```yaml
steps:
  - name: Checkout a host
    action: checkout
    arguments:
      workflow: my-workflow

  - name: Run a command
    action: ssh
    with:
      hosts: scenario_inventory
    arguments:
      cmd: "uname -a"
```

### Notes for Contributors

- `metadata.yaml` is generated automatically on every push to `master`. **Do not edit it manually** — your changes will be overwritten and the PR check will block the merge.
- Scenario files may optionally include a top-level `description` key; this is surfaced in `metadata.yaml` and `broker scenarios import --list`.
- If `broker scenarios validate` reports an error you consider acceptable for your use case, note it clearly in the PR description.
