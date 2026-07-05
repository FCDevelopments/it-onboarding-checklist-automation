"""IT Onboarding / Offboarding Checklist Automation — entry point.

Generates a role-specific IT checklist (markdown + CSV) for onboarding
or offboarding a team member. Tasks are built from a configurable rule set
that covers both universal defaults and role-specific systems.

Usage:
    python src/main.py --name "Jane Smith" --role "Support Engineer" --action onboard
    python src/main.py --name "Jane Smith" --role "Support Engineer" --action offboard --output-dir output
"""
import argparse
from checklist import get_tasks_for_role
from report import write_outputs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate an IT onboarding or offboarding checklist for a team member"
    )
    parser.add_argument("--name", required=True, help="Employee full name")
    parser.add_argument("--role", required=True, help="Employee role/title (e.g. 'Support Engineer')")
    parser.add_argument(
        "--action",
        choices=["onboard", "offboard"],
        required=True,
        help="Whether to generate an onboarding or offboarding checklist"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory for generated files (default: output)"
    )
    args = parser.parse_args()

    print(f"Generating {args.action} checklist for {args.name} ({args.role})...")

    # Get the full task list for this role and lifecycle action
    tasks = get_tasks_for_role(args.role, args.action)

    # Write checklist.md and tasks.csv to the output directory
    write_outputs(args.name, args.role, args.action, tasks, args.output_dir)

    print(f"Done. Outputs written to: {args.output_dir}/")
    print(f"  - {args.output_dir}/checklist.md")
    print(f"  - {args.output_dir}/tasks.csv")


if __name__ == "__main__":
    main()
