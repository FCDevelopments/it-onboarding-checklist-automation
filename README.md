# IT Onboarding / Offboarding Checklist Automation

> Generate consistent, role-specific IT onboarding and offboarding checklists from a simple config — no more missed steps, no more one-off emails.

## What it does
Takes a new hire or departing employee profile (name, role, department, start/end date) and generates a complete IT checklist covering the systems, access, and tasks relevant to that role. Outputs a markdown checklist and a CSV task tracker.

## Who it's for
- IT administrators managing user lifecycle workflows
- Anyone running onboarding/offboarding manually from memory or shared docs
- Teams wanting to standardize access provisioning without a full ITSM platform

## Problem it solves
Onboarding and offboarding steps are often tribal knowledge — someone forgets to revoke a SaaS account, or a new hire waits days for access. This tool generates a complete, role-specific checklist every time so nothing gets missed.

## Usage
```bash
python src/main.py --name "Jane Smith" --role "Support Engineer" --action onboard --output-dir output
python src/main.py --name "Jane Smith" --role "Support Engineer" --action offboard --output-dir output
python run_tests.py
```

## Outputs
| File | What it contains |
|---|---|
| `output/checklist.md` | Full markdown checklist with checkboxes |
| `output/tasks.csv` | Task tracker with owner, system, and status columns |

## Requirements
- Python 3.9+
- No external dependencies — uses standard library only

## Status
Current state: **QA-passed MVP**

## QA notes
- onboarding and offboarding now generate action-specific task wording
- includes `test_checklist.py` for pytest-based checks where available
- includes `run_tests.py` for constrained environments without pip/pytest
- sample outputs are included in `output/`

## Roadmap
- configurable role/system mappings via YAML config
- Slack/email notification stub
- Jira/ServiceNow ticket creation template
