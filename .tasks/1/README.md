---
priority: 100
status: closed
tags:
    - scope
    - meta
---

# Create a task branch to save all of the tasks to

## How does the task branch work
<REMOTE>/tasks branch should be the single source of truth for all tasks in the project
Every new task should be created here first in the remote, then push (without forcing, so you know the task did not get created yet)

## How to create a new task
Just create a directory in .tasks with the issue number (incrementing from the last one), then push it to the remote

### Filling the .tasks/<ID>/README.md
The first lines in the README.md of the task are the properties of that task, in yaml form.
there are multiple options you can include, exclude:

- status => will display the current tasks status (closed, open, ...)
- priority => will display the priority of the task (0-100)
- tags => a list of user defined tags to add to the task

All of the options in those properties are changeable in the .tasks/config.toml file
