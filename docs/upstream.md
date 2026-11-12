# Bringing in 9front (the rebase cycle)

The tree's branches (one git repository with worktrees):

| Branch | Worktree | What |
|---|---|---|
| `front` | (none) | mirror of github.com/9front/9front, branch `front`; fast-forward only |
| `gcc` | `tree-gcc` | 9front built with gcc; minimal changes against `front` |
| `main` | `tree` | nfront: gcc + the GPU stack + wsys/ui (`ui` until 2026-11-12) |
| `nix`, `riscv` | `tree-nix`, `tree-riscv` | ports on `gcc` |
| `upstream` | `tree-upstream` | fixes for 9front itself, one commit each on `origin/front` (`patch-upstream/`) |

Steps:

1. `git fetch origin`, fast-forward `front` to `origin/front`.
2. Rebase `gcc` onto `front`; regenerate the manifests (the generators in
   `scripts/gen`), `tests/static`.
3. Rebase `main`, `nix`, `riscv` onto the new `gcc`; build and test each
   branch (`tests/static`, `tests/gpu/run.sh` for `main`).
4. `upstream`: the patches onto the new `origin/front` (all must apply),
   export `patch-upstream/` again.
5. `bin/pin` in the distribution's repository.

Leave no backup branches in the repository (they once carried old history
with GPL code): before a rebase at most a `git bundle` outside the
repositories.
