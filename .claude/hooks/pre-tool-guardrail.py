#!/usr/bin/env python3
"""
Pre-Tool Guardrail Hook — Intercepts tool calls and checks against safety rules.

This is a PreToolUse hook that receives the tool name and input, then returns
a decision to allow or block the tool call.

Hook protocol:
  - Receives JSON on stdin: {"session_id", "tool_name", "tool_input", ...}
  - Returns JSON on stdout: {"decision": "allow"} or {"decision": "block", "reason": "..."}

Guardrail rules (from SOUL.md):
  1. Never send emails; never send Teams messages except to Frank's own notes-to-self chat
  2. Never post to social media
  3. Never access financial data
  4. Never delete anything without permission
  5. Block dangerous shell commands
"""

import json
import os
import re
import sys
from pathlib import Path

# Add scripts dir to path for importing guardrails
SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

# Frank's Teams notes-to-self chat. The only chat the agent may post to.
SELF_CHAT_ID = "19:c142cf69-5033-4b79-9f1b-df23832c13d9_7cb48f87-e8c5-4ac2-8858-9b5433fc0d79@unq.gbl.spaces"
TEAMS_SEND_SUFFIX = "teams_send_chat_message"
ALWAYS_BLOCK_SUFFIXES = (
    "teams_create_chat",
    "teams_send_channel_message",
    "teams_reply_channel_message",
    "outlook_send_mail",
    "outlook_send_draft",
    "outlook_forward_mail",
)


def check_connector_send(tool_name: str, tool_input: dict) -> dict | None:
    """Allow Teams sends only to the self-chat; block every other outbound send."""
    if tool_name.endswith(TEAMS_SEND_SUFFIX):
        if tool_input.get("chatId") == SELF_CHAT_ID:
            return {"decision": "allow"}
        return {"decision": "block", "reason": "Teams send only allowed to Frank's notes-to-self chat"}
    if tool_name.endswith(ALWAYS_BLOCK_SUFFIXES):
        short = tool_name.rsplit("__", 1)[-1]
        return {"decision": "block", "reason": f"Outbound send blocked by guardrail ({short})"}
    return None


def check_bash_command(command: str) -> dict:
    """Check a Bash command against guardrail rules."""
    try:
        from guardrails import check_command
        result = check_command(command)
        if result.blocked:
            return {"decision": "block", "reason": result.reason}
        return {"decision": "allow"}
    except ImportError:
        # Fallback: basic checks if guardrails module not available
        dangerous = [
            (r'\brm\s+(-[a-zA-Z]*[rf]|--force)', "Destructive delete operation"),
            (r'\bsudo\b', "Elevated privilege command"),
            (r'(?i)\bcurl\b.*\|\s*bash', "Remote code execution"),
            (r'\bgit\s+push\s+.*--force', "Force push"),
        ]
        for pattern, reason in dangerous:
            if re.search(pattern, command):
                return {"decision": "block", "reason": reason}
        return {"decision": "allow"}


def check_file_write(filepath: str) -> dict:
    """Check if writing to a file should be allowed."""
    filepath_lower = filepath.lower()

    # Block writing to financial files
    financial_keywords = ["invoice", "payment", "salary", "bank", "payroll"]
    for keyword in financial_keywords:
        if keyword in filepath_lower:
            return {"decision": "block", "reason": f"Writing to financial data file blocked ('{keyword}')"}

    # Block writing outside the project directory
    allowed_roots = [
        "/Users/frank.enendu/Documents/Personal/Second Brain Starter",
        "/Users/frank.enendu/Documents/Projects",
        "/sessions/",  # Cowork sandbox
    ]
    is_allowed = any(filepath.startswith(root) for root in allowed_roots)
    if not is_allowed and not filepath.startswith("/tmp/"):
        return {"decision": "block", "reason": f"Writing outside allowed directories: {filepath}"}

    return {"decision": "allow"}


def main():
    """Main hook entry point."""
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        # If we can't read input, allow by default (don't break the agent)
        json.dump({"decision": "allow"}, sys.stdout)
        return

    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})
    if not isinstance(tool_input, dict):
        tool_input = {}

    # Check Bash commands
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        result = check_bash_command(command)
        json.dump(result, sys.stdout)
        return

    # Check file writes
    if tool_name in ("Write", "Edit"):
        filepath = tool_input.get("file_path", "")
        result = check_file_write(filepath)
        json.dump(result, sys.stdout)
        return

    connector = check_connector_send(tool_name, tool_input)
    if connector is not None:
        json.dump(connector, sys.stdout)
        return

    # All other tools: allow
    json.dump({"decision": "allow"}, sys.stdout)


if __name__ == "__main__":
    main()
