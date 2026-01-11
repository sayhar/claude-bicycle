#!/usr/bin/env python3
"""
Warn when creating new .md files - update existing docs instead.

Allows:
  - /tmp/*.md (throwaway)
  - agents/state/sessions/*.md (session notes)
  - agents/state/inboxes/*.md (inbox files)
  - agents/oracle/observations/*.md (oracle observations)
  - Editing existing files (can't detect, but Write tool requires Read first)
"""

import json
import sys
import os


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    # This hook is for Write tool, not Bash
    if data.get("tool_name") != "Write":
        sys.exit(0)

    file_path = data.get("tool_input", {}).get("file_path", "")

    # Only care about .md files
    if not file_path.endswith(".md"):
        sys.exit(0)

    # Allow /tmp or tmp in filename
    if file_path.startswith("/tmp") or "/tmp/" in file_path:
        sys.exit(0)
    filename = os.path.basename(file_path)
    if filename.startswith("tmp") or filename.startswith("_tmp"):
        sys.exit(0)

    # Allow session notes
    if "agents/state/sessions/" in file_path:
        sys.exit(0)

    # Allow inboxes
    if "agents/state/inboxes/" in file_path:
        sys.exit(0)

    # Allow oracle observations
    if "agents/oracle/observations/" in file_path:
        sys.exit(0)

    # Check if file exists (editing existing is OK)
    if os.path.exists(file_path):
        sys.exit(0)

    # Warn about new .md file creation (but allow it)
    print(f"Warning: Creating new .md file: {file_path}")
    print("Consider: Update existing docs or use session notes. Each doc is debt.")
    sys.exit(0)


if __name__ == "__main__":
    main()
