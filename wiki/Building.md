# Building

Everything is built on a Linux host (x86-64) from the repositories of
[nfront-os](https://github.com/nfront-os) and the release archives they name.
The result is the 9front tree for amd64, 386 and arm64 with gcc, Rust and Go
for 9front, and an install CD.

From scratch it is a handful of commands (sections 2–4) and about three hours,
mostly gcc and Rust. Later builds are incremental and take minutes.

| Part | Where | What it is |
|---|---|---|
| plan9port | `tools/plan9port` | rc, yacc and the generators the tree's build runs on Linux |
| tree | `tree` | the 9front tree; `sys/src/cmd/build` (build.exe) builds it |
| gcc | `toolchain/gcc` | gcc 16 and binutils for 9front: the cross compiler (Linux → 9front) and gcc on 9front |
| Rust | `toolchain/rust` | rustc, cargo and std for 9front (from Rust's nightly source archive) |
| Go | `toolchain/go` | Go for 9front (from Go's release archive) |

All paths come from `dist/paths.env`. Every command below starts in
`~/Devel/nfront` unless it says otherwise.

## 1. Host

Install what [[Host-requirements]] lists under "Always", "Per architecture"
and "Toolchains"; for the CD and the tests also "Guests". Disk: about
170 GB (gcc 70, Rust 50, tree 20, Go 6, guest images 20).

## 2. The sources

```sh
mkdir -p ~/Devel/nfront && cd ~/Devel/nfront
git clone https://github.com/nfront-os/nfront dist
dist/bin/repos --sources
(cd tools/plan9port && ./INSTALL)
```

`dist/bin/repos` clones every part where `paths.env` puts it: the tree with its
worktrees (`tree-gcc`, `tree-nix`, `tree-riscv`, `tree-upstream`), gcc, Rust,
Go, mcp and plan9port. `--sources` then runs each toolchain's `./fetch.sh`
and `dist/bin/fetch`:

- `toolchain/gcc/fetch.sh`: gcc, binutils, gmp, mpfr, mpc (GNU's signatures,
  `sha256.txt`) into `src/`, our patches applied.
- `toolchain/rust/fetch.sh`: Rust's nightly source archive and libc's crate
  (signatures, `sha256.txt`) as the repositories `rust/` (its git data in
  `rust.git`) and `libc/`, our patches on their branch `plan9`; then
  `rust/bootstrap.toml`, `crates/` (the crates.io crates we change, fetched and
  checked against crates.io's index) and `cargo-plan9.toml`.
- `toolchain/go/fetch.sh`: Go's release archive as `go/`, our patches on its
  branch `plan9`.
- `dist/bin/fetch`: the archives of `distfiles.list` (Mesa, Wayland, SDL3, …)
  into `distfiles/`, checked by sha256.

plan9port's `./INSTALL` builds it in place (a few minutes). It writes its own
directory into about 75 of its files; that is expected, and `dist/bin/repos`
knows it.

## 3. Toolchains and tree

```sh
dist/bin/build-toolchains            # amd64 386 arm64; or name the architectures
```

It runs these steps in order, each one's output in `dist/logs/<step>.log`,
and stops at the first failure, showing the end of its log:

| Step | Runs | Time here |
|---|---|---|
| `tree-first` | `dist/bin/build-all`: the tree without the toolchains (gcc's cross compiler is built against its libraries) | 10 min |
| `gcc-A` | `toolchain/gcc`: `objtype=A ./build.sh cross hostlibs native plan9` | 15 min per arch |
| `rust-stage1` | `toolchain/rust/rust`: `./x build --stage 1 library --target <Linux and the arches>` (downloads Rust's stage-0 compiler and its LLVM) | 10 min |
| `llvm-A` | `objtype=A scripts/build-llvm.sh`: LLVM for 9front | 15 min per arch |
| `rustc-A` | `./x build --stage 2 --host T --target T compiler/rustc src/tools/rustdoc src/tools/rustfmt src/tools/clippy` | 10–25 min per arch |
| `stage1-again-A` | `./x build --stage 1 library …` (stage 2 removed the other targets' std) | 1 min |
| `cargo-A` | `objtype=A scripts/build-cargo.sh`: cargo for 9front | 5 min |
| `install-A` | `objtype=A scripts/install.sh`: `out/A`, which is `/A/rust` on 9front | 1 min |
| `go-A` | `toolchain/go`: `objtype=A scripts/build.sh && scripts/install.sh` (the host Go only for the first arch) | 5 min |
| `tree` | `dist/bin/build-all` again, now with the APE parts (Mesa, Wayland, SDL3, …) and the Rust programs (wsys, term, ui) | 15 min |

A is amd64, 386, arm64; T is the Rust target (`x86_64-unknown-plan9`,
`i686-unknown-plan9`, `aarch64-unknown-plan9`). `dist/bin/build-toolchains -n`
prints the steps with their full commands.

When a step fails, read its log and fix the cause. Then continue from that
step; the steps before it are done:

```sh
dist/bin/build-toolchains -from rustc-386
```

The tree's build ends with `NNN files expected, ok` for each architecture
(`dist/logs/tree.log`).

## 4. Boot loaders and the CD

9front's boot loaders are built with 9front's own compilers inside the built
system, in a QEMU guest (needs "Guests" of [[Host-requirements]]):

```sh
cd tree && scripts/guest/build-boot.sh && cd ..
dist/bin/build-all -iso amd64         # ~/.cache/9front-cli/9front.amd64.iso, with Rust and Go
```

The ISO is hybrid (BIOS, UEFI, CD or USB stick). At boot it asks for the
screen (`monitor`, default `vesa`):

| Answer | Screen |
|---|---|
| `vesa` | the firmware's VESA modes; works on every PC, no acceleration |
| `i915` | Intel graphics through the GPU stack (`aux/i915`, gpu(4)) |
| `amdgpu` | AMD graphics through the GPU stack (`aux/amdgpu`, gpu(4)) |
| `virtiogpu` | QEMU's virtio-gpu (`aux/virtiogpu`, gpu(4)) |

With `i915`, `amdgpu` or `virtiogpu` the driver sets up the screen itself; if
it has no picture after 60 seconds, the screen falls back to VESA. Its log
goes to the boot stick's ESP as `i915boot.log`, `amdgpuboot.log` or
`virtiogpuboot.log`. Details: gpu(4).

### In QEMU

| QEMU display | Answer |
|---|---|
| `-vga std` (QEMU's default) | `vesa` |
| `-vga none -device virtio-vga` | `virtiogpu` |
| `-vga none -device virtio-gpu-gl-pci,…` | `virtiogpu`: 3D, Vulkan (venus) and GL (virgl) on the host's GPU |

For 2D use `virtio-vga`, not `virtio-gpu-pci`: it also has a VGA screen, so the
boot loader and the boot questions are visible. `aux/virtiogpu` drives both.

For example, the CD with virtio-gpu:

```sh
qemu-system-x86_64 -enable-kvm -m 4096 -cdrom ~/.cache/9front-cli/9front.amd64.iso \
	-vga none -device virtio-vga
```

3D needs a GPU on the host with Vulkan, KVM, and QEMU with virglrenderer.
These are the options `tree/tests/gpu/run.sh` boots with:

```sh
-enable-kvm -cpu host -m 1024 -vga none \
-device virtio-gpu-gl-pci,blob=true,venus=true,hostmem=256M \
-object memory-backend-memfd,id=mem1,size=1024M,share=on -machine memory-backend=mem1 \
-display egl-headless
```

`-m` must be the memory backend's size. For a window instead of
`egl-headless`, QEMU's `-display gtk,gl=on` should work, but the tests don't use it.

To skip the question, make a CD with the answer in its `plan9.ini`
(`PLAN9INI` takes `name=value` lines that replace the CD's own):

```sh
cd tree && PLAN9INI='monitor=vesa' objtype=amd64 scripts/guest/mkiso.sh    # or i915, amdgpu, virtiogpu
```

The guest that makes the CD holds the whole image in memory: `mkiso.sh` gives
it 6 GB (`MEM=` to change).

## 5. Tests

```sh
cd tree
bash tests/static/run.sh       # seconds: manifests, licences, layouts (needs the Linux sources, see Host-requirements)
bash tests/run.sh guest boot   # the system boots and works in QEMU
bash tests/gpu/run.sh          # ~1 h: LinuxKPI selftests, virtio-gpu, Vulkan, GL, wsys (needs a host GPU)
```

Only one guest at a time: they share `~/.cache/9front-cli`.

## Later: updating

```sh
dist/bin/repos           # fast-forwards every part that is clean and on its branch
dist/bin/status          # each part against manifest.json
```

Then rebuild what changed:

| What changed | Then |
|---|---|
| only the tree | `dist/bin/build-all amd64 386 arm64` (`build.exe -D`: only what is out of date; seconds when nothing is) |
| gcc's patches or `sources.txt` | `cd toolchain/gcc && rm -rf src && ./fetch.sh && cd ../..`, then `dist/bin/build-toolchains -from gcc-amd64` (Rust and the tree depend on gcc) |
| Rust's patches (`toolchain/rust/patches/*`, not `crates`) | `cd toolchain/rust && scripts/rust-patches.sh apply && cd ../..`, then `dist/bin/build-toolchains -from rust-stage1` |
| a crate patch (`toolchain/rust/patches/crates`) | `cd toolchain/rust && scripts/crates-patch.sh apply && scripts/cargo-config.sh && cd ../..`, then `dist/bin/build-toolchains -from cargo-amd64` |
| Rust's `sources.txt` (a new nightly) | `cd toolchain/rust && rm -rf rust rust.git libc && ./fetch.sh && cd ../..`, then `-from rust-stage1` |
| Go's patches or `sources.txt` | `cd toolchain/go && rm -rf go && ./fetch.sh && cd ../..`, then `-from go-amd64` |
| `distfiles.list` | `dist/bin/fetch`, then `dist/bin/build-all amd64 386 arm64` |
| plan9port | `cd tools/plan9port && git checkout . && git pull && ./INSTALL` (`dist/bin/repos` says so too) |

`rm -rf src`, `go` or `rust` throws away work in those directories; the
patches are the record (each toolchain's README says how to write them back).
`rust-patches.sh apply` stops by itself if `plan9` has commits of its own
that the patches lack.

## Not in `build-toolchains`

- **riscv64** (the tree's branch `riscv`, worktree `tree-riscv`; needs
  `riscv64-linux-gnu-gcc`, see [[Host-requirements]]):

  ```sh
  (cd tree-riscv/sys/src/cmd/build && GO111MODULE=off go build -o build.exe .)
  (cd tree-riscv && CC=gcc ARCH=riscv64 sys/src/cmd/build/build.exe)
  (cd toolchain/gcc && objtype=riscv64 ./build.sh cross hostlibs native plan9)   # ~30 min
  ```
- **Self-hosting**: the tree built inside 9front with 9front-gcc,
  `tree/scripts/guest/build-self.sh`.
- **Real hardware** (VFIO GPU tests): `tree/tests/README.md`.
