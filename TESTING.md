# Testing HA-SIM Integration

## Safety Testing Before Deployment

### 1. Test in Development Environment

**Never test directly on your production Home Assistant instance!**

#### Option A: Docker Test Environment
```bash
# Create a test HA instance
docker run -d \
  --name ha-test \
  -v $(pwd)/custom_components:/config/custom_components \
  -v $(pwd)/test-config:/config \
  -p 8124:8123 \
  homeassistant/home-assistant:latest
```

#### Option B: Virtual Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Home Assistant
pip install homeassistant

# Run with custom component
hass -c test-config
```

### 2. Configuration Validation

Before starting HA with the integration:

```bash
# Check configuration
hass --script check_config -c test-config
```

### 3. Integration Testing Checklist

- [ ] Integration loads without errors
- [ ] Config flow completes successfully
- [ ] All entities are created
- [ ] Entities update on schedule
- [ ] Integration can be reloaded via UI
- [ ] Integration can be removed cleanly
- [ ] No errors in Home Assistant logs
- [ ] Memory usage remains stable

### 4. Reload Testing

Test the integration reload functionality:

1. Go to Developer Tools → YAML
2. Click "Reload" next to your integration
3. Check logs for errors
4. Verify entities still work

### 5. Error Scenarios to Test

1. **No failed integrations**: Verify sensors show correct "none" state
2. **Failed integration**: Manually break an integration to test detection
3. **Config entry removal**: Remove and re-add the integration
4. **Home Assistant restart**: Ensure integration survives restart

### 6. Log Monitoring

Watch for these error patterns:
```bash
# Monitor logs during testing
docker logs -f ha-test 2>&1 | grep -E "(ERROR|WARNING|ha_sim)"
```

### 7. Performance Testing

```yaml
# Add to configuration.yaml for profiling
logger:
  default: info
  logs:
    custom_components.ha_sim: debug
    homeassistant.helpers.update_coordinator: debug
```

## Safe Testing Script

Create `test_integration.py`:

```python
#!/usr/bin/env python3
"""Test HA-SIM integration safely."""
import asyncio
import logging
from pathlib import Path
import sys

# Add custom components to path
sys.path.insert(0, str(Path(__file__).parent / "custom_components"))

logging.basicConfig(level=logging.DEBUG)

async def test_coordinator():
    """Test the coordinator directly."""
    from ha_sim.coordinator import IntegrationMonitorCoordinator
    
    # Mock objects
    class MockHass:
        config_entries = None
    
    class MockEntry:
        data = {"scan_interval": 60}
        entry_id = "test"
    
    # Test coordinator
    hass = MockHass()
    entry = MockEntry()
    
    try:
        coordinator = IntegrationMonitorCoordinator(hass, entry)
        print("✓ Coordinator created successfully")
    except Exception as e:
        print(f"✗ Coordinator failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_coordinator())
    sys.exit(0 if success else 1)
```

## Warning Signs

Stop testing immediately if you see:

- Home Assistant becomes unresponsive
- Memory usage rapidly increasing
- Continuous error loops in logs
- Other integrations failing after adding HA-SIM

## Recovery

If something goes wrong:

1. Stop Home Assistant
2. Remove the integration folder: `rm -rf custom_components/ha_sim`
3. Remove from `configuration.yaml` if added there
4. Restart Home Assistant
5. Check `.storage/core.config_entries` and remove ha_sim entry if needed