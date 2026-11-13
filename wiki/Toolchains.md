# Using gcc, Rust and Go

nfront's toolchains run on 9front itself (native) and on Linux (cross). This
page shows how to use them and how to rebuild the system with gcc.
[[Building]] describes how they are built.

## Getting them onto 9front

The CD of the profile `full` (`dist/bin/mkcd full`, see [[Building]]) carries all three, as does any profile with `-dev all`:

| Toolchain | On 9front | Built in |
|---|---|---|
| gcc 16, binutils 2.47 | `/amd64/gnu` | `toolchain/gcc/out/amd64` |
| Rust (rustc, cargo, rustdoc, rustfmt, clippy) | `/amd64/rust` | `toolchain/rust/out/amd64` |
| Go | `/amd64/go` | `toolchain/go/out/amd64` |

On a system installed some other way, copy them over as archives, with paths
from `/` (on 386 or arm64 replace amd64 and the Rust target):

```sh
# on Linux, in ~/Devel/nfront
tar -C toolchain/gcc/out/amd64 -czf gnu-amd64.tgz amd64        # gcc has no archive of its own
ls toolchain/rust/out/amd64/*.tgz toolchain/go/out/amd64/*.tgz
```

```rc
# on 9front, with the archives in the current directory
cd / && tar xzf $home/gnu-amd64.tgz
cd / && tar xzf $home/rust-x86_64-unknown-plan9.tgz && tar xzf $home/rust-tools-x86_64-unknown-plan9.tgz
cd / && tar xzf $home/go-plan9-amd64.tgz
```

Rust needs gcc: rustc links with it.

## gcc

```rc
bind -b /$objtype/gnu/bin /bin
```

| Kind of program | Command |
|---|---|
| POSIX (over APE) | `gcc -o hello hello.c` (implies `-D_POSIX_SOURCE`, links `-lbsd -lap`) |
| BSD functions, sockets | `gcc -D_BSD_EXTENSION -o prog prog.c` (as with pcc) |
| native Plan 9 C | `gcc -nostdinc -I/$objtype/include -I/sys/include -fplan9-extensions -fno-builtin -c prog.c`, then `gcc -nostdlib -o prog prog.o -L/$objtype/lib.gcc -lc -lgcc` |
| C++ | `g++ -o prog prog.cc` (libstdc++ over APE: exceptions, threads, `<format>`; only the "C" locale) |

Things to know:

- C defaults to gnu17. gcc ignores `#pragma lib`, so name the libraries
  (`-lthread -lbio …` for native code).
- gcc's APE adds C99 and POSIX.1-2008 to 9front's: `<math.h>` with float and
  long double, `<fenv.h>`, `<complex.h>`, C99 printf/scanf, `<wchar.h>` (32-bit
  `wchar_t`, UTF-8), `clock_gettime`, `nanosleep`, `<pthread.h>` (a thread is a
  proc), `poll`, `mmap`.
- A program starts as on other POSIX systems: floating point exceptions masked,
  x87 at 64-bit precision.
- APE's stdio is not thread-safe: threads that share a `FILE` must lock it themselves.

More detail: `toolchain/gcc/README.md`.

### 9front's mkfiles with gcc: gccmk

```rc
bind -b /$objtype/gnu/bin /bin
cd /sys/src/cmd/hoc && gccmk install
```

`gccmk` runs mk with gcc instead of 6c/6a/6l (8c, 7c). The objects come out
the same as the tree's own build. It works for programs and libraries, but not
for the kernel or libc as a whole: libc's `9syscall` writes 6a assembly.

## Rust

```rc
bind -b /$objtype/gnu/bin /bin
bind -b /$objtype/rust/bin /bin
rustc hello.rs && ./hello
cargo new hello && cd hello && cargo run
```

- cargo needs the CA roots in `/sys/lib/tls/ca.pem` for crates.io.
- Crates with C code build through gcc (APE). Crates that 9front needs
  changes for come from nfront's patches (`toolchain/rust/crates`); in your own
  project, use them through `[patch.crates-io]` like `toolchain/rust/cargo-plan9.toml`.
