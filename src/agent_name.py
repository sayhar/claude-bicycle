#!/usr/bin/env python3
"""
Generate memorable agent names (adjective-noun pairs).

Usage:
    uv run python src/agent_name.py           # Generate random name
    uv run python src/agent_name.py --check   # List all possible names
"""

import random
import sys

ADJECTIVES = [
    # Row 1: classic
    "swift", "calm", "bold", "keen", "warm",
    "bright", "clear", "quick", "sharp", "steady",
    "brave", "quiet", "wild", "rare", "true",
    "fair", "deep", "soft", "cool", "wise",
    # Row 2: nature
    "fleet", "still", "fierce", "gentle", "vivid",
    "stark", "dense", "pale", "dark", "light",
    "fresh", "crisp", "dry", "wet", "raw",
    "pure", "rich", "lean", "spare", "prime",
    # Row 3: character
    "glad", "kind", "stern", "mild", "tense",
    "loose", "tight", "odd", "even", "plain",
    "grand", "slight", "vast", "brief", "long",
    "late", "early", "young", "old", "new",
]

NOUNS = [
    # Row 1: birds
    "falcon", "hawk", "crow", "wren", "finch",
    "swift", "heron", "crane", "dove", "lark",
    "raven", "owl", "jay", "tern", "kite",
    # Row 2: mammals
    "fox", "wolf", "bear", "hare", "lynx",
    "otter", "mink", "stoat", "vole", "shrew",
    "stag", "doe", "elk", "boar", "ram",
    # Row 3: nature
    "river", "storm", "flame", "stone", "frost",
    "dawn", "moon", "star", "wind", "wave",
    "pine", "oak", "elm", "ash", "birch",
    # Row 4: landscape
    "cliff", "ridge", "vale", "glen", "marsh",
    "brook", "spring", "lake", "pond", "peak",
    "cave", "dune", "moor", "heath", "dale",
]


def generate_name() -> str:
    """Generate a random adjective-noun name."""
    return f"{random.choice(ADJECTIVES)}-{random.choice(NOUNS)}"


def main():
    if "--check" in sys.argv:
        print(f"Possible combinations: {len(ADJECTIVES) * len(NOUNS)}")
        print(f"Adjectives: {', '.join(ADJECTIVES)}")
        print(f"Nouns: {', '.join(NOUNS)}")
    else:
        print(generate_name())


if __name__ == "__main__":
    main()
