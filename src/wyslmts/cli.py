import typer
import questionary
from rich.console import Console
from rich.table import Table
from typing import Optional

from wyslmts.models import Task, Priority
from wyslmts.storage import Storage
from wyslmts.ai_service import AIService
from wyslmts.notifications import send_notification
from wyslmts.utils import error_exit, success_print, info_print
from wyslmts.config import Config

app = typer.Typer(
    name="wyslmts",
    help="Personal AI Productivity CLI",
    add_completion=False,
)
task_app = typer.Typer(help="Manage your tasks")
research_app = typer.Typer(help="AI Research Agent")
summary_app = typer.Typer(help="Daily summaries")
config_app = typer.Typer(help="Manage settings")

app.add_typer(task_app, name="task")
app.add_typer(research_app, name="research")
app.add_typer(summary_app, name="summary")
app.add_typer(config_app, name="config")

console = Console()
storage = Storage()
config = Config()

def get_ai_service():
    try:
        return AIService()
    except ValueError as e:
        error_exit(str(e))

@app.command()
def hello():
    """
    Say hello to the user.
    """
    console.print("[bold green]Hello![/bold green] Welcome to WySlMtS - your AI Productivity assistant.")

@app.command("interactive")
def interactive_mode():
    """
    Start the interactive shell mode.
    """
    info_print("Entering Interactive Mode... (type 'exit' to quit)")
    
    while True:
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "List Tasks",
                "Add Task",
                "Complete Task",
                "Research Topic",
                "Generate Daily Summary",
                "Settings",
                "Exit"
            ]
        ).ask()

        if action == "Exit" or action is None:
            break
        elif action == "List Tasks":
            list_tasks()
        elif action == "Add Task":
            title = questionary.text("Task Title:").ask()
            if title:
                priority = questionary.select(
                    "Priority:",
                    choices=["low", "medium", "high"],
                    default="medium"
                ).ask()
                add_task(title=title, priority=Priority(priority))
        elif action == "Complete Task":
            tasks = [t for t in storage.load_tasks() if t.status != "done"]
            if not tasks:
                console.print("[yellow]No tasks to complete.[/yellow]")
                continue
            task_choices = [f"{str(t.id)[:8]} - {t.title}" for t in tasks]
            selected = questionary.select("Select task to complete:", choices=task_choices).ask()
            if selected:
                task_id = selected.split(" - ")[0]
                complete_task(task_id=task_id)
        elif action == "Research Topic":
            topic = questionary.text("Topic to research:").ask()
            if topic:
                research_topic(topic=topic)
        elif action == "Generate Daily Summary":
            generate_summary()
        elif action == "Settings":
            key = questionary.select(
                "Which setting to update?",
                choices=["openai_api_key", "tavily_api_key", "openai_model", "Back"]
            ).ask()
            if key != "Back":
                value = questionary.text(f"Enter value for {key}:").ask()
                if value:
                    config_set(key, value)

@config_app.command("set")
def config_set(key: str, value: str):
    """
    Set a configuration value.
    """
    config.set(key, value)
    success_print(f"Setting {key} updated.")

@config_app.command("get")
def config_get(key: str):
    """
    Get a configuration value.
    """
    value = config.get(key)
    if value:
        console.print(f"{key}: {value}")
    else:
        info_print(f"Setting {key} not found.")

@config_app.command("list")
def config_list():
    """
    List all configuration values.
    """
    if not config.settings:
        info_print("No settings configured.")
        return
    
    table = Table(title="Settings")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="magenta")
    
    for k, v in config.settings.items():
        # Mask API keys
        display_v = v
        if "key" in k:
            display_v = "*" * (len(v) - 4) + v[-4:] if len(v) > 4 else "****"
        table.add_row(k, display_v)
    
    console.print(table)

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
    success_print(f"Task added: {task.title} (ID: {str(task.id)[:8]})")
    send_notification("New Task", f"Added: {task.title}")

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
def complete_task(task_id: str = typer.Argument(..., help="The ID or prefix of the task")):
    """
    Mark a task as done by its ID (or a unique prefix).
    """
    tasks = storage.load_tasks()
    matches = [t for t in tasks if str(t.id).startswith(task_id)]
    
    if not matches:
        error_exit(f"No task found starting with '{task_id}'.")
    
    if len(matches) > 1:
        error_exit(f"Multiple tasks found starting with '{task_id}'. Please be more specific.")
    
    task = matches[0]
    task.mark_done()
    storage.save_tasks(tasks)
    success_print(f"Task '{task.title}' marked as done!")

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
    send_notification("Research Complete", f"Finished researching: {topic}")
    
    if typer.confirm("\nWould you like to add a task based on this research?"):
        task_title = f"Review research: {topic}"
        task = Task(title=task_title, description=f"AI Research generated for: {topic}")
        storage.add_task(task)
        success_print(f"Task added: {task_title}")

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
