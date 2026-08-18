"""
Task Manager CLI -- AI Genius Episode 1 Workshop Starter App

A command-line task manager that demonstrates a real Python project
for attendees to extend using AI-native workflows with GitHub Copilot.

Usage:
    python app.py add "Buy groceries"
    python app.py add "Deploy to production" --priority high --due 2025-12-31 --tag work
    python app.py list
    python app.py list --status pending --priority high
    python app.py list --overdue
    python app.py complete 1
    python app.py edit 1 --priority low --due 2026-01-15
    python app.py delete 1
    python app.py stats
"""

import json
import sys
from datetime import date, datetime
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.text import Text

TASKS_FILE = Path(__file__).resolve().with_name("tasks.json")

PRIORITIES = ("low", "medium", "high")
PRIORITY_COLOURS = {"low": "cyan", "medium": "yellow", "high": "red"}

console = Console()


# ---------------------------------------------------------------------------
# Storage helpers
# ---------------------------------------------------------------------------


def load_tasks() -> list[dict]:
    """Load tasks from the JSON storage file.

    Returns:
        A list of task dictionaries. Returns an empty list if the file
        does not exist or cannot be parsed.
    """
    if not TASKS_FILE.exists():
        return []
    try:
        with TASKS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("tasks file must contain a JSON array")
        return data
    except (json.JSONDecodeError, OSError, ValueError):
        console.print("[red]Warning: Could not read tasks file. Starting fresh.[/red]")
        return []


def save_tasks(tasks: list[dict]) -> None:
    """Persist tasks to the JSON storage file.

    Args:
        tasks: The list of task dictionaries to save.
    """
    with TASKS_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def next_id(tasks: list[dict]) -> int:
    """Calculate the next available task ID.

    Args:
        tasks: The current list of tasks.

    Returns:
        An integer ID one greater than the current maximum, or 1 if there
        are no tasks.
    """
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


# ---------------------------------------------------------------------------
# Domain helpers
# ---------------------------------------------------------------------------


def is_overdue(task: dict) -> bool:
    """Return True if a pending task has a due date in the past.

    Args:
        task: A task dictionary.

    Returns:
        True when the task is not yet done and its due_date is before today.
    """
    if task.get("done"):
        return False
    due = task.get("due_date")
    if not due:
        return False
    try:
        return date.fromisoformat(due) < date.today()
    except ValueError:
        return False


def format_due(task: dict) -> Text:
    """Render the due date with colour based on urgency.

    Args:
        task: A task dictionary.

    Returns:
        A Rich Text object: red if overdue, yellow if due today, plain otherwise.
    """
    due = task.get("due_date", "")
    if not due:
        return Text("—", style="dim")
    try:
        due_date = date.fromisoformat(due)
    except ValueError:
        return Text(due, style="dim")

    today = date.today()
    if due_date < today:
        return Text(due, style="bold red")
    if due_date == today:
        return Text(due, style="yellow")
    return Text(due)


def find_task(tasks: list[dict], task_id: int) -> dict | None:
    """Find a task by its integer ID.

    Args:
        tasks: The list of tasks to search.
        task_id: The ID to look for.

    Returns:
        The matching task dict, or None if not found.
    """
    return next((t for t in tasks if t["id"] == task_id), None)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


@click.group()
def cli() -> None:
    """Task Manager — manage your to-do list from the terminal."""


