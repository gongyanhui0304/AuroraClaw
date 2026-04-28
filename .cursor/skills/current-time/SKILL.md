---
name: current-time
description: Query the current date and time from the local system and return it in the user's preferred format. Use when the user asks for current time, date, timezone, today, now, or timestamp.
---

# Current Time

## Purpose

Provide reliable "current time" responses by reading system time directly instead of estimating from context.

## When To Use

Apply this skill when the user asks to:

- Check current time or current date
- Get today's weekday/date
- Show local timezone time
- Return an ISO timestamp

Typical trigger words include: `当前时间`, `几点`, `现在`, `今天`, `time now`, `current time`, `today`, `timestamp`.

## Workflow

1. Detect the user's preferred output style (brief, normal, or structured).
2. Run a shell command to fetch local system time:
   - PowerShell: `Get-Date -Format "yyyy-MM-dd HH:mm:ss K"`
   - Optional ISO: `Get-Date -Format "o"`
3. If the user asks for timezone details, also return timezone name and UTC offset.
4. Respond clearly, and avoid extra explanation unless requested.

## Output Format

Default format:

```markdown
当前时间：<yyyy-MM-dd HH:mm:ss ±HH:mm>
```

If user asks for detailed output:

```markdown
当前时间：<yyyy-MM-dd HH:mm:ss ±HH:mm>
ISO 8601：<timestamp>
时区：<timezone name>
```

## Guardrails

- Always query system time via shell; do not guess.
- Keep format consistent unless the user asks for another format.
- If the command fails, report the failure briefly and retry once.
- If user requests another timezone, clarify whether conversion is needed.

## Examples

User: `现在几点了？`

Assistant:

`当前时间：2026-04-24 14:35:10 +08:00`

User: `给我 ISO 时间戳`

Assistant:

`ISO 8601：2026-04-24T14:35:10.1234567+08:00`
