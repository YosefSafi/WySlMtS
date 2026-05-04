import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from wyslmts.models import Task, Priority
from wyslmts.storage import Storage
from wyslmts.ai_service import AIService

app = typer.Typer(
    name="wyslmts",
    help="Personal AI Productivity CLI",
    add_completion=False,
)
task_app = typer.Typer(help="Manage your tasks")
research_app = typer.Typer(help="AI Research Agent")
summary_app = typer.Typer(help="Daily summaries")

app.add_typer(task_app, name="task")
app.add_typer(research_app, name="research")
app.add_typer(summary_app, name="summary")

console = Console()
storage = Storage()

def get_ai_service():
    try:
        return AIService()
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)

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

@research_app.command("topic")
def research_topic(topic: str = typer.Argument(..., help="The topic to research")):
    """
    Research a topic using AI.
    """
    ai = get_ai_service()
    with console.status(f"[bold blue]Researching {topic}..."):
        result = ai.research_topic(topic)
    
    console.print(f"\n[bold cyan]Research Results for: {topic}[/bold cyan]\n")
    console.print(result)
    
    # Optionally add as a task
    if typer.confirm("\nWould you like to add a task based on this research?"):
        task_title = f"Review research: {topic}"
        task = Task(title=task_title, description=f"AI Research generated for: {topic}")
        storage.add_task(task)
        console.print(f"[bold green]Task added:[/bold green] {task_title}")

@summary_app.command("generate")
def generate_summary():
    """
    Generate a daily productivity summary.
    """
    tasks = storage.load_tasks()
    if not tasks:
        console.print("[yellow]No tasks to summarize.[/yellow]")
        return

    ai = get_ai_service()
    tasks_str = "\n".join([f"- {t.title} ({t.status.value})" for t in tasks])
    
    with console.status("[bold blue]Generating daily summary..."):
        summary = ai.summarize_day(tasks_str)
    
    console.print("\n[bold magenta]Daily Productivity Summary[/bold magenta]\n")
    console.print(summary)

if __name__ == "__main__":
    app()
