#!/bin/bash
# ============================================================================
# Second Brain — Local Deployment Installer
# ============================================================================
# Installs launchd plists for automated tasks on macOS.
# Run once after setting up the project.
#
# Usage:
#   chmod +x deploy/install.sh
#   ./deploy/install.sh
#
# What it does:
#   1. Validates Python dependencies are installed
#   2. Validates auth tokens are configured (.env, MS Graph)
#   3. Copies launchd plists to ~/Library/LaunchAgents/
#   4. Loads them into launchd
#   5. Runs a health check
# ============================================================================

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_DIR="/Users/frank.enendu/Documents/Personal/Second Brain Starter"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
LOG_DIR="$PROJECT_DIR/.claude/data/logs"

echo "================================================"
echo "  Second Brain — Local Deployment Installer"
echo "================================================"
echo ""

# ---- Step 1: Check project directory ----
echo -e "${YELLOW}[1/5] Checking project directory...${NC}"
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}ERROR: Project directory not found at $PROJECT_DIR${NC}"
    exit 1
fi
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "${RED}ERROR: .env file not found. Create it with GITLAB_PAT and other tokens.${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Project directory exists${NC}"
echo -e "${GREEN}  ✓ .env file found${NC}"

# ---- Step 2: Check Python dependencies ----
echo ""
echo -e "${YELLOW}[2/5] Checking Python dependencies...${NC}"

check_python_module() {
    if python3 -c "import $1" 2>/dev/null; then
        echo -e "${GREEN}  ✓ $1${NC}"
        return 0
    else
        echo -e "${RED}  ✗ $1 — install with: pip install $2${NC}"
        return 1
    fi
}

DEPS_OK=true
check_python_module "fastembed" "fastembed" || DEPS_OK=false
check_python_module "msal" "msal" || DEPS_OK=false
check_python_module "sqlite_vec" "sqlite-vec" || DEPS_OK=false

if [ "$DEPS_OK" = false ]; then
    echo ""
    echo -e "${YELLOW}Install missing dependencies with:${NC}"
    echo "  pip install -r $PROJECT_DIR/requirements.txt --break-system-packages"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# ---- Step 3: Check auth tokens ----
echo ""
echo -e "${YELLOW}[3/5] Checking authentication...${NC}"

# Check GitLab PAT
if grep -q "GITLAB_PAT=" "$PROJECT_DIR/.env" 2>/dev/null; then
    echo -e "${GREEN}  ✓ GitLab PAT configured${NC}"
else
    echo -e "${YELLOW}  ⚠ GitLab PAT not found in .env — GitLab integrations will fail${NC}"
fi

# Check MS Graph token cache
MS_TOKEN_CACHE="$PROJECT_DIR/.claude/data/state/ms_token_cache.json"
if [ -f "$MS_TOKEN_CACHE" ]; then
    echo -e "${GREEN}  ✓ Microsoft Graph token cache exists${NC}"
else
    echo -e "${YELLOW}  ⚠ MS Graph not authenticated — run: python3 .claude/scripts/integrations/microsoft_graph.py auth${NC}"
fi

# Check Anthropic API key (for future Claude Agent SDK use)
if [ -n "${ANTHROPIC_API_KEY:-}" ] || grep -q "ANTHROPIC_API_KEY=" "$PROJECT_DIR/.env" 2>/dev/null; then
    echo -e "${GREEN}  ✓ Anthropic API key configured${NC}"
else
    echo -e "${YELLOW}  ⚠ ANTHROPIC_API_KEY not set — Claude Agent SDK calls will fail${NC}"
fi

# ---- Step 4: Create log directory ----
echo ""
echo -e "${YELLOW}[4/5] Setting up directories...${NC}"
mkdir -p "$LOG_DIR"
mkdir -p "$PROJECT_DIR/.claude/data/state"
mkdir -p "$PROJECT_DIR/vault/daily"
mkdir -p "$PROJECT_DIR/vault/drafts/active"
mkdir -p "$PROJECT_DIR/vault/drafts/sent"
mkdir -p "$PROJECT_DIR/vault/drafts/expired"
mkdir -p "$PROJECT_DIR/vault/sources/articles"
mkdir -p "$PROJECT_DIR/vault/sources/screenshots"
mkdir -p "$PROJECT_DIR/vault/sources/data"
echo -e "${GREEN}  ✓ All directories created${NC}"

# ---- Step 5: Install launchd plists ----
echo ""
echo -e "${YELLOW}[5/5] Installing launchd plists...${NC}"
mkdir -p "$LAUNCH_AGENTS"

PLISTS=(
    "com.secondbrain.heartbeat.plist"
    "com.secondbrain.reflect.plist"
    "com.secondbrain.index.plist"
    "com.secondbrain.morning-brief.plist"
)

for plist in "${PLISTS[@]}"; do
    src="$PROJECT_DIR/deploy/$plist"
    dest="$LAUNCH_AGENTS/$plist"

    if [ -f "$src" ]; then
        # Unload if already loaded
        launchctl unload "$dest" 2>/dev/null || true

        # Copy and load
        cp "$src" "$dest"
        launchctl load "$dest"
        echo -e "${GREEN}  ✓ Installed and loaded $plist${NC}"
    else
        echo -e "${YELLOW}  ⚠ $plist not found in deploy/ — skipping${NC}"
    fi
done

# ---- Done ----
echo ""
echo "================================================"
echo -e "${GREEN}  Installation complete!${NC}"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Run ./deploy/status.sh to verify everything is healthy"
echo "  2. Check logs at: $LOG_DIR/"
echo "  3. The heartbeat runs every 30 min (9 AM - 7 PM)"
echo "  4. Daily reflection runs at 8 AM"
echo "  5. Memory re-index runs every 2 hours"
echo "  6. Morning brief posts to Teams the first weekday tick after 06:30 with VPN up"
echo ""
echo "Cowork scheduled tasks (7 tasks) are managed separately in the Cowork app."
echo "The launchd plists handle the local-only automation (heartbeat, reflect, index)."
