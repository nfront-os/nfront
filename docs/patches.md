# What nfront changes in other projects' sources (as of 2026-11-12)

Every change to a template is kept as a patch series beside it, so that an
update is a rebase of that series.

| Part | Template | Patches | Where |
|---|---|---|---|
| 9front | github.com/9front/9front `front` | 27 fixes for 9front itself | tree `patch-upstream/` (its README: the status of each patch) |
| 9front, the port | `front` | branch `gcc` (minimal changes, each marked `/* GCC port */`), branch `main` | tree |
| Mesa | 26.2.4 | 42 | tree `sys/src/mesa/patches`, `scripts/mesa/patches.sh` |
| Linux DRM | 7.3.1 (MIT files only, `vendor/`) | none; own versions in `replace/`, the LinuxKPI in `kpi/` (templates OpenBSD a9becb03c, FreeBSD 584f44221f45, drm-kmod drm_v6.14) | tree `sys/src/linux` (NOTICE, REJECTED, PROVENANCE) |
| gcc, binutils | gcc 16.2.0, binutils 2.47 | `gcc.patch`, `binutils.patch` | `toolchain/gcc/patches` |
| Rust | the nightly source archive (rust with cargo, backtrace, llvm-project; branch `plan9`), libc's crate, crates | rust 25, libc 7, llvm-project 1, cargo 3, backtrace 1, crates 43 | `toolchain/rust/patches` |
| Go | go1.27.3 (branch `plan9`) | 6 | `toolchain/go/patches` |
| Libraries for APE | expat, freetype, fontconfig, pixman, fcft, tllist, foot, xkbcommon, wayland, SDL3, GLFW, libffi | overlays/`plan9/` files per library | tree `sys/src/<lib>` (VERSION or VENDOR.json, archives in DISTFILES) |
| plan9port | 9fans/plan9port | none (used unchanged, `tools/plan9port`) | — |

Open: a rebase cycle per part (phase 2 of the roadmap), upstream
submissions where possible.
