# Smart Task Manager (CLI)

A command-line task manager built in Python — no frameworks, no third-party dependencies, just the standard library. Built incrementally as a learning project: started as a basic in-memory task list, grew feature by feature into a persistent tool with live weather-aware risk advisories and a runtime-configurable rules engine.

## What it does

- Add, view, mark done, and delete tasks — persisted to disk as JSON.
- Look up live weather for any city (via [wttr.in](https://wttr.in), no API key required).
- Flag outdoor tasks as "risky" based on real-time weather conditions and temperature thresholds.
- Fully configurable: outdoor-task keywords, risky weather conditions, and temperature bounds live in a JSON config file, editable at runtime through a settings menu — no code changes required.
- Text-command interface for the main menu (in progress).

## Why it's built this way

Every feature was added as a deliberate step, not planned all at once:

1. In-memory task list (two parallel lists → refactored to a single list of dicts once that design broke down)
2. JSON persistence, with validation against corrupted or malformed files
3. Live weather integration using only `urllib` — no `requests`, since a single GET call doesn't justify a dependency
4. Weather-based risk advisory for outdoor tasks
5. Config-driven rules — keywords and thresholds moved out of code and into a JSON file, editable live
6. Text-command parsing for the main menu *(current)*

The commit history reflects this progression — each stage is a real, tested addition, not a rewrite.

## Tech stack

Python 3, standard library only: `json`, `pathlib`, `urllib`.

## Running it

```bash
python3 src/main.py
```

No setup required beyond Python 3 — no `pip install`, no API keys. Data and config files are created automatically on first run.

## Project structure

```
Taskmanager/
├── src/
│   ├── main.py            # entry point, command routing
│   ├── task.py            # task CRUD + JSON persistence
│   ├── weather.py         # wttr.in integration
│   └── confif.py          # config loading, validation, live editing
├── data/
│   ├── tasks.json          # created automatically, not tracked in git
│   └── config.json         # created automatically, not tracked in git
```

## Status

Actively being built and extended — this is a live learning project, not a finished product. Next: replacing the numbered menu entirely with text commands, then wiring in an LLM API for smarter task handling.