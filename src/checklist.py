"""Checklist rule engine.

Defines which systems and tasks are relevant for each role/department,
and generates a structured task list for onboarding or offboarding.

To add a new role: add an entry to ROLE_TASKS below.
To add a new system to an existing role: append to its task list.
All roles inherit the tasks in DEFAULT_TASKS automatically.
"""
from __future__ import annotations

from typing import Dict, List

Task = Dict[str, str]

# Tasks that apply to every employee regardless of role.
# Each task has explicit onboarding/offboarding wording so outputs stay action-safe.
DEFAULT_TASKS: List[Task] = [
    {
        "system": "Email / Google Workspace",
        "onboard_task": "Create email account and assign baseline groups",
        "offboard_task": "Suspend email account, delegate mailbox if needed, and archive data",
        "owner": "IT Admin",
    },
    {
        "system": "SSO / Okta",
        "onboard_task": "Provision SSO account and assign baseline applications",
        "offboard_task": "Disable SSO account and revoke application assignments",
        "owner": "IT Admin",
    },
    {
        "system": "Azure AD",
        "onboard_task": "Add user to Azure AD and assign required groups",
        "offboard_task": "Block sign-in, remove group access, and review shared resources",
        "owner": "IT Admin",
    },
    {
        "system": "Laptop / Device",
        "onboard_task": "Provision device, enroll in MDM, and verify baseline security controls",
        "offboard_task": "Collect device, wipe if approved, and update asset inventory",
        "owner": "IT Admin",
    },
    {
        "system": "Password Manager",
        "onboard_task": "Create account and assign the correct vaults",
        "offboard_task": "Suspend account, remove vault access, and rotate sensitive shared credentials if needed",
        "owner": "IT Admin",
    },
    {
        "system": "Slack / Teams",
        "onboard_task": "Add user to workspace and join relevant channels",
        "offboard_task": "Deactivate account and transfer ownership of critical channels or bots if needed",
        "owner": "IT Admin",
    },
]

# Role-specific tasks layered on top of the defaults.
# Keys should match the --role argument value (case-insensitive comparison is handled below).
ROLE_TASKS: Dict[str, List[Task]] = {
    "Support Engineer": [
        {
            "system": "Zendesk",
            "onboard_task": "Create agent account and assign groups, views, and macros",
            "offboard_task": "Suspend agent account and remove group, view, and macro access",
            "owner": "Support Lead",
        },
        {
            "system": "Intercom",
            "onboard_task": "Add user to inbox and assign conversation routing rules",
            "offboard_task": "Remove inbox access and review conversation ownership handoff",
            "owner": "Support Lead",
        },
        {
            "system": "Loom",
            "onboard_task": "Add user to the team workspace for async walkthroughs",
            "offboard_task": "Remove user from the workspace and transfer important recordings if needed",
            "owner": "IT Admin",
        },
    ],
    "IT Administrator": [
        {
            "system": "Unifi / Network Console",
            "onboard_task": "Grant admin access to network management tools with the correct role",
            "offboard_task": "Revoke admin access to network management tools and review audit logs",
            "owner": "IT Lead",
        },
        {
            "system": "1Password Teams",
            "onboard_task": "Assign user to the IT vault with the correct permissions",
            "offboard_task": "Remove vault access and rotate sensitive credentials if warranted",
            "owner": "IT Lead",
        },
        {
            "system": "GitHub Org",
            "onboard_task": "Add user to the GitHub org and relevant teams",
            "offboard_task": "Remove user from the GitHub org, teams, and personal access paths",
            "owner": "IT Lead",
        },
    ],
    "Sales": [
        {
            "system": "CRM / Salesforce",
            "onboard_task": "Create CRM account and assign the correct territory or pipeline",
            "offboard_task": "Deactivate CRM account and reassign owned records or opportunities",
            "owner": "Sales Ops",
        },
        {
            "system": "LinkedIn Sales Navigator",
            "onboard_task": "Assign an active seat in the team plan",
            "offboard_task": "Remove the seat and transfer saved lists if needed",
            "owner": "Sales Ops",
        },
        {
            "system": "Outreach / Apollo",
            "onboard_task": "Provision sequencing tool account with the correct templates and permissions",
            "offboard_task": "Disable sequencing tool account and transfer active sequences or ownership",
            "owner": "Sales Ops",
        },
    ],
    "Engineering": [
        {
            "system": "GitHub",
            "onboard_task": "Add user to the GitHub org and engineering teams",
            "offboard_task": "Remove user from the GitHub org, teams, and deployment access",
            "owner": "Engineering Lead",
        },
        {
            "system": "AWS / GCP / Azure",
            "onboard_task": "Create cloud IAM access with least-privilege permissions",
            "offboard_task": "Disable cloud IAM access, revoke keys, and review active sessions",
            "owner": "DevOps",
        },
        {
            "system": "Jira",
            "onboard_task": "Add user to the relevant project boards and teams",
            "offboard_task": "Deactivate Jira access and reassign active issues or filters",
            "owner": "Engineering Lead",
        },
        {
            "system": "Datadog / Sentry",
            "onboard_task": "Grant monitoring access to the correct dashboards and projects",
            "offboard_task": "Remove monitoring access and review alert ownership",
            "owner": "DevOps",
        },
    ],
}


def _normalize_task(task: Task, action: str) -> Task:
    """Return a task with the action-specific wording collapsed into `task`."""
    task_key = "onboard_task" if action == "onboard" else "offboard_task"
    return {
        "system": task["system"],
        "task": task[task_key],
        "owner": task["owner"],
    }


def get_tasks_for_role(role: str, action: str) -> List[Task]:
    """Return the full task list for a given role and lifecycle action.

    Combines DEFAULT_TASKS with any role-specific tasks defined in ROLE_TASKS.
    Unknown roles still get the default tasks plus a manual review step.
    """
    if action not in {"onboard", "offboard"}:
        raise ValueError("action must be 'onboard' or 'offboard'")

    matched_key = next((key for key in ROLE_TASKS if key.lower() == role.lower()), None)

    tasks = [_normalize_task(task, action) for task in DEFAULT_TASKS]
    if matched_key:
        tasks.extend(_normalize_task(task, action) for task in ROLE_TASKS[matched_key])
    else:
        review_text = (
            f"Review role-specific systems and provision required access for: {role}"
            if action == "onboard"
            else f"Review role-specific systems and revoke any remaining access for: {role}"
        )
        tasks.append({
            "system": "Role-specific systems",
            "task": review_text,
            "owner": "IT Admin",
        })

    return tasks
