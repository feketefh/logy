# beauty-log

A lightweight, customizable Python logger with color support, tree-based message formatting, grouping, and file output.

## Installation

```bash
pip install beauty-log
```

## Requirements

- Python 3.12+
- colorama

## Quick Start

```python
from beauty_log import Logger

logger = Logger(
    tree=["{time}", "{level}", "{message}"],
)

logger.console("Application started")
logger.console("Something went wrong", level="ERROR")
```

Output:

```
12:00:01 INFO Application started
12:00:01 ERROR Something went wrong
```

## Usage

### Basic Setup

```python
from beauty_log import Logger

logger = Logger(
    tree=["{time}", "{level}", "{message}"],   # defines the output format
)
```

### Log Levels

| Level | Color |
|-------|-------|
| `DEBUG` | Cyan |
| `INFO` | Blue |
| `SUCCESS` | Green |
| `WARNING` | Yellow |
| `ERROR` | Red |
| `CRITICAL` | Magenta |

```python
logger.console("Loaded config",     level="DEBUG")
logger.console("Server started",    level="SUCCESS")
logger.console("Disk space low",    level="WARNING")
logger.console("Connection failed", level="ERROR")
logger.console("System failure",    level="CRITICAL")
```

### Custom Color Scheme

Override the default colors or add custom levels entirely:

```python
from colorama import Fore

logger = Logger(
    tree=["{time}", "{level}", "{message}"],
    levelColorScheme={
        "INFO":    Fore.WHITE,
        "SUCCESS": Fore.GREEN,
        "DB":      Fore.CYAN,    # custom level
        "AUTH":    Fore.MAGENTA, # custom level
    }
)

logger.console("Query executed", level="DB")
logger.console("User logged in", level="AUTH")
```

### Tree Formatting

The `tree` parameter defines the structure of each log line. Each element is a segment that supports built-in placeholders:

| Placeholder | Value |
|-------------|-------|
| `{message}` | The log message |
| `{time}` | Current time (`HH:MM:SS`) |
| `{level}` | Colored level label |

```python
logger = Logger(tree=["[{time}]", "[{level}]", ">>", "{message}"])
# [12:00:01] [INFO] >> Server is running
```

### Variables

Pass custom variables to be substituted anywhere in the tree:

```python
logger = Logger(
    tree=["{time}", "[{module}]", "{level}", "{message}"],
    variables={"{module}": "database"}
)

logger.console("Connected successfully", level="SUCCESS")
# 12:00:01 [database] SUCCESS Connected successfully
```

### Grouping

Use `setGroupLevel()` to indent related log messages and visually group them:

```python
logger.console("Starting app", level="INFO")

logger.setGroupLevel(1)
logger.console("Loading config", level="DEBUG")
logger.console("Connecting to DB", level="DEBUG")

logger.setGroupLevel(2)
logger.console("Running migrations", level="DEBUG")
logger.setGroupLevel(1)

logger.console("Ready", level="SUCCESS")
logger.setGroupLevel(0)

logger.console("App started", level="SUCCESS")
```

Output:

```
12:00:01 INFO    Starting app
  12:00:01 DEBUG   Loading config
  12:00:01 DEBUG   Connecting to DB
    12:00:01 DEBUG   Running migrations
  12:00:01 SUCCESS  Ready
12:00:01 SUCCESS App started
```

### Saving to File

```python
logger.save("Server started", level="INFO", logFile="app.log")
```

ANSI color codes are automatically stripped from file output.

### log()

Log to both the terminal and a file in one call:

```python
logger.log("User signed up", level="SUCCESS", logFile="app.log")
```

### Timer

Measure and log execution time using the context manager:

```python
with logger.timer("Database query"):
    results = db.execute(query)
# logs: Database query took 42.30ms

# Automatically escalate to WARNING if a threshold is exceeded
with logger.timer("API call", warnAfter=200):
    response = requests.get(url)
# logs as WARNING if it takes over 200ms
```

## API Reference

### `Logger(tree, levelColorScheme, variables)`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `tree` | `list` | `None` | Output format segments |
| `levelColorScheme` | `dict` | Built-in colors | Map of level names to colorama colors |
| `variables` | `dict` | `None` | Custom substitution variables |

### `console(message, level, useBuiltIns)`

Print a formatted message to the terminal.

### `save(message, level, logFile, useBuiltIns)`

Write a message to a log file (colors stripped automatically).

### `log(message, level, logFile)`

Print to terminal and write to file.

### `setGroupLevel(groupLevel)`

Set the current indent depth. Accepts any non-negative integer. Raises `ValueError` for negative values.

### `timer(label, level, warnAfter)`

Context manager that measures execution time and logs the result.

## License

This project is licensed under the GNU General Public License v3.0 — see the [LICENSE](LICENSE) file for details.
