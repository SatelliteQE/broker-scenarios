# Libvirt Provider Test Scenarios

This directory contains end-to-end test scenarios for the Broker Libvirt provider.

## Available Test Scenarios

### 1. `smoke_libvirt_test_no_ssh.yaml` ✅ **Recommended for CI/automated testing**

**Purpose:** Validates Libvirt provider functionality WITHOUT requiring SSH access to the guest VM.

**What it tests:**
- ✓ Provider info queries (images, networks, pools)
- ✓ VM checkout from base image
- ✓ IP address assignment via DHCP
- ✓ All hypervisor-level actions:
  - pause / resume
  - reset
  - hard-stop / power-on
  - power-off
- ✓ Inventory queries (domains)
- ✓ VM checkin and cleanup verification

**Prerequisites:**
- Running libvirtd daemon (`systemctl status libvirtd`)
- User in `libvirt` group (`groups | grep libvirt`)
- At least one base image in the storage pool

**Usage:**
```bash
# Run with defaults (uses fed44.qcow2)
broker scenarios execute testing/smoke_libvirt_test_no_ssh

# Use a different base image
broker scenarios execute testing/smoke_libvirt_test_no_ssh --vars BASE_IMAGE=rhel9.qcow2

# Custom memory/CPU allocation
broker scenarios execute testing/smoke_libvirt_test_no_ssh \
  --vars MEMORY_MB=4096 CPUS=4
```

**Expected runtime:** ~20-30 seconds
**Exit code:** 0 on success, non-zero on failure

---

### 2. `smoke_libvirt_test.yaml` — Full E2E with SSH

**Purpose:** Complete end-to-end validation including SSH connectivity to the guest VM.

**What it tests (in addition to smoke_libvirt_test_no_ssh.yaml):**
- ✓ SSH connectivity
- ✓ Command execution via SSH (hostname, uptime, file I/O)
- ✓ VM responsiveness after hypervisor actions (reboot, resume)

**Prerequisites:**
⚠️ **The base image MUST be customized with SSH credentials first!**

1. Run the setup scenario to customize your base image:
   ```bash
   # For password-based auth (matches broker_settings.yaml example)
   broker scenarios execute scenario_libvirt_setup_local \
     --vars AUTH_METHOD=basic GUEST_PASSWORD=dog8code

   # OR for key-based auth
   broker scenarios execute scenario_libvirt_setup_local \
     --vars AUTH_METHOD=key PUBKEY_PATH=~/.ssh/id_ed25519.pub
   ```

2. Ensure `broker_settings.yaml` has matching credentials:
   ```yaml
   ssh:
     auth_method: basic  # or "key"
     host_password: dog8code  # if auth_method=basic
     # OR
     host_ssh_key_filename: /path/to/key  # if auth_method=key
   ```

**Usage:**
```bash
broker scenarios execute testing/smoke_libvirt_test
```

**Expected runtime:** ~90-120 seconds (includes VM reboot)
**Common failure:** "Password-based authentication failed" means you need to run the setup scenario first (see prerequisites above).

---

## Interpreting Results

### Success
```
====================================
VM successfully released and removed from Libvirt inventory.
Smoke test PASSED - all assertions validated.
====================================
```
Exit code: **0**

### Failure
The scenario will:
1. Print detailed error messages
2. Attempt cleanup (checkin the VM)
3. Exit with a non-zero code:
   - **10**: VM checkout failed
   - **11**: SSH connectivity failed (smoke_libvirt_test.yaml only)
   - **5**: Test passed but cleanup failed (manual cleanup needed)
   - **16**: Assertion failure or step error

### Manual Cleanup

If a test fails and leaves a VM behind:
```bash
# List running domains
virsh -c qemu:///system list --all

# Clean up manually
virsh -c qemu:///system destroy broker_jake_XXXXXXXX
virsh -c qemu:///system undefine broker_jake_XXXXXXXX --nvram
virsh -c qemu:///system vol-delete broker_jake_XXXXXXXX.qcow2 --pool default
```

---

## CI Integration Example

```bash
#!/bin/bash
set -e

echo "Running Libvirt provider smoke tests..."

# Quick validation (no SSH required)
broker scenarios execute testing/smoke_libvirt_test_no_ssh || {
  echo "ERROR: Libvirt smoke test failed!"
  exit 1
}

echo "Libvirt provider tests PASSED"
```

---

## Customization

Both scenarios support variable overrides via `--vars`:

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_IMAGE` | `fed44.qcow2` | Base qcow2 image to use |
| `MEMORY_MB` | `2048` | RAM allocation in MB |
| `CPUS` | `2` | vCPU count |
| `EXPECTED_NETWORK` | `default` | Expected libvirt network |
| `EXPECTED_POOL` | `default` | Expected storage pool |
| `TEST_STRING` | `broker_libvirt_e2e_test_marker` | Marker for file I/O tests (full test only) |

---

## Troubleshooting

### "No base images found in the storage pool"
```bash
# Download a base image (example: Fedora 44)
sudo curl -L -o /var/lib/libvirt/images/fed44.qcow2 \
  https://download.fedoraproject.org/pub/fedora/linux/releases/44/Server/x86_64/images/Fedora-Server-Guest-Generic-44-1.7.x86_64.qcow2

# Refresh the pool
sudo virsh pool-refresh default
```

### "Expected network 'default' not found"
```bash
# Start the default network
sudo virsh net-start default
sudo virsh net-autostart default
```

### "Permission denied" / "authentication cancelled"
Your user needs to be in the `libvirt` group:
```bash
sudo usermod -aG libvirt $USER
# Then log out and back in, or run:
newgrp libvirt
```

### Validate scenario syntax
```bash
broker scenarios validate scenarios/testing/smoke_libvirt_test_no_ssh.yaml
```

---

## Architecture Notes

- **Assertions:** Each test uses the `assert` action extensively to validate expected behavior at each step
- **Error handling:** Failed steps trigger `on_error` handlers that attempt cleanup before exiting
- **Retries:** SSH connectivity and post-action checks use retry logic to handle timing issues
- **Isolation:** Each scenario uses `scenario_inventory` to track only VMs created during that run
- **Idempotency:** Tests can be run repeatedly; cleanup is verified at the end

---

## Contributing

When adding new test scenarios:
1. Use `_spec_ver: 3` at the top
2. Add comprehensive `assert` steps after each action
3. Include `on_error` handlers for cleanup
4. Document prerequisites clearly
5. Validate with `broker scenarios validate` before committing
6. Test both success and failure paths
