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
  manifest from the parts' heads)
- `docs/`: `roadmap.md`, `upstream.md` (bringing in 9front), `patches.md`, the plans (`plans/ui`, `plans/gpu`), `review/`

The parts (now beside this repository in ~/Devel, later in ~/Devel/nfront):

| part | what |
|---|---|
| `9front` | the tree (branch `ui`); worktrees `9front-gccwt` (gcc), `9front-nix`, `9front-riscv`, `9front-upstream` |
| `9front-gcc` | gcc 16 and binutils for 9front (cross and native) |
| `9front-rust` | Rust for 9front |
| `9front-go` | Go for 9front |
| `9front-mcp` | MCP server: an agent on Linux works on 9front |
| `9front-ui/src` | the releases' archives other projects' sources come from (DISTFILES) |
