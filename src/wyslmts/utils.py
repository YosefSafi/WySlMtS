import typer
from rich.console import Console

console = Console()

def error_exit(message: str, code: int = 1):
    console.print(f"[bold red]Error:[/bold red] {message}")
    raise typer.Exit(code=code)

def success_print(message: str):
    console.print(f"[bold green]Success:[/bold green] {message}")

def info_print(message: str):
    console.print(f"[bold blue]Info:[/bold blue] {message}")
