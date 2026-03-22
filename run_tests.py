"""Lightweight test runner for environments without pytest/pip.

Runs a few core assertions against the checklist generation logic using only
Python's standard library so QA can still validate behavior on constrained hosts.
"""
from checklist import get_tasks_for_role


def task_text(tasks, system):
    return next(task["task"] for task in tasks if task["system"] == system)


def main() -> None:
    onboard_tasks = get_tasks_for_role("Support Engineer", "onboard")
    offboard_tasks = get_tasks_for_role("Support Engineer", "offboard")

    assert "Create agent account" in task_text(onboard_tasks, "Zendesk")
    assert "Suspend agent account" in task_text(offboard_tasks, "Zendesk")
    assert "Add user to the team workspace" in task_text(onboard_tasks, "Loom")
    assert "Remove user from the workspace" in task_text(offboard_tasks, "Loom")

    unknown_onboard = get_tasks_for_role("Finance Analyst", "onboard")
    unknown_offboard = get_tasks_for_role("Finance Analyst", "offboard")
    assert "provision required access" in task_text(unknown_onboard, "Role-specific systems")
    assert "revoke any remaining access" in task_text(unknown_offboard, "Role-specific systems")

    print("run_tests.py: PASS")


if __name__ == "__main__":
    main()
