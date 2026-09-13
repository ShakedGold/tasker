---
status: open
priority: 50
kind: feature
---

# Add commands to tasker in .config.toml

## How will commands work?

You can define a command in the tasker config and then invoke it with
```console
tasker cmd ...
```

### Example

`.config.toml`:
```toml
[cmds.tag]
property = tags
```

will work like so:
```console
tasker cmd --id 6 tag add scope
tasker cmd --id 6 tag remove scope
```

we can auto detect the subactions you can do on the property by its type
