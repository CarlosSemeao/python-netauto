# Python for Network Automation

This repo contains small Python labs for network automation.

## Lab Evidence

- [Input inventory](data/input/devices.csv)
- [Valid devices](artifacts/expected/valid_devices.csv)
- [Invalid rows](artifacts/expected/invalid_devices.txt)
- [Site summary](artifacts/expected/site_summary.json)
- [Backup commands](artifacts/expected/backup_commands.txt)
- [Inventory run log](artifacts/expected/run_inventory.txt)
- [Summary run log](artifacts/expected/run_summary.txt)
- [Test results](artifacts/expected/test_results.txt)

## Sample Output

### Inventory run

```text
Processed 6 rows: 4 valid, 2 invalid
Wrote data/output/valid_devices.csv
Wrote data/output/invalid_devices.txt

### Summary run

Loaded 4 valid devices across 3 sites
Wrote data/output/site_summary.json
Wrote data/output/backup_commands.txt

### Test run

test_process_inventory (test_inventory.TestInventoryProcessing.test_process_inventory) ... ok
test_summary_and_backup_plan (test_inventory_summary.TestInventorySummary.test_summary_and_backup_plan) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK

