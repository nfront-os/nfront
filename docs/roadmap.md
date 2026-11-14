# nfront: the way to a distribution

The starting point was a review of the project. Unlike its recommendation
(an overlay on 9front, merging upstream as an option), nfront is a
**distribution of its own** (decided 2026-11-12): its own name, its own
replica and ISOs. 9front's `front` stays the source, brought in regularly
(`upstream.md`); single fixes still go to 9front as patches
(`patch-upstream/` in the tree).

## State (2026-11-12)

- Parts and paths: `../paths.env`, `../manifest.json`, `../bin/status`;
  `../bin/repos` gets them from GitHub (github.com/nfront-os).
- Licences: no GPL code of Linux in the tree or its git history (the
  LinuxKPI from OpenBSD/FreeBSD templates, `scripts/linux/provenance.py` in
  `tests/static`). Exceptions: Bison parsers (GPL with the Bison
  exception), dual-licensed files (a permissive choice), firmware separate
  under `/lib/firmware`; the CA roots (Mozilla's, MPL-2.0) likewise a separate file,
  from `distfiles.list` onto a CD with Rust or Go as `/sys/lib/tls/ca.pem`. It is a fixed
  state: before each release raise its entry in `distfiles.list` to curl's newest
  `cacert-DATE.pem` (https://curl.se/ca/); installed systems get no update of it
  until there is an update path (replica/pull; there now: `pull(1)`, once
  the update server runs).
- Tests: `tests/static`, `tests/gpu/run.sh` (QEMU, ~140 checks), the
  RX 7600 by VFIO (`amdall.rc`); the laptop (i915) on Linux 7.3 green in its
  runs 9 and 10 (2026-11-11). What ran where: `hardware.md`.

## Progress (2026-11-14)

- Phase 0 reached: `build-toolchains` from scratch; the four profiles' CDs
  from one pinned state, each `iso` 7/7; the suites green but for two old
  gaps (386: APE shared memory cannot grow; arm64: no segment(3) in the
  kernel; `tree/MEMORY.md`). The userland builds with `-O2` (Rust thin LTO,
  Go `-s -w`). The release step (tag 0.1-preview) waits for the user.
- Phase 1: wsys is the desktop of the profiles `ui` and `full`
  (`desktop=rio` chooses rio); the hardware matrix is `hardware.md`.
  Updates over HTTP (the user's choice): `pull(1)` runs replica/pull through
  `replica/httpfs`, which serves the server's tree from a signed index
  (RSA, SHA-256 per file; webfs checks no TLS certificate, so the signature
  carries the trust); `tree/scripts/replica/publish.py` publishes a CD's tree
  (every `mkcd`: into `cache/replica/current/NAME.ARCH`, channel `current`,
  signed with `~/.config/nfront/replica.pem`), and the CD installs the client
  up to date. On gefs `pull` snapshots `main` first, the way back; on hjfs
  what it replaces is gone. `tests/replica` covers it. The server does not
  exist yet: the CDs ask a placeholder, `https://nfront-os.github.io/replica`
  (GitHub, likely). For GitHub: files over 100 MB are refused there (the
  `full` profile's rustc, rustdoc, clippy-driver are 147-161 MB stripped),
  objects would need splitting, or another host. Open as well: the
  reference workflow as one test, a file manager.

## Phase 0: reference build (weeks)

Goal: a reproducible build, an ISO, a green test suite.

- `bin/build-all`: toolchains (only when their commit changes) → tree
  (`build.exe -D` per arch) → ISO (`scripts/guest/mkiso.sh` with Rust and Go).
- Done: the move to `~/Devel/nfront/` (umbrella; only `paths.env` changed);
  `distfiles/` with checksums and `bin/fetch`; the toolchains from release
  archives (`fetch.sh`).
- ISO amd64 with `desktop=wsys`; VESA, virtio-gpu, amdgpu, i915.
- Result: **0.1-preview**, internal.

## Phase 1: daily driver (months)

Goal: a working day on the desktop.

- wsys as the default; term, the ui programs, wbar, a theme.
- draw(3), Wayland (foot) and Vulkan programs in daily use.
- Replica + `pull` with a way back; channel `current` (done but for the
  server's place and key, 2026-11-14).
- Reference workflow without a browser: term, an editor (acme/sam), a file
  manager, a ui client, a draw(3) program, a Wayland program, 9P over the
  network.
- Result: **0.9-beta**, public, with a hardware matrix.

## Phase 2: stable

Goal: **1.0** with a frozen public API.

- ui(4), uiview, libui, uigo, p9win frozen; versions.
- A rebase cycle for Linux (DRM), Mesa, Rust, Go, gcc, wgpu/winit
  (`patches.md`).
- The security model of wsys/ui (file permissions, namespaces, buffer
  ownership).
- Signed ISOs, an SBOM (from `manifest.json` and the distfiles), channel
  `release`.

## Phase 3: platform

arm64 GPU, riscv64 (Rust target, drivers), more drivers; programs beside
it as packages (GPL allowed there, not in the tree).

## The five 1.0 criteria

1. A working day on the laptop without a crash (term, ui, draw(3),
   Wayland, Vulkan, network).
2. A reproducible build, byte-identical on two machines, with the Rust
   bootstrap.
3. `pull` updates and rolls back (or documents what is lost).
4. The public API frozen, with manual pages and examples.
5. A published hardware matrix (tested/works/untested; VESA as the
   guarantee).
