#!/bin/bash
# ============================================================================
# Second Brain — Health Check
# ============================================================================
# Checks the status of all components: plists, tokens, vault, scripts.
#
# Usage:
#   chmod +x deploy/status.sh
#   ./deploy/status.sh
# ============================================================================

set -uo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PROJECT_DIR="/Users/frank.enendu/Documents/Personal/Second Brain Starter"
LOG_DIR="$PROJECT_DIR/.claude/data/logs"

echo "================================================"
echo "  Second Brain — Health Check"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "================================================"
echo ""

# ---- Project Structure ----
echo -e "${BLUE}[Project Structure]${NC}"
DIRS=(
    "vault" "vault/daily" "vault/projects" "vault/meetings" "vault/drafts/active"
    "vault/sources" "vault/team" "vault/portfolio"
    ".claude/hooks" ".claude/scripts" ".claude/scripts/integrations"
    ".claude/skills" ".claude/data/state"
)
for dir in "${DIRS[@]}"; do
    if [ -d "$PROJECT_DIR/$dir" ]; then
        echo -e "${GREEN}  ✓ $dir/${NC}"
    else
        echo -e "${RED}  ✗ $dir/ — MISSING${NC}"
    fi
done

# ---- Core Files ----
echo ""
echo -e "${BLUE}[Core Files]${NC}"
FILES=(
    "vault/SOUL.md" "vault/USER.md" "vault/MEMORY.md" "vault/HEARTBEAT.md" "vault/HABITS.md"
    ".claude/settings.json" ".env" ".gitignore"
)
for f in "${FILES[@]}"; do
    if [ -f "$PROJECT_DIR/$f" ]; then
        lines=$(wc -l < "$PROJECT_DIR/$f" 2>/dev/null | tr -d ' ')
        echo -e "${GREEN}  ✓ $f ($lines lines)${NC}"
    else
        echo -e "${RED}  ✗ $f — MISSING${NC}"
    fi
done

# ---- Hooks ----
echo ""
echo -e "${BLUE}[Hooks]${NC}"
HOOKS=(
    "session-start-context.py"
    "pre-compact-flush.py"
    "session-end-flush.py"
    "pre-tool-guardrail.py"
)
for hook in "${HOOKS[@]}"; do
    if [ -f "$PROJECT_DIR/.claude/hooks/$hook" ]; then
        echo -e "${GREEN}  ✓ $hook${NC}"
    else
        echo -e "${RED}  ✗ $hook — MISSING${NC}"
    fi
done

# ---- Scripts ----
echo ""
echo -e "${BLUE}[Scripts]${NC}"
SCRIPTS=(
    "db.py" "embeddings.py" "memory_index.py" "memory_search.py"
    "heartbeat.py" "memory_reflect.py" "draft_manager.py"
    "sanitize.py" "guardrails.py"
)
for script in "${SCRIPTS[@]}"; do
    if [ -f "$PROJECT_DIR/.claude/scripts/$script" ]; then
        echo -e "${GREEN}  ✓ $script${NC}"
    else
        echo -e "${RED}  ✗ $script — MISSING${NC}"
    fi
done

# ---- Integrations ----
echo ""
echo -e "${BLUE}[Integrations]${NC}"
INTEGRATIONS=(
    "gitlab_integration.py" "microsoft_graph.py" "teams.py" "outlook.py" "query.py"
)
for script in "${INTEGRATIONS[@]}"; do
    if [ -f "$PROJECT_DIR/.claude/scripts/integrations/$script" ]; then
        echo -e "${GREEN}  ✓ $script${NC}"
    else
        echo -e "${RED}  ✗ $script — MISSING${NC}"
    fi
done

