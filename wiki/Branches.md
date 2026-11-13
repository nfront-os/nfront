# Branches

## tree (9front)

```
origin/front ── front ── gcc ──┬── main       nfront: GPU stack, wsys, ui
                               ├── nix        NIX: application cores
                               └── riscv      riscv64 port
origin/front ── upstream                      fixes for 9front itself
```

| Branch | Worktree, if any | What | Rule |
|---|---|---|---|
| `front` | — | mirror of 9front's `front` | fast-forward only |
| `gcc` | (`tree-gcc`) | 9front built with gcc | minimal diff to `front`; each change marked `/* GCC port: why */` |
| `main` | `tree` | the distribution | 9front code may change where nfront needs it |
| `nix` | (`tree-nix`) | NIX (AC/TC cores) on `gcc` | |
| `riscv` | (`tree-riscv`) | riscv64 kernel and userland on `gcc` | |
| `upstream` | (`tree-upstream`) | one commit per fix, on `origin/front`; exported to `patch-upstream/` | must apply to 9front as is |

Bringing in 9front (details: `dist/docs/upstream.md`):

```sh
cd tree
git fetch origin front:front                  # fast-forward only
git worktree add ../tree-gcc gcc              # gcc has no worktree: one for the while
(cd ../tree-gcc && git rebase front)          # regenerate manifests, tests/static
git worktree remove ../tree-gcc
git rebase gcc                                # main, here: build, tests/static, tests/gpu
```

Work happens on `main`, in `tree`. The other branches are refs in the same
repository; a worktree beside `tree` (`tree-gcc`, …) is made only to work on
one of them (`dist/bin/repos --worktrees=gcc,riscv`). Never switch `tree` to
another branch: its working tree holds `main`'s build.

## Toolchains and tools

| Repository | Branch | Port lives on |
|---|---|---|
| `toolchain/gcc` | `main` | the repository itself |
| `toolchain/rust` | `main` | `rust/` (with cargo, backtrace, llvm-project inside), `libc/`: branch `plan9` |
| `toolchain/go` | `main` | `go/`: branch `plan9` |
| `tools/mcp` | `main` | — |
| `dist` | `main` | — |
