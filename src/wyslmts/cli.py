import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from wyslmts.models import Task, Priority
from wyslmts.storage import Storage

app = typer.Typer(
    name="wyslmts",
    help="Personal AI Productivity CLI",
    add_completion=False,
)
task_app = typer.Typer(help="Manage your tasks")
app.add_typer(task_app, name="task")

console = Console()
storage = Storage()

@app.command()
def hello():
    """
    Say hello to the user.
    """
    console.print("[bold green]Hello![/bold green] Welcome to WySlMtS - your AI Productivity assistant.")

@task_app.command("add")
def add_task(
    title: str = typer.Argument(..., help="The title of the task"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="Description of the task"),
    priority: Priority = typer.Option(Priority.MEDIUM, "--priority", "-p", help="Task priority"),
):
    """
    Add a new task.
    """
    task = Task(title=title, description=description, priority=priority)
    storage.add_task(task)
    console.print(f"[bold green]Task added:[/bold green] {task.title} (ID: {str(task.id)[:8]})")

@task_app.command("list")
def list_tasks():
    """
    List all tasks.
    """
    tasks = storage.load_tasks()
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="Your Tasks")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Priority", style="magenta")
    table.add_column("Status", style="green")

    for task in tasks:
        table.add_row(
            str(task.id)[:8],
            task.title,
            task.priority.value,
            task.status.value
        )

    console.print(table)

@task_app.command("done")
def complete_task(task_id: str):
    """
    Mark a task as done by its ID (first 8 chars).
    """
    tasks = storage.load_tasks()
    found = False
    for task in tasks:
        if str(task.id).startswith(task_id):
            task.mark_done()
            found = True
            break
    
    if found:
        storage.save_tasks(tasks)
        console.print(f"[bold green]Task marked as done![/bold green]")
    else:
        console.print(f"[bold red]Task with ID starting with {task_id} not found.[/bold red]")

if __name__ == "__main__":
    app()
