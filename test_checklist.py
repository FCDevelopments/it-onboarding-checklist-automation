from checklist import get_tasks_for_role


def task_text(tasks, system):
    return next(task["task"] for task in tasks if task["system"] == system)


def test_support_engineer_onboarding_and_offboarding_use_different_actions():
    onboard_tasks = get_tasks_for_role("Support Engineer", "onboard")
    offboard_tasks = get_tasks_for_role("Support Engineer", "offboard")

    assert "Create agent account" in task_text(onboard_tasks, "Zendesk")
    assert "Suspend agent account" in task_text(offboard_tasks, "Zendesk")
    assert "Add user to the team workspace" in task_text(onboard_tasks, "Loom")
    assert "Remove user from the workspace" in task_text(offboard_tasks, "Loom")


def test_unknown_role_gets_action_safe_manual_review_task():
    onboard_tasks = get_tasks_for_role("Finance Analyst", "onboard")
    offboard_tasks = get_tasks_for_role("Finance Analyst", "offboard")

    assert "provision required access" in task_text(onboard_tasks, "Role-specific systems")
    assert "revoke any remaining access" in task_text(offboard_tasks, "Role-specific systems")
