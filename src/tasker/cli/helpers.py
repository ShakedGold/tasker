from pathlib import Path

TASKER_DIR_NAME = ".tasker"


def find_tasks_dir(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()

    while True:
        tasks_dir = current / TASKER_DIR_NAME

        if tasks_dir.is_dir():
            return tasks_dir

        parent = current.parent

        # We've reached the filesystem root.
        if parent == current:
            raise RuntimeError("not in a tasker project")

        current = parent


def find_all_task_paths(tasks_dir: Path) -> list[Path]:
    return [p for p in tasks_dir.iterdir() if p.is_dir()]


def find_tasks_by_partial_id(partial_task_id: str, tasks_dir: Path) -> list[Path]:
    return [p for p in tasks_dir.iterdir() if p.is_dir() if p.name.startswith(partial_task_id)]


def find_single_task_by_partial_id(partial_task_id: str, tasks_dir: Path) -> Path:
    tasks = find_tasks_by_partial_id(partial_task_id, tasks_dir)

    if len(tasks) == 0:
        raise RuntimeError(f"task({partial_task_id}) not found")

    if len(tasks) > 1:
        raise RuntimeError(
            f"task({partial_task_id}) is ambigous, matched tasks: {[task.name for task in tasks]}"
        )

    return tasks[0]
