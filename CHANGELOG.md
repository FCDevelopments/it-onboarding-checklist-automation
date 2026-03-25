# Changelog

All notable changes to this project will be documented here.

---

## [1.1.0] — 2026-03-25

### Added
- `live_test_onboard/` — live QA run artifacts for IT Administrator onboarding scenario (Alex Rivera)
- `live_test_offboard/` — live QA run artifacts for IT Administrator offboarding scenario (Alex Rivera)
- Both folders include generated `checklist.md` and `tasks.csv` outputs demonstrating real CLI runs

### Changed
- Verified CLI-to-output pipeline is fully functional end-to-end with no external dependencies
- Confirmed onboard and offboard wording is action-specific (not shared generic copy)

### Notes
- All outputs generated with `python src/main.py --name "Alex Rivera" --role "IT Administrator" --action onboard/offboard --output-dir live_test_onboard/offboard`
- `run_tests.py` passes cleanly in standard Python 3.9+ environments