@cli.command()
@click.argument("name")
@click.option(
    "--priority",
    "-p",
    type=click.Choice(PRIORITIES),
    default="medium",
    show_default=True,
    help="Task priority.",
)
@click.option("--description", "-d", default="", help="Optional longer description.")
@click.option(
    "--due",
    default=None,
    metavar="YYYY-MM-DD",
    help="Optional due date (ISO 8601).",
)
@click.option(
    "--tag",
    "-t",
    multiple=True,
    metavar="TAG",
    help="Tag to attach (may be repeated).",
)
def add(name: str, priority: str, description: str, due: str | None, tag: tuple[str, ...]) -> None:
    """Add a new task.

    NAME is the title of the task to add.
    """
    name = name.strip()
    if not name:
        console.print("[red]Error: Task name cannot be empty.[/red]")
        sys.exit(1)
    if len(name) > 200:
        console.print("[red]Error: Task name cannot exceed 200 characters.[/red]")
        sys.exit(1)

    if due:
        try:
            date.fromisoformat(due)
        except ValueError:
            console.print(f"[red]Error: '{due}' is not a valid date. Use YYYY-MM-DD format.[/red]")
            sys.exit(1)

    tasks = load_tasks()
    task: dict = {
        "id": next_id(tasks),
        "name": name,
        "description": description.strip(),
        "priority": priority,
        "tags": list(tag),
        "due_date": due,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    tasks.append(task)
    save_tasks(tasks)

    priority_colour = PRIORITY_COLOURS[priority]
    console.print(
        f"[green]Added task #[bold]{task['id']}[/bold][/green]: {name} "
        f"[[{priority_colour}]{priority}[/{priority_colour}]]"
    )


@cli.command(name="list")
@click.option(
    "--status",
    type=click.Choice(["pending", "done", "all"]),
    default="all",
    show_default=True,
    help="Filter by completion status.",
)
@click.option(
    "--priority",
    "-p",
    type=click.Choice(PRIORITIES),
    default=None,
    help="Filter by priority.",
)
@click.option("--tag", "-t", default=None, metavar="TAG", help="Filter by tag.")
@click.option("--overdue", is_flag=True, default=False, help="Show only overdue tasks.")
def list_tasks(status: str, priority: str | None, tag: str | None, overdue: bool) -> None:
    """List tasks with optional filters."""
    tasks = load_tasks()

    if not tasks:
        console.print("[yellow]No tasks yet. Use 'add' to create one.[/yellow]")
        return

    # Apply filters
    if status == "pending":
        tasks = [t for t in tasks if not t.get("done")]
    elif status == "done":
        tasks = [t for t in tasks if t.get("done")]

    if priority:
        tasks = [t for t in tasks if t.get("priority") == priority]

    if tag:
        tasks = [t for t in tasks if tag in t.get("tags", [])]

    if overdue:
        tasks = [t for t in tasks if is_overdue(t)]

    if not tasks:
        console.print("[yellow]No tasks match your filters.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold blue", box=None, pad_edge=False)
    table.add_column("ID", style="dim", width=4, justify="right")
    table.add_column("Task", min_width=30)
    table.add_column("Priority", width=8)
    table.add_column("Due", width=12)
    table.add_column("Tags", min_width=10)
    table.add_column("Status", width=9)

    for task in tasks:
        task_name = Text(str(task["name"]))
        if task.get("done"):
            task_name.stylize("strike dim")

        prio = task.get("priority", "medium")
        prio_colour = PRIORITY_COLOURS.get(prio, "white")
        priority_text = Text(prio, style=prio_colour)

        tags_text = Text(", ".join(task.get("tags", [])) or "—", style="dim")
        status_text = (
            Text("✓ Done", style="green") if task.get("done") else Text("Pending", style="yellow")
        )
        if is_overdue(task):
            status_text = Text("Overdue", style="bold red")

        table.add_row(
            str(task["id"]),
            task_name,
            priority_text,
            format_due(task),
            tags_text,
            status_text,
        )

    console.print(table)


@cli.command()
@click.argument("task_id", type=int)
def complete(task_id: int) -> None:
    """Mark a task as complete.

    TASK_ID is the numeric ID of the task to complete.
    """
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if task is None:
        console.print(f"[red]Error: No task found with ID {task_id}.[/red]")
        sys.exit(1)

    if task["done"]:
        console.print(f"[yellow]Task #{task_id} is already marked as done.[/yellow]")
        return

    task["done"] = True
    save_tasks(tasks)
    console.print(f"[green]Task #{task_id} marked as complete.[/green]")


@cli.command()
@click.argument("task_id", type=int)
@click.option("--name", "-n", default=None, help="New task name.")
@click.option(
    "--priority",
    "-p",
    type=click.Choice(PRIORITIES),
    default=None,
    help="New priority.",
)
@click.option("--description", "-d", default=None, help="New description.")
@click.option(
    "--due",
    default=None,
    metavar="YYYY-MM-DD",
    help="New due date (use '' to clear).",
)
@click.option(
    "--tag",
    "-t",
    multiple=True,
    metavar="TAG",
    help="Replace all tags (may be repeated; omit to leave unchanged).",
)
def edit(
    task_id: int,
    name: str | None,
    priority: str | None,
    description: str | None,
    due: str | None,
    tag: tuple[str, ...],
) -> None:
    """Edit an existing task.

    TASK_ID is the numeric ID of the task to edit.
    """
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if task is None:
        console.print(f"[red]Error: No task found with ID {task_id}.[/red]")
        sys.exit(1)

    changed = False

    if name is not None:
        name = name.strip()
        if not name:
            console.print("[red]Error: Task name cannot be empty.[/red]")
            sys.exit(1)
        if len(name) > 200:
            console.print("[red]Error: Task name cannot exceed 200 characters.[/red]")
            sys.exit(1)
        task["name"] = name
        changed = True

    if priority is not None:
        task["priority"] = priority
        changed = True

    if description is not None:
        task["description"] = description.strip()
        changed = True

    if due is not None:
        if due == "":
            task["due_date"] = None
        else:
            try:
                date.fromisoformat(due)
            except ValueError:
                console.print(
                    f"[red]Error: '{due}' is not a valid date. Use YYYY-MM-DD format.[/red]"
                )
                sys.exit(1)
            task["due_date"] = due
        changed = True

    if tag:
        task["tags"] = list(tag)
        changed = True

    if not changed:
        console.print("[yellow]No changes specified. Use --help to see options.[/yellow]")
        return

    save_tasks(tasks)
    console.print(f"[green]Task #{task_id} updated.[/green]")


@cli.command()
@click.argument("task_id", type=int)
def delete(task_id: int) -> None:
    """Delete a task.

    TASK_ID is the numeric ID of the task to delete.
    """
    tasks = load_tasks()
    updated = [t for t in tasks if t["id"] != task_id]

    if len(updated) == len(tasks):
        console.print(f"[red]Error: No task found with ID {task_id}.[/red]")
        sys.exit(1)

    save_tasks(updated)
    console.print(f"[green]Task #{task_id} deleted.[/green]")


@cli.command()
def stats() -> None:
    """Show a summary of your tasks."""
    tasks = load_tasks()

    total = len(tasks)
    done = sum(1 for t in tasks if t.get("done"))
    pending = total - done
    overdue = sum(1 for t in tasks if is_overdue(t))

    by_priority = {p: 0 for p in PRIORITIES}
    for t in tasks:
        if not t.get("done"):
            prio = t.get("priority", "medium")
            if prio in by_priority:
                by_priority[prio] += 1

    table = Table(show_header=False, box=None, pad_edge=False)
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    table.add_row("Total tasks", str(total))
    table.add_row("[green]Done[/green]", str(done))
    table.add_row("[yellow]Pending[/yellow]", str(pending))
    table.add_row("[bold red]Overdue[/bold red]", str(overdue))
    table.add_section()
    for prio in PRIORITIES:
        colour = PRIORITY_COLOURS[prio]
        table.add_row(f"[{colour}]Pending {prio}[/{colour}]", str(by_priority[prio]))

    console.print(table)


if __name__ == "__main__":
    cli()
