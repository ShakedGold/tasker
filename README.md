# Tasker - A tool to manage your tasks with the code

## Features
All of the normal task creation features you think are here, here are some of the interesting ones

- Finding tasks based on TQL ([Task Query Language](./docs/TQL.md))
- `cat/bat` like task displaying (meaning you can display multiple tasks like in `cat`, they are markdown formatted in the terminal like `bat`)
- Editing tasks with `$EDITOR`

## Installing
Installing is easy, you can use `uv tool install` to install this from the remote repo, or clone it and install it locally:
```bash
uv tool install git+https://github.com/ShakedGold/tasker.git
```

## The `tasker` format
The [Tasker Format](./docs/tasker-format.md) is the format in which an entire tasker project is defined, it mentions how a tasker project is structured
in the file system, how the tasks themselves should be formatted.
And how the config file works.

## Why?
I needed an issue manager for [playday](https://github.com/ShakedGold/playday-api.git), And had these constraints:
1. Need a non vendor lock-in issue manager (so github's builtin issue tracker is gone)
2. Need an open source tracker (jira, trello, ... are gone)
3. Need an readable format, so even if I later switch to a different issue tracker, it is seamless/super easy (think obsidian for issues)
4. Syncable with online tools and version control so there is a single source of truth

I looked online and found some cool projects (big shoutout to https://github.com/tsoding/tatr which game me the idea to create this project)
however they were either lacking in features or too strict in their format.

My goal was to create a generic issue manager (so even the `'status'` is not required, it is just a convention), I wanted it to be simple yet powerfull.
I could not find anything online, so I just had to create my own.

> [!NOTE] tasker is not dependant on any source control/remote file managers like ftp, so you can safely use it with whatever you want, everything is self-contained within the `.tasker/` directory

### Syncing and SSOT (Single Source of Truth)
A big part of why I did not use any other existing task/issue managers that are in repo, is that they provided no way to have a single point where all issues are in.
The reason I want this is to be able to look in one place, see all of my issues and know who is working on what.

#### Possible solutions I tried with existing software
- Syncing with remote repo for every single task/issue creation => this failed since it is slow, and error prone, meaning it is easy to create 2 tasks of the same id and have a merge conflict
- Having unique ids for tasks => this failed since most fully unique ids (e.g. UUID, hash, ...) are very cumbersome to remember
- One branch to rule them all => Sucks for obvious reasons and ties the entire tasker project into git

#### The solution I came up with
My solution to this problem is basically nothing, I do not enforce any syncing of tasks, however we do allow the option to create tasks with "UUID"s that are readable and memorable.
My advice, is that if you are working by yourself on a small-medium project, you can get away with the default task generation (counter: 1, 2, 3, ...).
However, if you do need a unique identifier of the task there are multiple options defined in the config you can use (for example: "proquint"-esq which makes unique ids that are readable).
After creating your unique task, you can push it directly if you want to (using any version control, remote server, for example: git, ftp, scp, ...) into a single source of truth (for git it can be just a remote branch)

So the flow of creating tasks is still totally offline but it is very hard to have duplicates if you want to avoid them.

##### Example for git with remotes
I recommend the following flow for git:

- `git switch tasker` - switch to a branch that will contain all tasks (will never get merged, just a collection of tasks)
- `tasker new` - create a new task using the generation defined in the config file
- `git add .tasker` - add the new task after editing it
- `git commit -m "task(#): created"` - commit you changes
- `git push` - optionally push to a remote if exists in order to keep you tasks pushed (although you can do this later as well)

This is just my workflow I recommend using, you can just as easily create a different one that keeps an SSOT :)
This is a script I created to allow tasker to work in a git repo.

If you put this in your $PATH and then execute `git tasker ...` it will execute this script.
```bash
#!/usr/bin/env bash

set -euo pipefail

git switch -C tasker > /dev/null 2>&1

if [[ "$1" == "sync" ]]; then
  echo "Syncing tasker branch..."
  git pull --rebase &>/dev/null

  exit
fi

tasker $@

if [ -n "$(git status --short)" ]; then
  git add -A
  echo "Committing tasker changes" && git commit -m "tasker" > /dev/null

  if git ls-remote --exit-code --heads origin tasker > /dev/null 2>&1; then
    echo "Pushing tasker changes..." && git push &> /dev/null || \
    echo "Remote changes detected, rebasing..." && git pull --rebase &>/dev/null && \
    echo "Pushing tasker changes..." && git push &> /dev/null
  fi
fi

git switch - > /dev/null 2>&1
```

After each tasker command, it checks to see if there are any changes, if there are it tries to sync them with a remote if it exists.
You can use `git tasker sync` to sync it manually from the remote
