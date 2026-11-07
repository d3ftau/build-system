# Backlog

Things to do later. Not a plan; strike freely.

## Token-saving setup (ponytail, lean-ctx, batching, shell timeout)
Measured 2026-10-15: usage is dominated by a few huge sessions; earlier compaction is the main lever (see doc). lean-ctx no longer recommended. Earlier: caveman dropped, ponytail installed, lean-ctx rolled back:
v3.11.4 sets itself up during npm install, gates shell commands, blocks Grep/Glob, and
has telemetry on. Shell timeout and batching not started.
Sandbox-tested install recipe (shell compression only, permissions kept):  [backlog/token-saving-setup.md](backlog/token-saving-setup.md)

- A silent app break reaches your phone within a day, not the next time you use it (repo-creeper #118)

- A failure that broke one build warns the next build before it starts (repo-creeper #120)

- Your token spend reports itself weekly instead of waiting for you to audit it (repo-creeper #121)
