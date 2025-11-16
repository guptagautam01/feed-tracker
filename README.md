# Status Tracker

## Overview

`feed-tracker` is an asynchronous Python project for tracking Atom/RSS feeds, with a focus on monitoring the OpenAI status feed. It is designed for extensibility and can be adapted to track other feeds by subclassing the base tracker classes.

### Sample Output
```text
[2025-08-22T23:12:44.895Z] OpenAI : Elevated API errors and latencies
Incident Link: https://status.openai.com//incidents/01K39H0SBZ3GDWCK3MGKE6QR3G
Affected components: ['Audio (Operational)', 'Embeddings (Operational)']
```

## Project Structure

```
feed-tracker/
├── atom_tracker.py        # Base class for Atom/RSS feed tracking
├── feed_tracker.py        # Abstract base class for all feed trackers
├── main.py                # Entry point to start all trackers
├── openai_tracker.py      # Tracker for OpenAI's Atom feed
├── pyproject.toml         # Project metadata and dependencies
```

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (for dependency management and running)

## Setup Instructions

1. **Install uv** (if not already installed):

	```sh
	pip install uv
	```

2. **Install dependencies:**

	```sh
	uv pip install -r pyproject.toml
	```

	Or, to create a virtual environment and install dependencies:

	```sh
	uv venv .venv
	source .venv/bin/activate
	uv pip install -r pyproject.toml
	```

## Running the Project

To start the feed tracker(s):

```sh
uv run main.py
```

This will start the OpenAI feed tracker. You can extend `main.py` to add more trackers as needed.

### Skipping Old Feed Entries (clear_backlog)

In `main.py`, you can control whether historical (old) feed entries are processed on startup using the `clear_backlog` variable:

```python
clear_backlog = False 
```

- If `clear_backlog` is set to `True`, the tracker will skip processing all existing entries in the feed when it first starts, and will only process new entries that appear after startup.
- If `clear_backlog` is set to `False`, the tracker will process all entries, including historical ones, on the first run.

Adjust this variable as needed for your use case.

## Extending

- To add a new feed tracker, subclass `FeedTracker` or `AtomFeedTracker` and implement the required methods.
- Register your tracker in `main.py`.
