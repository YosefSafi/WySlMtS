import typer
from rich.console import Console

app = typer.Typer(
    name="wyslmts",
    help="Personal AI Productivity CLI",
    add_completion=False,
)
console = Console()

@app.command()
def hello():
    """
    Say hello to the user.
    """
    console.print("[bold green]Hello![/bold green] Welcome to WySlMtS - your AI Productivity assistant.")

if __name__ == "__main__":
    app()
