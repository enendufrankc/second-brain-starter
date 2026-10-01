#!/usr/bin/env python3
"""
Sanitize — Three-layer sanitization for external data entering the second brain.

Layer 1: Pattern detection — identifies URLs, code blocks, suspicious instructions
Layer 2: Markdown escaping — neutralizes formatting that could confuse the LLM
Layer 3: Trust boundaries — wraps external data in XML tags for clear separation

All text from Teams, Outlook, and GitLab should pass through this before being
stored in the vault or passed to Claude for reasoning.

Usage:
    # As a library
    from sanitize import sanitize_external_text, SanitizeConfig

    clean = sanitize_external_text(raw_text, source="teams")

    # As a CLI
    echo "some text" | python3 sanitize.py --source teams
    python3 sanitize.py --source outlook --file message.txt
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SanitizeConfig:
    """Configuration for sanitization behavior."""
    strip_urls: bool = False           # Don't strip, but escape
    escape_code_blocks: bool = True    # Escape backtick blocks
    wrap_trust_boundary: bool = True   # Add <external_data> tags
    max_length: int = 10000            # Truncate beyond this
    detect_injections: bool = True     # Flag suspicious patterns


# Patterns that look like prompt injection attempts
INJECTION_PATTERNS = [
    r"(?i)ignore\s+(?:all\s+)?(?:previous|above|prior)\s+instructions",
    r"(?i)you\s+are\s+now\s+(?:a|an|in)\s+",
    r"(?i)system\s*:\s*",
    r"(?i)(?:new|updated?)\s+instructions?\s*:",
    r"(?i)(?:admin|root|sudo)\s+(?:mode|access|override)",
    r"(?i)forget\s+(?:everything|all|your)\s+",
    r"(?i)disregard\s+(?:your|all|previous)",
    r"(?i)act\s+as\s+(?:if|though)\s+you",
    r"(?i)<\s*(?:system|admin|prompt|instruction)",
    r"(?i)\[INST\]",
    r"(?i)<<\s*SYS\s*>>",
]

# Patterns for detecting embedded commands
COMMAND_PATTERNS = [
    r"(?i)(?:please\s+)?(?:run|execute|eval)\s+(?:this|the\s+following)",
    r"(?i)(?:curl|wget|fetch)\s+https?://",
    r"(?i)(?:rm|del|delete)\s+-rf?\s+",
    r"(?i)(?:pip|npm)\s+install\s+",
]

# Social media domains to flag
SOCIAL_DOMAINS = [
    "twitter.com", "x.com", "facebook.com", "instagram.com",
    "tiktok.com", "linkedin.com", "reddit.com",
]

# Financial data patterns to flag
FINANCIAL_PATTERNS = [
    r"(?i)\b(?:invoice|payment|salary|bank\s*account|credit\s*card|routing\s*number)\b",
    r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",  # Credit card-like numbers
    r"\b(?:sort\s*code|iban|swift|bic)\b",
]


def detect_injections(text: str) -> list:
    """Detect potential prompt injection patterns."""
    findings = []
    for pattern in INJECTION_PATTERNS:
        matches = re.finditer(pattern, text)
        for match in matches:
            findings.append({
                "type": "injection",
                "pattern": pattern,
                "match": match.group(),
                "position": match.start(),
            })
    return findings


def detect_commands(text: str) -> list:
    """Detect embedded command patterns."""
    findings = []
    for pattern in COMMAND_PATTERNS:
        matches = re.finditer(pattern, text)
        for match in matches:
            findings.append({
                "type": "command",
                "match": match.group(),
                "position": match.start(),
            })
    return findings


def detect_financial_data(text: str) -> list:
    """Detect potential financial data."""
    findings = []
    for pattern in FINANCIAL_PATTERNS:
        matches = re.finditer(pattern, text)
        for match in matches:
            findings.append({
                "type": "financial",
                "match": match.group(),
                "position": match.start(),
            })
    return findings


def escape_markdown(text: str) -> str:
    """Escape markdown formatting that could confuse processing."""
    # Escape triple backticks (code blocks)
    text = text.replace("```", "\\`\\`\\`")
    # Escape HTML-like tags that could be interpreted as instructions
    text = re.sub(r'<(/?)(system|admin|prompt|instruction|command)', r'&lt;\1\2', text, flags=re.IGNORECASE)
    return text


def truncate(text: str, max_length: int) -> str:
    """Truncate text to max_length, preserving word boundaries."""
    if len(text) <= max_length:
        return text
    truncated = text[:max_length].rsplit(" ", 1)[0]
    return truncated + f"\n\n[Truncated — original was {len(text)} chars]"


def wrap_trust_boundary(text: str, source: str) -> str:
    """Wrap text in XML trust boundary tags."""
    return f'<external_data source="{source}" trust="untrusted">\n{text}\n</external_data>'


def sanitize_external_text(text: str, source: str = "unknown",
                           config: SanitizeConfig = None) -> dict:
    """
    Full three-layer sanitization pipeline.

    Returns:
        dict with:
            - text: sanitized text
            - warnings: list of security findings
            - truncated: whether text was truncated
    """
    if config is None:
        config = SanitizeConfig()

    warnings = []
    truncated = False

    # Layer 0: Basic cleanup
    text = text.strip()

    # Truncate if needed
    if len(text) > config.max_length:
        text = truncate(text, config.max_length)
        truncated = True

    # Layer 1: Pattern detection
    if config.detect_injections:
        injections = detect_injections(text)
        if injections:
            warnings.extend(injections)
            # Don't strip the text — just flag it. The agent should see it
            # but know it's suspicious.

        commands = detect_commands(text)
        if commands:
            warnings.extend(commands)

        financial = detect_financial_data(text)
        if financial:
            warnings.extend(financial)

    # Layer 2: Markdown escaping
    if config.escape_code_blocks:
        text = escape_markdown(text)

    # Layer 3: Trust boundary
    if config.wrap_trust_boundary:
        text = wrap_trust_boundary(text, source)

    return {
        "text": text,
        "warnings": warnings,
        "truncated": truncated,
        "source": source,
        "warning_count": len(warnings),
    }


def format_warnings(warnings: list) -> str:
    """Format warnings for human reading."""
    if not warnings:
        return ""
    lines = ["⚠️ Security warnings:"]
    for w in warnings:
        lines.append(f"  - [{w['type']}] Found: '{w['match'][:60]}' at position {w.get('position', '?')}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Sanitize external text for the second brain")
    parser.add_argument("--source", default="unknown", help="Data source (teams, outlook, gitlab)")
    parser.add_argument("--file", type=str, help="Read from file instead of stdin")
    parser.add_argument("--no-wrap", action="store_true", help="Skip trust boundary wrapping")
    parser.add_argument("--json", action="store_true", help="JSON output with warnings")
    args = parser.parse_args()

    # Read input
    if args.file:
        text = Path(args.file).read_text()
    else:
        text = sys.stdin.read()

    config = SanitizeConfig(wrap_trust_boundary=not args.no_wrap)
    result = sanitize_external_text(text, source=args.source, config=config)

    if args.json:
        import json
        # Make warnings JSON-serializable
        for w in result["warnings"]:
            if "pattern" in w:
                del w["pattern"]
        print(json.dumps(result, indent=2))
    else:
        print(result["text"])
        warning_text = format_warnings(result["warnings"])
        if warning_text:
            print(f"\n{warning_text}", file=sys.stderr)


if __name__ == "__main__":
    main()
