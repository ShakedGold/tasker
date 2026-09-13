---
status: closed
priority: 100
kind: feature
tags:
    - scope
    - config
---

# Add a default option to the config that will be added to new tasks

## Example

```toml
[properties.status]
type = "enum"
values = ["open", "closed"]
default = "open"
```

then when running `tasker new` it will create

```yaml
---
status: open
---
```
