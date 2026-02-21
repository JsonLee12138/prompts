---
name: solo-ops
description: >
  AI team role manager for multi-agent development workflows.
  Use when the user wants to create/delete team roles, open role sessions in WezTerm tabs,
  assign tasks to roles, check team status, or merge role branches.
  Triggers on /solo-ops commands, "create a team role", "open role session",
  "assign task to role", "show team status", "merge role branch".
---

# solo-ops

Manages AI team roles using git worktrees + WezTerm tabs. Each role runs in its own isolated worktree (branch `team/<name>`) and opens as a full-permission AI session in a new WezTerm tab.

For directory layout, task format, and bidirectional communication details, see [references/details.md](references/details.md).

## Usage

The skill base directory is shown at the top when this skill loads. Run directly with:

```bash
python3 <base-dir>/scripts/solo_ops.py <command>
```

Use tmux backend directly with:

```bash
python3 <base-dir>/scripts/solo_ops_tmux.py <command>
```

## Commands

Always run from within the project git repository.

### Create a role
```bash
python3 <base-dir>/scripts/solo_ops.py create <name>
```
Creates `team/<name>` git branch + worktree at `.worktrees/<name>/`. Generates:
- `agents/teams/<name>/config.yaml` — provider, description, pane tracking
- `agents/teams/<name>/prompt.md` — role system prompt (edit this to define the role)
- `agents/teams/<name>/tasks/pending/` and `tasks/done/`

After creating, guide the user to edit `prompt.md` to define the role's expertise and behavior.

### Open a role session
```bash
python3 <base-dir>/scripts/solo_ops.py open <name> [claude|codex]
```
- Copies `prompt.md` → `CLAUDE.md` in worktree root (auto-injected as system context)
- Spawns a new WezTerm tab titled `<name>` running `claude --dangerously-skip-permissions` (or `codex --dangerously-bypass-approvals-and-sandbox`)
- Provider priority: argument > `config.yaml default_provider` > claude

tmux variant:
```bash
python3 <base-dir>/scripts/solo_ops_tmux.py open <name> [claude|codex|opencode] [--model <model>]
```

### Open all sessions
```bash
python3 <base-dir>/scripts/solo_ops.py open-all [claude|codex]
```

tmux variant:
```bash
python3 <base-dir>/scripts/solo_ops_tmux.py open-all [claude|codex|opencode] [--model <model>]
```
Opens every role that has a config.yaml.

### Assign a task
```bash
python3 <base-dir>/scripts/solo_ops.py assign <name> "<task description>" [claude|codex]
```
1. Writes `agents/teams/<name>/tasks/pending/<timestamp>-<slug>.md`
2. Auto-opens the role session if not running
3. Sends a notification message to the running session via `wezterm cli send-text`

tmux variant:
```bash
python3 <base-dir>/scripts/solo_ops_tmux.py assign <name> "<task description>" [claude|codex|opencode] [--model <model>]
```

### Reply to a role
```bash
python3 <base-dir>/scripts/solo_ops.py reply <name> "<answer>"
```
Sends a reply to a role's running session. Used when a role has asked a question via `ask claude` and the main controller wants to respond. The message is prefixed with `[Main Controller Reply]` so the role AI can identify it.

tmux variant:
```bash
python3 <base-dir>/scripts/solo_ops_tmux.py reply <name> "<answer>"
```

### Check status
```bash
python3 <base-dir>/scripts/solo_ops.py status
```
Shows all roles, whether their session is running (by pane-id), and pending task count.

### Merge completed work
```bash
python3 <base-dir>/scripts/solo_ops.py merge <name>
```
Merges `team/<name>` into the current branch with `--no-ff`. Run `delete` afterward to clean up.

### Delete a role
```bash
python3 <base-dir>/scripts/solo_ops.py delete <name>
```
Removes the worktree and deletes the `team/<name>` branch.