- The other tools: `rustdoc`, `rustfmt`, `cargo fmt`, `cargo clippy`.

From Linux (cross), with the stage-1 compiler and gcc's cross compiler:

```sh
cd ~/Devel/nfront/toolchain/rust
TOP=$PWD; . scripts/nfront-paths.sh
PATH=$GCC_DIR/build/amd64/cross/bin:$PATH
rust/build/host/stage1/bin/rustc --edition 2024 --target x86_64-unknown-plan9 -O hello.rs
```

Targets: `x86_64-unknown-plan9`, `i686-unknown-plan9`, `aarch64-unknown-plan9`.
The tree builds its Rust programs this way (`tree/scripts/build/cargo.sh`).

## Go

```rc
bind -b /$objtype/go/bin /bin
go run hello.go
go build -o hello hello.go
```

- `go` finds its tree at `/$objtype/go`; you don't need `$GOROOT`.
- On the live CD `$home` is read-only: set `GOCACHE=/tmp/go-build`.
- The first build compiles std (about two minutes on amd64 under KVM).
- cgo works on amd64, 386 and arm64: gcc links the program against APE into an ELF
  program (without cgo, Go writes a.out as usual).

From Linux (cross):

```sh
cd ~/Devel/nfront/toolchain/go
GOOS=plan9 GOARCH=amd64 go/bin/go build -o hello hello.go     # 386, arm64 likewise
```

## Rebuilding the system with gcc

### The whole tree, in a guest, from Linux

```sh
cd ~/Devel/nfront/tree
scripts/guest/build-self.sh               # amd64; objtype=386 for 386
```

The script:

1. boots the built system in QEMU with the native gcc (`/$objtype/gnu`);
2. gives the guest a copy of the tree's sources (`git ls-files`) on an ext4
   disk;
3. runs the tree's own build tool there (`build.exe`, built for Plan 9) with
   gcc, exactly as `CC=gcc ARCH=$objtype build.exe` on Linux does;
4. copies the result back to `~/.cache/9front-cli/self.$objtype` and compares
   every object with the Linux build.

It needs the tree built for that architecture and `toolchain/gcc/out/$objtype`
(see [[Building]]), plus the "Guests" part of [[Host-requirements]]. It takes
hours. `KEEP=1` continues in the last copy after a fix; arguments name single
manifests, e.g. `sys/src/ape/cmd/cmds.json`.

Last run: 2026-10-22, on the state of the branch `gcc`. amd64 and 386 built
completely in the guest, every object byte-identical to the Linux build, and
the kernel built there boots. The steps `main` has added since (Mesa through
the cross compiler, the Rust programs, the LinuxKPI) have not been run in the
guest yet.

### The whole tree, by hand on 9front

This is what `build-self.sh` types in the guest (`tree/scripts/guest/boot/mkself.rc`).
You need:

- the tree's sources at some path, here `/n/src9`;
- `build.exe` for Plan 9 in it. Build it on Linux:

  ```sh
  cd tree/sys/src/cmd/build && GOOS=plan9 GOARCH=amd64 GO111MODULE=off go build -o build.exe .
  ```

  On 9front, Go can build it too:

  ```rc
  cd sys/src/cmd/build; GO111MODULE=off go build -o build.exe .
  ```

  The Go-on-9front route is untested.

Then:

```rc
cd /n/src9
bind /n/src9/sys/include /sys/include
bind /n/src9/$objtype/include /$objtype/include
@{
	rfork E
	path=(/$objtype/gnu/bin /bin .)
	PLAN9=/n/src9
	ARCH=$objtype
	objtype=$objtype
	cputype=$cputype
	CC=gcc
	NPROC=`{wc -l </dev/sysstat}
	CPUS=$NPROC
	user=$user
	home=/tmp
	sys/src/cmd/build/build.exe
}
```

`rfork E` gives the build an empty environment. The build tool hands its
environment on to its commands as Go sees it, and rc can't read its own
functions back from that, so the block sets every variable the build needs
again.

The binaries and the kernel land in `/n/src9/$objtype`, as on Linux. To build
only some manifests, name them: `sys/src/cmd/build/build.exe sys/src/cmd/cmds.json`.
