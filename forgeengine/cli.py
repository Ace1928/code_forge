"""Command line interface for the Narrative Engine."""

import argparse

from .engine import NarrativeEngine


def run_chat(args: argparse.Namespace) -> None:
    engine = NarrativeEngine(memory_path=args.memory, think_interval=args.think)
    engine._reset_timer()
    print("Type 'quit' or 'exit' to stop.")
    try:
        while True:
            user_input = input("> ")
            if user_input.lower().strip() in {"quit", "exit"}:
                break
            print(engine.respond(user_input))
    except KeyboardInterrupt:
        pass
    finally:
        engine.shutdown()


def show_memory(args: argparse.Namespace) -> None:
    engine = NarrativeEngine(memory_path=args.memory, think_interval=args.think)
    for item in engine.store.data.interactions:
        print(f"{item['timestamp']}: {item['user']} -> {item['response']}")


def show_events(args: argparse.Namespace) -> None:
    engine = NarrativeEngine(memory_path=args.memory, think_interval=args.think)
    for evt in engine.store.data.events:
        print(f"{evt['timestamp']}: {evt['event']}")


def show_glossary(args: argparse.Namespace) -> None:
    engine = NarrativeEngine(memory_path=args.memory, think_interval=args.think)
    for word, count in sorted(engine.store.data.glossary.items()):
        print(f"{word}: {count}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Narrative Engine CLI")
    parser.add_argument("--memory", default="memory.json", help="Memory file path")
    parser.add_argument(
        "--think", type=int, default=10, help="Seconds of idle before thinking"
    )

    sub = parser.add_subparsers(dest="command")
    chat = sub.add_parser("chat", help="Start interactive chat")
    chat.set_defaults(func=run_chat)

    mem = sub.add_parser("memory", help="Show stored interactions")
    mem.set_defaults(func=show_memory)

    evt = sub.add_parser("events", help="Show recorded events")
    evt.set_defaults(func=show_events)

    glo = sub.add_parser("glossary", help="Show learned glossary")
    glo.set_defaults(func=show_glossary)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()

