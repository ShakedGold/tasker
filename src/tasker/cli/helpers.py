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
    task_names = [task.name for task in tasks]
    found_task = None

    if len(tasks) == 0:
        raise RuntimeError(f"task({partial_task_id}) not found")

    full_task_matches = list(filter(lambda task: task.name == partial_task_id, tasks))

    if len(full_task_matches) == 1:
        found_task = full_task_matches[0]
    elif len(tasks) > 1:
        raise RuntimeError(f"task({partial_task_id}) is ambigous, matched tasks: {task_names}")
    else:
        found_task = tasks[0]

    return found_task
