# CLAUDE.md — nfront

nfront (working name) is a distribution built on 9front: the 9front tree
built with gcc, the GPU stack (gpu(4), the LinuxKPI with Linux's DRM
drivers, Mesa), the window system wsys and the ui framework, and the
toolchains gcc, Rust and Go for it. This directory holds all of its parts;
it is not a git repository itself, each part is one.

## Layout

| Path | What | Git |
|---|---|---|
| `tree/` | the 9front tree, branch `main` (was `ui`); see `tree/CLAUDE.md` | yes; worktrees below |
| `tree-gcc/`, `tree-nix/`, `tree-riscv/`, `tree-upstream/` | worktrees of `tree`: branches `gcc` (the gcc port), `nix`, `riscv`, `upstream` (fixes for 9front itself) | worktrees |
| `toolchain/gcc/` | gcc 16 and binutils for 9front, cross and native (branch `main`) | yes |
| `toolchain/rust/` | Rust for 9front; `rust/`, `libc/`, `llvm-project/` are repositories of their own | yes |
| `toolchain/go/` | Go for 9front; `go/` is a repository of its own | yes |
| `tools/mcp/` | MCP server: an agent on Linux works on a 9front guest | yes |
| `tools/plan9port/` | Plan 9 from User Space (`PLAN9PORT`: rc, yacc, the host build's generators); 9fans' repository, unchanged, built by its `./INSTALL` | yes (9fans') |
| `distfiles/` | the releases' archives other projects' sources come from | no (data) |
| `dist/` | the distribution: `paths.env`, `manifest.json`, `bin/`, `docs/` | yes |

Outside, on purpose: `~/Devel/nfront-attic` (the plans and chats, downloads
with GPL sources, a bundle of the old git history with GPL code). Never move them into nfront, never put
the attic into git: a copy of nfront must carry no GPL material.

## Paths

- `dist/paths.env` is the only place with paths (relative to this
  directory; things outside it as `../linux-7.3.1`, ...).
  After moving anything, change only this file.
- Scripts read it: in the tree `scripts/lib/paths.sh` (after `ROOT=`) and
  `scripts/lib/paths.py` (`paths.get('GCC_DIR')`, `paths.archive()` for
  `$DISTFILES/x`); in each toolchain `scripts/nfront-paths.sh` (after
  `TOP=`). Never write a sibling path (`../9front-gcc`, `~/Devel/...`) into a
  script.
- `~/Devel/9front*` are symlinks of the old layout, kept until the
  toolchains are rebuilt from here; then they go.

## Tools (dist/bin)

- `status`: each part (branch, commit) against `manifest.json`, changed files.
- `pin [-f]`: `manifest.json` from the parts' heads, after commits.
- `fetch [-n]`: the archives of `distfiles.list` into `distfiles/`, checked by sha256.
- `build-all [-iso] [ARCH...]`: checks the toolchains, builds the tree
  (`build.exe -D` per arch), optionally the amd64 CD with Rust and Go.

Docs: `dist/docs/roadmap.md` (phases, 1.0 criteria), `upstream.md` (bringing
in 9front: front → gcc → main), `patches.md`; the plans (German) are kept
outside git in `~/Devel/nfront-attic/dist-docs`.
Logs of the work: `tree/MEMORY.md` (German, stays so: every branch edits it, a translation would conflict in each rebase), `toolchain/*/NOTES.md` (English).

## Rules

- Licences: in the tree only permissive code (MIT, BSD, ISC, zlib, public
  domain); firmware as separate files. The LinuxKPI holds no GPL text of
  Linux: `tree/scripts/linux/provenance.py --check` (in `tests/static`;
  needs `LINUX`, `LINUX_OLD` of paths.env). Own versions of GPL files are
  written by hand from usage, never generated from the original; copied code
  keeps its notices. Exceptions the user accepted: Bison-generated parsers,
  dual-licensed files (a permissive choice).
- Git: commit only your own files (`git add <files>`, not `-A` in a tree with
  build output); never commit build files (`.o`, `.d`, logs). Other agents
  may have uncommitted work in a part (`toolchain/rust`: crate patches):
  leave it alone. No backup branches in the repositories: a `git bundle`
  outside nfront instead. History rewrites only with the user's word and
  `filter-repo --refs` limited to the range concerned.
- Builds: never two builds in one tree at once (`build-all` locks). After
  changes: `tree/tests/static/run.sh`, the build, and for the GPU stack
  `tree/tests/gpu/run.sh` (QEMU, ~140 checks).
- Guests: one at a time (they share `~/.cache/9front-cli`); no side load
  while a test suite boots guests. The RX 7600 by VFIO only when the user has
  bound it (`sudo tree/scripts/guest/vfio-gpu.sh bind <pid of the long-lived
  parent>`); no guest while binding or releasing.
- Documentation only in English: `dist/docs`, the wiki, READMEs, NOTES.md, comments. Exception: the tree's `MEMORY.md` stays German.
- Fix causes, not symptoms; close open ends (hangs, unrun tests) before new work.