# ---- Skills ----
echo ""
echo -e "${BLUE}[Skills]${NC}"
SKILLS_DIR="$PROJECT_DIR/.claude/skills"
if [ -d "$SKILLS_DIR" ]; then
    skill_count=$(find "$SKILLS_DIR" -name "SKILL.md" | wc -l | tr -d ' ')
    echo -e "${GREEN}  $skill_count skills installed:${NC}"
    for skill_dir in "$SKILLS_DIR"/*/; do
        skill_name=$(basename "$skill_dir")
        if [ -f "$skill_dir/SKILL.md" ]; then
            echo -e "${GREEN}    ✓ $skill_name${NC}"
        fi
    done
fi

# ---- Authentication ----
echo ""
echo -e "${BLUE}[Authentication]${NC}"

# GitLab
if grep -q "GITLAB_PAT=" "$PROJECT_DIR/.env" 2>/dev/null; then
    echo -e "${GREEN}  ✓ GitLab PAT configured${NC}"
else
    echo -e "${RED}  ✗ GitLab PAT not in .env${NC}"
fi

# MS Graph
MS_CACHE="$PROJECT_DIR/.claude/data/state/ms_token_cache.json"
if [ -f "$MS_CACHE" ]; then
    cache_age=$(( ($(date +%s) - $(stat -f %m "$MS_CACHE" 2>/dev/null || echo 0)) / 86400 ))
    if [ "$cache_age" -lt 7 ]; then
        echo -e "${GREEN}  ✓ MS Graph token cache (${cache_age}d old)${NC}"
    else
        echo -e "${YELLOW}  ⚠ MS Graph token cache is ${cache_age}d old — may need refresh${NC}"
    fi
else
    echo -e "${YELLOW}  ⚠ MS Graph not authenticated${NC}"
fi

# Anthropic
if [ -n "${ANTHROPIC_API_KEY:-}" ] || grep -q "ANTHROPIC_API_KEY=" "$PROJECT_DIR/.env" 2>/dev/null; then
    echo -e "${GREEN}  ✓ Anthropic API key configured${NC}"
else
    echo -e "${YELLOW}  ⚠ ANTHROPIC_API_KEY not set${NC}"
fi

# ---- Database ----
echo ""
echo -e "${BLUE}[Memory Database]${NC}"
DB_PATHS=(
    "$PROJECT_DIR/.claude/data/memory.db"
    "$HOME/.second-brain/memory.db"
)
for db in "${DB_PATHS[@]}"; do
    if [ -f "$db" ]; then
        db_size=$(du -h "$db" 2>/dev/null | cut -f1)
        echo -e "${GREEN}  ✓ $db ($db_size)${NC}"
    fi
done

# ---- Heartbeat State ----
echo ""
echo -e "${BLUE}[Heartbeat State]${NC}"
HB_STATE="$PROJECT_DIR/.claude/data/state/heartbeat-state.json"
if [ -f "$HB_STATE" ]; then
    last_run=$(python3 -c "import json; d=json.load(open('$HB_STATE')); print(d.get('last_run','unknown'))" 2>/dev/null || echo "unknown")
    echo -e "${GREEN}  Last heartbeat: $last_run${NC}"
else
    echo -e "${YELLOW}  ⚠ No heartbeat state — hasn't run yet${NC}"
fi

# ---- Launchd Plists ----
echo ""
echo -e "${BLUE}[LaunchD Plists]${NC}"
PLISTS=(
    "com.secondbrain.heartbeat"
    "com.secondbrain.reflect"
    "com.secondbrain.index"
    "com.secondbrain.morning-brief"
)
for plist in "${PLISTS[@]}"; do
    if launchctl list "$plist" &>/dev/null; then
        echo -e "${GREEN}  ✓ $plist — loaded${NC}"
    elif [ -f "$HOME/Library/LaunchAgents/$plist.plist" ]; then
        echo -e "${YELLOW}  ⚠ $plist — installed but not loaded${NC}"
    else
        echo -e "${YELLOW}  ○ $plist — not installed (using Cowork scheduled tasks instead)${NC}"
    fi
done

# ---- Cowork Scheduled Tasks ----
echo ""
echo -e "${BLUE}[Cowork Scheduled Tasks]${NC}"
echo "  (Managed in Cowork app — 7 tasks configured)"
echo "  daily-briefing, end-of-day-wrapup, pipeline-mr-monitor,"
echo "  weekly-retro, deadline-warning, project-health-check, ai-news-briefing"

# ---- Vault Statistics ----
echo ""
echo -e "${BLUE}[Vault Statistics]${NC}"
if [ -d "$PROJECT_DIR/vault" ]; then
    total_files=$(find "$PROJECT_DIR/vault" -name "*.md" | wc -l | tr -d ' ')
    daily_logs=$(find "$PROJECT_DIR/vault/daily" -name "*.md" -not -name "ai-news-*" 2>/dev/null | wc -l | tr -d ' ')
    ai_news=$(find "$PROJECT_DIR/vault/daily" -name "ai-news-*" 2>/dev/null | wc -l | tr -d ' ')
    projects=$(find "$PROJECT_DIR/vault/projects" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    meetings=$(find "$PROJECT_DIR/vault/meetings" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    drafts_active=$(find "$PROJECT_DIR/vault/drafts/active" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    drafts_sent=$(find "$PROJECT_DIR/vault/drafts/sent" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

    echo "  Total markdown files: $total_files"
    echo "  Daily logs: $daily_logs"
    echo "  AI news briefings: $ai_news"
    echo "  Project files: $projects"
    echo "  Meeting notes: $meetings"
    echo "  Active drafts: $drafts_active"
    echo "  Sent drafts (voice library): $drafts_sent"
fi

# ---- Summary ----
echo ""
echo "================================================"
echo "  Health check complete"
echo "================================================"
