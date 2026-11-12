# Repositories

Layout of `~/Devel/nfront` (each entry below is a git repository; worktrees
of `tree` are left out, see [[Branches]]):

```
nfront/
├── dist/              the distribution: paths, manifest, tools, docs
├── tree/              the 9front tree
├── toolchain/
│   ├── gcc/           gcc and binutils for 9front
│   ├── rust/          Rust for 9front (+ rust/, libc/, llvm-project/)
│   └── go/            Go for 9front (+ go/)
├── tools/mcp/         MCP server for 9front
└── distfiles/         release archives (not git)
```

| Repository | Holds | Upstream it builds on |
|---|---|---|
| `dist` | `paths.env` (all paths), `manifest.json` (commits that belong together), `bin/` (`status`, `pin`, `fetch`, `build-all`), `docs/` (plans, roadmap), this wiki | — |
| `tree` | 9front with the gcc port, the GPU stack, wsys, ui, tests, build tool (`sys/src/cmd/build`) | github.com/9front/9front |
| `toolchain/gcc` | `build.sh`, `fetch.sh`, `patches/` (gcc.patch, binutils.patch), `plan9/` (gccmk) | gcc 16.2.0, binutils 2.47 |
| `toolchain/rust` | `patches/` (rust, cargo, backtrace, llvm-project, libc, crates), `crates/`, `scripts/`, `tests/` | rust-lang/rust, rust-lang/libc |
| `toolchain/rust/rust`, `libc`, `llvm-project` | the sources; the port on branch `plan9` (made from `patches/` by `scripts/rust-patches.sh apply`) | upstream clones |
| `toolchain/go` | `patches/go`, `scripts/build.sh`, `install.sh`, tests | go1.27.3 |
| `toolchain/go/go` | Go's sources, port on branch `plan9` | go.googlesource.com/go |
| `tools/mcp` | `9front-mcp`: lets an agent on Linux work on a 9front system (read, write, edit, glob, grep, rc) | — |

Outside nfront, referenced by `dist/paths.env`:

| Name | Path | Needed for |
|---|---|---|
| `PLAN9PORT` | `../plan9port` | rc, yacc and generators of the host build |
| `LINUX`, `LINUX_OLD` | `../linux-7.3.1`, `../linux-6.6` | the LinuxKPI's tools and its GPL check |
| `OPENBSD_SRC`, `FREEBSD_SRC`, `DRMKMOD_SRC` | `../openbsd`, `../freebsd-src`, `../drm-kmod` | importing the LinuxKPI's BSD templates |

Show every part against the manifest:

```sh
$ dist/bin/status
tree               main       fc5380bd2c   =
tree-gcc           gcc        b7f15db6a8   =
tree-nix           nix        80de19da42   =
tree-riscv         riscv      4f296917c7   =
tree-upstream      upstream   edaf0ee0e9   =
gcc                main       83a2ebbd7c   =
rust               main       fec0fb3653   +2 32 changed
...
```

`=`: at the pinned commit; `+N`: N commits after it; `dist/bin/pin` pins the current heads.

Paths: never written into scripts. The tree reads them with
`scripts/lib/paths.sh` / `paths.py`, each toolchain with
`scripts/nfront-paths.sh`. Moving a part means editing `dist/paths.env`:

```sh
GCC_DIR=toolchain/gcc
DISTFILES=distfiles
LINUX=../linux-7.3.1
```
