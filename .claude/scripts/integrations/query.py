#!/usr/bin/env python3
"""
Unified Query CLI — Single entry point for all platform integrations.

Usage:
    python3 query.py gitlab mrs|issues|pipelines|activity|summary
    python3 query.py teams messages|calendar|dms|summary
    python3 query.py outlook inbox|unread|summary
    python3 query.py all                    # Full cross-platform summary
"""

import sys
from pathlib import Path

# Ensure integrations dir is on path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    platform = sys.argv[1].lower()

    if platform == "gitlab":
        from gitlab_integration import main as gitlab_main
        sys.argv = sys.argv[1:]  # Shift args
        gitlab_main()

    elif platform == "teams":
        from teams import main as teams_main
        sys.argv = sys.argv[1:]
        teams_main()

    elif platform == "outlook":
        from outlook import main as outlook_main
        sys.argv = sys.argv[1:]
        outlook_main()

    elif platform == "all":
        from datetime import datetime
        print(f"# Cross-Platform Summary — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

        # GitLab always works (PAT auth)
        try:
            from gitlab_integration import get_full_summary
            print(get_full_summary())
            print()
        except Exception as e:
            print(f"GitLab: Error - {e}\n")

        # Teams/Outlook need MS Graph auth
        try:
            from teams import get_full_summary as teams_summary
            print(teams_summary())
            print()
        except SystemExit:
            print("Teams: Not configured (run: python3 microsoft_graph.py auth)\n")
        except Exception as e:
            print(f"Teams: Error - {e}\n")

        try:
            from outlook import get_full_summary as outlook_summary
            print(outlook_summary())
        except SystemExit:
            print("Outlook: Not configured (run: python3 microsoft_graph.py auth)\n")
        except Exception as e:
            print(f"Outlook: Error - {e}\n")

    else:
        print(f"Unknown platform: {platform}")
        print("Available: gitlab, teams, outlook, all")
        sys.exit(1)


if __name__ == "__main__":
    main()
