# 9front einspielen (Rebase-Ablauf)

Die Branches des Trees (ein Git-Repository mit Worktrees):

| Branch | Worktree | Was |
|---|---|---|
| `front` | (keiner) | Spiegel von github.com/9front/9front, Branch `front`; nur fast-forward |
| `gcc` | `tree-gcc` | 9front mit gcc gebaut; minimale Änderungen gegen `front` |
| `main` | `tree` | nfront: gcc + GPU-Stack + wsys/ui (bis 2026-11-12 `ui`) |
| `nix`, `riscv` | `tree-nix`, `tree-riscv` | Ports auf `gcc` |
| `upstream` | `tree-upstream` | Korrekturen für 9front selbst, je ein Commit auf `origin/front` (`patch-upstream/`) |

Ablauf:

1. `git fetch origin`, `front` fast-forward auf `origin/front`.
2. `gcc` auf `front` rebasen; Manifeste neu erzeugen (Generatoren in
   `scripts/gen`), `tests/static`.
3. `main`, `nix`, `riscv` auf das neue `gcc` rebasen; je Branch Build und
   Tests (`tests/static`, `tests/gpu/run.sh` für `main`).
4. `upstream`: die Patches auf das neue `origin/front` (alle müssen
   anwenden), `patch-upstream/` neu exportieren.
5. `bin/pin` im Distributions-Repo.

Keine Sicherungs-Branches im Repository lassen (sie trugen einmal alte,
GPL-belastete Historie): vor einem Rebase höchstens ein `git bundle`
außerhalb der Repositories.
