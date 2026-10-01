#!/usr/bin/env python3
"""
Microsoft Graph Authentication Module — Shared auth for Teams + Outlook.

Uses Device Code Flow (no client secret needed, public client).
Tokens are cached to disk and refreshed automatically.

Setup (one-time):
1. Register app at https://entra.microsoft.com → App Registrations
2. Enable "Allow public client flows" under Authentication
3. Add delegated permissions: Chat.Read, Calendars.Read, Mail.Read, Mail.ReadWrite, User.Read
4. Set MSFT_CLIENT_ID and MSFT_TENANT_ID in .env
5. Run: python3 microsoft_graph.py auth  (follow the device code prompt)

Usage after setup:
    from microsoft_graph import get_graph_client, api_get
    data = api_get("/me/messages", params={"$top": 10})
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Token cache location
TOKEN_CACHE = Path(__file__).resolve().parent.parent.parent / ".claude" / "data" / "state" / "ms_token_cache.json"

# Required scopes
SCOPES = [
    "Chat.Read",
    "Calendars.Read",
    "Mail.Read",
    "Mail.ReadWrite",
    "User.Read",
]

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def _load_env() -> dict:
    """Load Microsoft config from .env file."""
    config = {}
    env_files = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent.parent.parent / ".env",
        Path.home() / "Documents" / "Personal" / "Second Brain Starter" / ".env",
    ]
    for env_file in env_files:
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    config[key.strip()] = val.strip()
            break
    return config


def get_client_config() -> tuple[str, str]:
    """Get client ID and tenant ID."""
    client_id = os.environ.get("MSFT_CLIENT_ID")
    tenant_id = os.environ.get("MSFT_TENANT_ID")

    if not client_id or not tenant_id:
        env = _load_env()
        client_id = client_id or env.get("MSFT_CLIENT_ID")
        tenant_id = tenant_id or env.get("MSFT_TENANT_ID")

    if not client_id or not tenant_id:
        print("""
Microsoft Graph not configured. To set up:

1. Go to https://entra.microsoft.com → App Registrations → New Registration
2. Name: "Second Brain"
3. Supported account types: "Accounts in this organizational directory only"
4. Redirect URI: leave blank (public client)
5. After creation:
   - Go to Authentication → Enable "Allow public client flows"
   - Go to API Permissions → Add: Chat.Read, Calendars.Read, Mail.Read, Mail.ReadWrite, User.Read
6. Add to your .env file:
   MSFT_CLIENT_ID=<Application (client) ID>
   MSFT_TENANT_ID=<Directory (tenant) ID>
7. Run: python3 microsoft_graph.py auth
""", file=sys.stderr)
        sys.exit(1)

    return client_id, tenant_id


def authenticate():
    """Run device code flow to get initial tokens."""
    try:
        import msal
    except ImportError:
        print("Installing msal...")
        os.system(f"{sys.executable} -m pip install msal msal-extensions --quiet")
        import msal

    client_id, tenant_id = get_client_config()
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    # Set up token cache
    cache = msal.SerializableTokenCache()
    TOKEN_CACHE.parent.mkdir(parents=True, exist_ok=True)
    if TOKEN_CACHE.exists():
        cache.deserialize(TOKEN_CACHE.read_text())

    app = msal.PublicClientApplication(
        client_id,
        authority=authority,
        token_cache=cache,
    )

    # Try silent auth first
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            print("Already authenticated (token refreshed silently)")
            _save_cache(cache)
            return result["access_token"]

    # Device code flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        print(f"Error: {flow.get('error_description', 'Failed to create device flow')}")
        sys.exit(1)

    print(f"\n{flow['message']}\n")
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        _save_cache(cache)
        print(f"✅ Authenticated as {result.get('id_token_claims', {}).get('preferred_username', 'unknown')}")
        return result["access_token"]
    else:
        print(f"Error: {result.get('error_description', 'Authentication failed')}")
        sys.exit(1)


def get_access_token() -> str:
    """Get a valid access token (refresh if needed)."""
    try:
        import msal
    except ImportError:
        print("Error: msal not installed. Run: pip install msal msal-extensions", file=sys.stderr)
        sys.exit(1)

    client_id, tenant_id = get_client_config()
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    cache = msal.SerializableTokenCache()
    if TOKEN_CACHE.exists():
        cache.deserialize(TOKEN_CACHE.read_text())

    app = msal.PublicClientApplication(
        client_id,
        authority=authority,
        token_cache=cache,
    )

    accounts = app.get_accounts()
    if not accounts:
        print("Not authenticated. Run: python3 microsoft_graph.py auth", file=sys.stderr)
        sys.exit(1)

    result = app.acquire_token_silent(SCOPES, account=accounts[0])
    if result and "access_token" in result:
        _save_cache(cache)
        return result["access_token"]

    print("Token expired. Run: python3 microsoft_graph.py auth", file=sys.stderr)
    sys.exit(1)


def _save_cache(cache):
    """Save the MSAL token cache to disk."""
    if cache.has_state_changed:
        TOKEN_CACHE.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_CACHE.write_text(cache.serialize())


def api_get(endpoint: str, params: dict = None) -> dict | list:
    """Make a GET request to Microsoft Graph API."""
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
    from urllib.error import HTTPError

    token = get_access_token()
    url = f"{GRAPH_BASE}{endpoint}"
    if params:
        url += "?" + urlencode(params)

    req = Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })

    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get("value", data)
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"Graph API error {e.code}: {body[:200]}", file=sys.stderr)
        return []


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Microsoft Graph authentication")
    parser.add_argument("command", choices=["auth", "test", "status"],
                        help="auth=authenticate, test=test connection, status=check token")
    args = parser.parse_args()

    if args.command == "auth":
        authenticate()
    elif args.command == "test":
        token = get_access_token()
        me = api_get("/me")
        print(f"Connected as: {me.get('displayName', '?')} ({me.get('mail', '?')})")
    elif args.command == "status":
        if TOKEN_CACHE.exists():
            stat = TOKEN_CACHE.stat()
            mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            print(f"Token cache exists (last modified: {mod_time})")
            print(f"Location: {TOKEN_CACHE}")
        else:
            print("No token cache found. Run: python3 microsoft_graph.py auth")


if __name__ == "__main__":
    main()
