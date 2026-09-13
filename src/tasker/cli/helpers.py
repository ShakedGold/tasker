from pathlib import Path

def find_tasks_dir(start: Path | None = None) -> Path | None:
    current = (start or Path.cwd()).resolve()

    while True:
        tasks_dir = current / ".tasks"

        if tasks_dir.is_dir():
            return tasks_dir

        parent = current.parent

        # We've reached the filesystem root.
        if parent == current:
            return None

        current = parent

def find_all_task_paths(tasks_dir: Path) -> list[Path]:
    return [p for p in tasks_dir.iterdir() if p.is_dir() and p.name.isdigit()]
