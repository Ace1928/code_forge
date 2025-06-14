# Code Forge Narrative Engine

This repository contains a proof-of-concept narrative engine that maintains
persistent memory of conversations and events. The system can run in an
interactive chat mode from the command line, storing all interactions in a
local JSON file. During idle periods the engine generates autonomous
"thoughts" that are also recorded.

## Features

- **Persistent memory** stored in `memory.json` by default.
- **Glossary** that counts words the engine encounters.
- **Idle thinking**: the engine reflects on the last message when no input has
  been received for a configurable period.
- **Command line interface** with subcommands to chat and inspect memory.

## Usage

Run the chat interface:

```bash
python -m forgeengine.cli chat
```

View stored interactions:

```bash
python -m forgeengine.cli memory
```

Other subcommands include `events` and `glossary`. Use `--help` for details.

