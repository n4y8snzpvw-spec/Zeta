from __future__ import annotations

import argparse


def generate_response(prompt: str) -> str:
    """Return a simple AI-style response for the provided prompt."""
    cleaned = prompt.strip() or "hello"
    return f"Zeta response: I received '{cleaned}'. Ready to help with your next task."


def main() -> None:
    parser = argparse.ArgumentParser(description="Zeta CLI")
    parser.add_argument("prompt", nargs="?", default="hello", help="Input text for the assistant")
    args = parser.parse_args()
    print(generate_response(args.prompt))


if __name__ == "__main__":
    main()
