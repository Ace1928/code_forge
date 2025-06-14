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
- **Model-based responses** powered by a small open-source language model.

## Usage

Run the chat interface. By default the engine uses the
`mradermacher/Uncensored_DeepSeek_R1_Distill_Qwen_1.5B_safetensors_finetune_2-GGUF`
model from HuggingFace:

```bash
forgengine chat
```

To select a different model:

```bash
forgengine --model sshleifer/tiny-gpt2 chat
```

Use `--max-tokens` to control the length of responses:

```bash
forgengine --max-tokens 128 chat
```

View stored interactions:

```bash
forgengine memory
```

Other subcommands include `events` and `glossary`. Use `--help` for details.

### Interactive setup

Running `forgengine` with no existing configuration walks you through a short
setup. Your choices are stored in `~/.forgengine.json` and reused on subsequent
runs. Use `--setup` at any time to reconfigure.

