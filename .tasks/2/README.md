---
status: closed
priority: 100
tags:
    - scope
    - meta
---

# Add filters to the `ls` command to filter on properties

## Filter options

All of the logical operations should work (and, or, not)
You should be able to search for a specific property with a specific value

## Examples

```console
tasker find .status eq open
tasker find .priority gt 50
tasker find .tags has scoped
```
