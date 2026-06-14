import os
import sys
import subprocess

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from Solver.state import createRandomState
from Solver.annealing import runAnnealingUntil, runAnnealing
from reporter import sendResults

console = Console()


def create_spinner():
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    )


def show_menu():
    console.print(
        Panel.fit(
            "[bold cyan]Project Kobon[/bold cyan]\n"
            "[dim]Kobon Triangle Solver[/dim]",
            border_style="cyan"
        )
    )

    console.print("[bold green]1.[/] Run solver")
    console.print("[bold green]2.[/] Run until target")
    console.print("[bold green]3.[/] Open viewer")
    console.print()


def main():
    try:
        show_menu()

        choice = int(input("Select an option (1-3): ").strip())

        if choice not in (1, 2, 3):
            console.print("[bold red]Error:[/] Invalid option.")
            return

        if choice == 1:
            console.print(Rule("[cyan]Run Solver[/cyan]"))
            console.print("Usage: <k> <iterations> <restarts> <ma/mi>")

            parts = input("Enter parameters: ").split()

            if len(parts) != 4:
                console.print("[bold red]Error:[/] Please provide all 4 parameters.")
                return

            k = int(parts[0])
            iters = int(parts[1])
            restarts = int(parts[2])

            goalInput = parts[3].lower()

            if goalInput not in ("ma", "mi"):
                console.print("[bold red]Error:[/] Last parameter must be 'ma' or 'mi'.")
                return

            goalText = "MAXIMIZE" if goalInput == "ma" else "MINIMIZE"

            webhookURL = input("Enter Discord Webhook URL: ").strip()

            console.print(
                f"\n[green]Configuration complete.[/] "
                f"Running [bold]{goalText}[/bold] solver..."
            )

            with create_spinner() as progress:
                progress.add_task("[yellow]Searching for solutions...[/]", total=None)
                topResults = runAnnealing(k, iters, restarts, goalText)

            console.print("[bold green]✓ Solver finished[/]")

            with create_spinner() as progress:
                progress.add_task("[yellow]Sending results...[/]", total=None)
                sendResults(webhookURL, topResults, k, goalText)

            console.print("[bold green]✓ Results sent[/]")

        elif choice == 2:
            console.print(Rule("[cyan]Run Until Target[/cyan]"))
            console.print("Usage: <k> <reset every> <ma/mi> <target gap>")
            console.print(
                "[dim]reset every = iterations before restarting "
                "with a new random arrangement[/dim]"
            )

            parts = input("Enter parameters: ").split()

            if len(parts) != 4:
                console.print("[bold red]Error:[/] Please provide all 4 parameters.")
                return

            k = int(parts[0])
            resetEvery = int(parts[1])

            goalInput = parts[2].lower()

            if goalInput not in ("ma", "mi"):
                console.print("[bold red]Error:[/] Last parameter must be 'ma' or 'mi'.")
                return

            goalText = "MAXIMIZE" if goalInput == "ma" else "MINIMIZE"
            targetGap = int(parts[3])

            webhookURL = input("Enter Discord Webhook URL: ").strip()

            console.print(
                f"\nRunning [bold]{goalText}[/bold] solver, "
                f"resetting every [cyan]{resetEvery}[/cyan] iterations "
                f"until within [cyan]{targetGap}[/cyan] of ceiling..."
            )

            with create_spinner() as progress:
                progress.add_task("[yellow]Searching for solutions...[/]", total=None)
                topResults = runAnnealingUntil(k, resetEvery, goalText, targetGap)

            console.print("[bold green]✓ Solver finished[/]")

            with create_spinner() as progress:
                progress.add_task("[yellow]Sending results...[/]", total=None)
                sendResults(webhookURL, topResults, k, goalText)

            console.print("[bold green]✓ Results sent[/]")

        elif choice == 3:
            console.print("[cyan]Opening viewer...[/]")
            subprocess.run([sys.executable, "Viewer/viewer.py"])

    except ValueError:
        console.print("[bold red]Error:[/] Invalid input format.")

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Process stopped.[/]")
        sys.exit()


if __name__ == "__main__":
    main()