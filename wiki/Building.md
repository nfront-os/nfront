# Building

Everything is cross-built on a Linux host (x86-64). gcc and Rust take hours; the tree takes minutes once they are there.

## Prerequisites

See [[Host-requirements]]: what the host needs for the tree, each toolchain,
the guest steps and the tests.

## 0. Layout

Put the repositories where `dist/paths.env` says (see [[Repositories]]),
then fetch the release archives:

```sh
cd ~/Devel/nfront
dist/bin/fetch            # checks every archive by sha256, fetches missing ones
```

## 1. The tree, first pass (no APE, no Rust)

```sh
cd tree/sys/src/cmd/build && GO111MODULE=off go build -o build.exe . && cd -
cd tree && CC=gcc ARCH=amd64 sys/src/cmd/build/build.exe
```

Ends with `NNN files expected, ok`. Steps needing the cross compiler or Rust
are skipped (`nocross`, `norust`). `ARCH=386` / `ARCH=arm64` for the others.

## 2. gcc for 9front

```sh
cd toolchain/gcc
./fetch.sh                                  # sources, GNU signatures, patches
for s in cross hostlibs native plan9; do objtype=amd64 ./build.sh $s; done
```

`cross`: Linux → 9front compiler (used by the tree's APE parts and by Rust).
`native`, `plan9`: gcc that runs on 9front (`out/amd64`, installed as `/amd64/gnu`).
Repeat with `objtype=386`, `arm64`, `riscv64`.

## 3. The tree, complete

```sh
dist/bin/build-all amd64 386 arm64     # checks the toolchains, build.exe -D
```

Now Mesa (`libvulkan.a`), libwayland, SDL3, GLFW and the APE programs are built.

## 4. Rust

```sh
cd toolchain/rust
scripts/rust-patches.sh apply            # branches plan9 from upstream clones
cp bootstrap.toml.example rust/bootstrap.toml   # set $GCC9, $RUST9 to the real paths
cd rust && ./x build --stage 1 library --target x86_64-unknown-linux-gnu,x86_64-unknown-plan9,i686-unknown-plan9,aarch64-unknown-plan9
```

The stage-1 compiler is enough for the tree: `dist/bin/build-all` again
builds wsys, term, wbar, ui. For a Rust that runs on 9front, per target
(`amd64`/`x86_64-unknown-plan9`, `386`/`i686-…`, `arm64`/`aarch64-…`):

```sh
objtype=amd64 scripts/build-llvm.sh
(cd rust && ./x build --stage 2 --host x86_64-unknown-plan9 --target x86_64-unknown-plan9 \
    compiler/rustc src/tools/rustdoc src/tools/rustfmt src/tools/clippy)
(cd rust && ./x build --stage 1 library --target ...all four...)   # stage 2 removes the others' sysroots
objtype=amd64 scripts/build-cargo.sh
objtype=amd64 scripts/install.sh       # out/amd64: /amd64/rust
```

## 5. Go

```sh
cd toolchain/go
git clone --depth 1 --branch go1.27.3 https://go.googlesource.com/go go
git -C go switch -c plan9 && git -C go am $PWD/patches/go/*.patch
objtype=amd64 scripts/build.sh && objtype=amd64 scripts/install.sh    # also 386, arm64
```

## 6. Boot loaders and the CD

```sh
cd tree
scripts/guest/build-boot.sh        # 9front's loaders, built with 8c/6c in a guest
../dist/bin/build-all -iso amd64      # ~/.cache/9front-cli/9front.amd64.iso, with Rust and Go
```

The ISO is hybrid (BIOS, UEFI, USB). Boot options go into `plan9.ini`:

```sh
PLAN9INI='monitor=i915' objtype=amd64 scripts/guest/mkiso.sh
```

## 7. Tests

```sh
bash tests/static/run.sh       # seconds, no build: manifests, licences, layouts
bash tests/gpu/run.sh          # ~1 h: LinuxKPI selftests, i915 mock, virtio-gpu, Vulkan, GL, wsys
bash tests/run.sh guest boot   # more suites: tests/README.md
```
