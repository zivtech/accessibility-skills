"""CLI entry point. See README.md for receipt and identity requirements."""
import argparse
import json
from .freeze import CONDITION, freeze, verify_files
from .runner import run, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("freeze", "verify-files", "summary", "run"):
        command = commands.add_parser(name)
        command.add_argument("--out", required=True)
        if name == "freeze":
            command.add_argument("--num-predict", type=int, default=16384)
            command.add_argument("--condition", default=CONDITION)
        if name == "run":
            command.add_argument("--model", required=True)
            command.add_argument("--stage", choices=("screen", "clean", "bugreport"), required=True)
            command.add_argument("--backend", choices=("ollama", "openai"), required=True)
            command.add_argument("--url", required=True)
            command.add_argument("--shared-url", default="http://127.0.0.1:11434")
            command.add_argument("--draws", type=int, default=3)
            command.add_argument("--num-predict", type=int, default=16384)
            command.add_argument("--identity-file")
    args = parser.parse_args()
    if args.command == "run" and args.draws != 3:
        parser.error("the fixed CLEAN condition requires --draws 3")
    try:
        if args.command == "freeze":
            result = freeze(args.out, args.num_predict, args.condition)
        elif args.command == "verify-files":
            result = verify_files(args.out)
        else:
            result = summary(args.out) if args.command == "summary" else run(args)
    except (ValueError, RuntimeError, OSError) as error:
        parser.exit(1, f"FAIL CLOSED: {error}\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
