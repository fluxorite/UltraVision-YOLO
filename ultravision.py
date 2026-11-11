import os
import sys
import glob
import urllib.request

try:
    from ultralytics import YOLO
    from rich.console import Console
    from rich.table import Table
    from rich.progress import (
        track,
        Progress,
        BarColumn,
        DownloadColumn,
        TransferSpeedColumn,
        TimeRemainingColumn,
    )
except KeyboardInterrupt:
    print("\nScript stopped by user.")
    sys.exit(0)
except ImportError as e:
    print(f"Missing library: {e.name}. Install it with: pip install ultralytics rich")
    sys.exit(1)
except Exception as e:
    print(f"Startup error: {e}")
    sys.exit(1)

console = Console()

MODEL_FILE = "yolo26x.pt"
MODEL_URLS = [
    "https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26x.pt",
    "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo26x.pt",
]


def clear_screen():
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass


HEADER_WIDTH = 36  # width of the YOLO X ASCII art


def show_header():
    try:
        header_text = """
 [bold yellow]__   _____  _     ___      __  __[/bold yellow]
 [bold yellow]\\ \\ / / _ \\| |   / _ \\     \\ \\/ /[/bold yellow]
 [bold yellow] \\ V / | | | |  | | | |     \\  /[/bold yellow]
 [bold yellow]  | || |_| | |__| |_| |     /  \\ [/bold yellow]
 [bold yellow]  |_| \\___/|_____\\___/     /_/\\_\\ [/bold yellow]
    [bold cyan]ULTRA VISION - OFFLINE AI[/bold cyan]
    """
        console.print(header_text)
        credit = "Made by Hansraj"
        pad = " " * ((HEADER_WIDTH - len(credit)) // 2)
        console.print(f"{pad}[bold yellow]{credit}[/bold yellow]")
    except Exception:
        pass


def download_model(dest, urls):
    """Try each URL in order and save the file to dest."""
    tmp = dest + ".part"
    for url in urls:
        try:
            console.print(f"[bold yellow]Downloading from: {url}[/bold yellow]")
            with urllib.request.urlopen(url, timeout=30) as resp, open(tmp, "wb") as out:
                total = int(resp.headers.get("Content-Length", 0)) or None
                with Progress(
                    "[cyan]Downloading...[/cyan]",
                    BarColumn(),
                    DownloadColumn(),
                    TransferSpeedColumn(),
                    TimeRemainingColumn(),
                    console=console,
                ) as progress:
                    task = progress.add_task("dl", total=total)
                    while True:
                        chunk = resp.read(1024 * 256)
                        if not chunk:
                            break
                        out.write(chunk)
                        progress.update(task, advance=len(chunk))
            os.replace(tmp, dest)
            console.print(f"[bold green][OK] {dest} downloaded.[/bold green]")
            return True
        except KeyboardInterrupt:
            if os.path.exists(tmp):
                os.remove(tmp)
            raise
        except Exception as e:
            console.print(f"[bold red][!] Download failed: {e}[/bold red]")
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass
    return False


def saved_folder(results):
    """Return the real results folder, e.g. runs/detect/predict-10."""
    try:
        return f"runs/detect/{os.path.basename(str(results[0].save_dir))}"
    except Exception:
        return "runs/detect"


def run_image(model):
    img = console.input("[bold blue]Enter Image Path/Name: [/bold blue]").strip().strip('"').strip("'")
    if os.path.exists(img):
        with console.status("[bold yellow]Processing...[/bold yellow]"):
            results = model.predict(source=img, save=True, imgsz=640)
        console.print(f"[bold green][OK] Success! Check {saved_folder(results)}[/bold green]")
    else:
        console.print(f"[bold red][!] Logically: '{img}' Not Found.[/bold red]")


def run_batch(model):
    folder_path = console.input("[bold blue]Enter Folder Path: [/bold blue]").strip().strip('"').strip("'")
    if os.path.isdir(folder_path):
        files = []
        for ext in ("*.jpg", "*.png", "*.jpeg"):
            files.extend(glob.glob(os.path.join(folder_path, ext)))

        if not files:
            console.print("[bold red][!] Logically: No images found in this folder.[/bold red]")
        else:
            console.print(f"[bold yellow]Found {len(files)} images. Starting...[/bold yellow]")
            for file in track(files, description="[cyan]Processing Batch...[/cyan]"):
                try:
                    model.predict(source=file, save=True, imgsz=640, verbose=False)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    console.print(f"[bold red][!] Skipped '{file}': {e}[/bold red]")
            console.print("[bold green][OK] Batch Processing Complete![/bold green]")
    else:
        console.print(f"[bold red][!] Logically: Folder '{folder_path}' not found.[/bold red]")


def run_video(model):
    vid = console.input("[bold blue]Enter Video Path/Name: [/bold blue]").strip().strip('"').strip("'")
    if os.path.exists(vid):
        console.print("[bold yellow]Processing Video (Heavy Task)...[/bold yellow]")
        model.predict(source=vid, save=True)
        console.print("[bold green][OK] Video Processed Successfully.[/bold green]")
    else:
        console.print(f"[bold red][!] Logically: Video '{vid}' Not Found.[/bold red]")


def main():
    os.environ["ULTRALYTICS_OFFLINE"] = "True"
    model_file = MODEL_FILE

    clear_screen()
    show_header()

    if not os.path.exists(model_file):
        console.print(f"[bold yellow][!] {model_file} not found in this folder.[/bold yellow]")
        if not download_model(model_file, MODEL_URLS):
            console.print(f"[bold red][!] Error: could not download {model_file}. Check your internet.[/bold red]")
            return

    try:
        with console.status("[bold green]Loading AI Engine...[/bold green]"):
            model = YOLO(model_file)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        console.print(f"[bold red]Crash: {e}[/bold red]")
        return

    actions = {"1": run_image, "2": run_batch, "3": run_video}

    while True:
        # Menu
        try:
            table = Table(title="MAIN MENU", style="cyan")
            table.add_column("Option", style="yellow", justify="center")
            table.add_column("Task", style="white")
            table.add_row("1", "Single Image")
            table.add_row("2", "Batch Folder (Manual Path)")
            table.add_row("3", "Single Video")
            table.add_row("exit", "Close Script")

            console.print(table)
            choice = console.input("[bold green]Action >> [/bold green]").strip().lower()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold red]Shutting down... Goodbye![/bold red]")
            return
        except Exception as e:
            console.print(f"[bold red][!] Menu error: {e}[/bold red]")
            continue

        if choice == "exit":
            console.print("[bold red]Shutting down... Goodbye![/bold red]")
            return

        action = actions.get(choice)
        if action is None:
            console.print("[bold red][!] Invalid Selection. Use 1, 2, 3 or exit.[/bold red]")
            continue

        # Task
        try:
            action(model)
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold yellow][!] Cancelled. Back to menu.[/bold yellow]")
        except Exception as e:
            console.print(f"[bold red][!] Error: {e}[/bold red]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Script stopped by user.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Crash: {e}[/bold red]")

