# Was nfront an fremden Quellen ändert (Stand 2026-11-12)

Jede Änderung an einer Vorlage steht als Patch-Reihe neben ihr, damit ein
Update ein Rebase dieser Reihe ist.

| Teil | Vorlage | Patches | Wo |
|---|---|---|---|
| 9front | github.com/9front/9front `front` | 27 Korrekturen für 9front selbst | Tree `patch-upstream/` (README dort: Status je Patch) |
| 9front, Port | `front` | Branch `gcc` (minimale Änderungen, je mit `/* GCC port */`), Branch `ui` | Tree |
| Mesa | 26.2.4 | 42 | Tree `sys/src/mesa/patches`, `scripts/mesa/patches.sh` |
| Linux DRM | 7.3.1 (nur MIT-Dateien, `vendor/`) | keine; eigene Fassungen in `replace/`, LinuxKPI in `kpi/` (Vorlagen OpenBSD a9becb03c, FreeBSD 584f44221f45, drm-kmod drm_v6.14) | Tree `sys/src/linux` (NOTICE, REJECTED, PROVENANCE) |
| gcc, binutils | gcc 16.2.0, binutils 2.47 | `gcc.patch`, `binutils.patch` | `9front-gcc/patches` |
| Rust | rust, libc, llvm-project (Branch `plan9`), Crates | rust 26, libc 7, llvm-project 1, cargo 3, backtrace 1, Crates 43 | `9front-rust/patches` |
| Go | go1.27.3 (Branch `plan9`) | 6 | `9front-go/patches` |
| Bibliotheken für APE | expat, freetype, fontconfig, pixman, fcft, tllist, foot, xkbcommon, wayland, SDL3, GLFW, libffi | Overlays/`plan9/`-Dateien je Bibliothek | Tree `sys/src/<lib>` (VERSION bzw. VENDOR.json, Archive in DISTFILES) |

Offen: ein Rebase-Zyklus je Teil (Phase 2 der Roadmap), Upstream-Anträge
wo möglich.
