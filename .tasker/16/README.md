---
status: open
priority: 60
kind: feature
---

# Add tasker remotes

Kind of like git remotes, tasker remotes should work in the non-locally. For example:

- Git Repo
- SFTP
- DIRECTORY
- SCP/SSH

But unlike git, the remotes should be a SSOT always synced remote. meaning each action a user performs should be synced with the remote.
A conflict resolution in tasker should be the following:

1. Get the list of changes in the .tasker dir
2. Convert them to a list of "set" operations (expanded later)
3. Sync with the remote
4. Apply the "set" operations
5. Upload to the remote

## Set Operations
We do not want to make the user start to resolve conflicts in the .tasker project.
So unlike git, we will just have a full sync of the changes.
Meaning instead of additions/subtractions/modifications, we have a *change*, for example:
If a user changes a property from "open" to "closed" it is a *change*, and when synced to the remote it overwrites the remote completely without trying to merge

Another example:
A user adds/removes an item in a property array. instead of an *addition* or *subtraction*, the entire property is modified to the exact items in the local changes.

Same goes for the body and title
