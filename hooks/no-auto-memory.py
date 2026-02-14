#!/usr/bin/env python3
"""
Block writes to Claude Code's auto-memory directory.

Persistent state belongs in bootup files or inbox, not MEMORY.md.
"""

import json
import sys


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    file_path = data.get("tool_input", {}).get("file_path", "")

    if "/.claude/" not in file_path or "/memory/" not in file_path:
        sys.exit(0)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Don't use auto-memory. Instead: "
                "(1) edit a bootup file (this.*.agent.md, *.context.md, principles/) or "
                "(2) send meta an inbox message to make the change."
            ),
        }
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
