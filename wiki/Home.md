# nfront

nfront (working name) is a distribution built on [9front](https://9front.org):

- 9front built with **gcc** on Linux (amd64, 386, arm64; riscv64 as a port)
- a **GPU stack**: gpu(4), Linux's DRM drivers on a LinuxKPI, Mesa (Vulkan, OpenGL)
- **wsys**, a GPU-composing window system, and **ui**, a declarative UI framework served as files
- toolchains for 9front: **gcc**, **Rust**, **Go**

All of it lives in one directory, `~/Devel/nfront`; each part is a git repository.

| Page | What |
|---|---|
| [[Repositories]] | the git repositories and what each holds |
| [[Branches]] | branches and how they stack |
| [[Host-requirements]] | what the Linux host needs |
| [[Building]] | from a Linux host to an ISO, step by step |
| [[Using gcc, Rust and Go|Toolchains]] | the toolchains on 9front and from Linux; rebuilding the system with gcc |
| [[Features]] | what works today, and where |

Licences: the 9front tree holds only permissive code (MIT, BSD, ISC, zlib,
public domain); firmware is kept as separate files. A check
(`scripts/linux/provenance.py`, part of `tests/static`) keeps GPL text of
Linux out of the LinuxKPI.
