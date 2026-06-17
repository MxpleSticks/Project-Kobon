import multiprocessing
import sys
import subprocess
import os

import random
import numpy as np
import time
import math

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from Solver.state import createRandomState
from Solver.annealing import runAnnealingUntil, runAnnealing
from reporter import sendResults

console = Console()

def workerRun(arg):
    maxSeed = 2**32 - 1
    
    seed = (int((time.time() * 1000)) + os.getpid()) % maxSeed
    
    random.seed(seed)
    np.random.seed(seed)
    
    k, iters, restarts, goalText = arg
    return runAnnealing(k, iters, restarts, goalText)


def workerRunUntil(arg):
    maxSeed = 2**32 - 1
    
    seed = (int((time.time() * 1000)) + os.getpid()) % maxSeed
    random.seed(seed)
    np.random.seed(seed)
    k, resetEvery, goalText, targetGap = arg

    return runAnnealingUntil(k, resetEvery, goalText, targetGap)

def getScore(resultItem):
    return resultItem[0]


def mergeResults(resultsList):
    allResults = []
    for i in resultsList:
        allResults.extend(i)
    
    allResults.sort(key=getScore, reverse=True)

    finalTop = []
    seenScores = set()

    for i in allResults:
        score = i[0]
        if(score not in seenScores):
            finalTop.append(i)
            seenScores.add(score)
        if(len(finalTop) == 3):
            break
    
    return finalTop

def getWorkerCount():
    totalCores = os.cpu_count()
    safeMaxLimit = max(1, totalCores - 1)
    safeModeDefault = max(1, totalCores - 4)

    console.print(
    f"[dim]Recommended: {safeModeDefault} workers[/dim]"
    )
    console.print(
        f"[dim]Maximum: {safeMaxLimit} workers[/dim]"
    )
    
    choice = input(f"Worker Processes [{safeModeDefault}]: ").strip().lower()

    if choice == "max":
        console.print(f"[cyan]Using maximum worker count:[/] {safeMaxLimit}")
        return safeMaxLimit
    elif(choice.isdigit()):
        userChoice = int(choice)
        actual = min(userChoice, safeMaxLimit)
        return actual
    else:
        return safeModeDefault


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

            workers = getWorkerCount()
            restartsPerWorker = math.ceil(restarts / workers)
            tasks = [(k, iters, restartsPerWorker, goalText) for _ in range(workers)]

            with create_spinner() as progress:
                progress.add_task(f"[yellow]Searching with {workers} workers...[/]", total=None)
                with multiprocessing.Pool(processes=workers) as pool:
                    raw_results = pool.map(workerRun, tasks)
                    topResults = mergeResults(raw_results)

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

            workers = getWorkerCount()
            tasks = [(k, resetEvery, goalText, targetGap) for _ in range(workers)]

            with create_spinner() as progress:
                progress.add_task(f"[yellow]Racing {workers} workers to target...[/]", total=None)
                with multiprocessing.Pool(processes=workers) as pool:
                    for result in pool.imap_unordered(workerRunUntil, tasks):
                        topResults = result
                        pool.terminate()
                        break

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
    multiprocessing.freeze_support()
    main()