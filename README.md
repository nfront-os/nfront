# nfront

Working name of a distribution built on 9front: the gcc-built tree with
the GPU stack (gpu(4), the LinuxKPI with Linux's DRM drivers, Mesa), the
window system wsys and the ui framework, and the toolchains gcc, Rust and
Go for it.  This repository holds what ties the parts together:

- `paths.env`: where each part is (the only place with paths; the
  scripts of the tree and the toolchains read it)
- `manifest.json`: the parts, their branches and the commits that belong
  together
- `bin/`: `status` (each part against the manifest), `pin` (the
  manifest from the parts' heads), `fetch` (the archives of
  `distfiles.list` into DISTFILES, checked by sha256)
- `docs/`: `roadmap.md`, `upstream.md` (bringing in 9front), `patches.md`, the plans (`plans/ui`, `plans/gpu`), `review/`

The parts (in ~/Devel/nfront, beside this repository, `dist/`):

| part | what |
|---|---|
| `tree` | the 9front tree (branch `main`); worktrees `tree-gcc` (gcc), `tree-nix`, `tree-riscv`, `tree-upstream` |
| `toolchain/gcc` | gcc 16 and binutils for 9front (cross and native) |
| `toolchain/rust` | Rust for 9front |
| `toolchain/go` | Go for 9front |
| `tools/mcp` | MCP server: an agent on Linux works on 9front |
| `distfiles` | the releases' archives other projects' sources come from (DISTFILES) |
