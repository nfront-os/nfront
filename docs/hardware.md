# Hardware matrix

What nfront has run on, and how far. The roadmap's 1.0 asks for this table
published, with VESA as the guarantee: the aim is that every machine with
a VESA BIOS or UEFI GOP gets rio and the desktop (wsys composing on the
processor), with or without a GPU driver; the rows below say where that
was seen.

Levels:

- **tested**: a test suite ran on it and passed (named in the row).
- **works**: used by hand and seen working; no suite, or only part of one.
- **fails**: tried, does not work (what fails is said).
- **untested**: expected to work (a driver is there), never run.

Every run on real hardware below predates the userland's switch to `-O2`
(2026-11-13); QEMU's rows are from the suites after it, where not said
otherwise.

## Machines

| Machine | Part | Level | Last run | Notes |
|---|---|---|---|---|
| Lenovo ThinkPad X1 Carbon (2015, Broadwell) | boot, amd64 CD | tested | 2026-11-11 | CD and USB stick up to rio; `tests/hw` stick runs (disk read-only, usb, net listing, clock) |
| | GPU: Intel HD 5500 (i915) | tested | 2026-11-11 | `aux/i915`, eDP 1920×1080, Vulkan through hasvk (vulkaninfo, vktri, vkcube ~71 fps); laptop runs 9 and 10 of the desktop green (`deskrun`, `comprun`, `wlrun`, overlay plane) |
| | desktop (`desktop=wsys`) | tested | 2026-11-11 | wsys on i915, wbar, title bars, Mod4+Tab, Wayland (foot) |
| | xHCI | works | 2026-11-01 | the test stick boots and is read from it |
| | backlight, external monitor | untested | | open in `MEMORY.md` |
| HP Mini 2140 (Atom N270, 945GSE, UHCI+EHCI) | boot, 386 CD | fails | 2026-10-14 | the boot stops (not looked at since; 386 comes later) |
| AMD Radeon RX 7600 XT (Navi 33) | GPU, by VFIO in a QEMU guest | tested | 2026-11-12 | `amdall.rc`: `aux/amdgpu`, RADV (Vulkan), wsys composing on the GPU, overlay plane, eframe/egui on wgpu, SDL3 on Vulkan, ui on vello/wgpu |
| | second monitor | untested | | |

## QEMU (the test suites)

| Device | Level | Suite |
|---|---|---|
| amd64, 386, arm64 (virt, GICv3) guests | tested | `tests/run.sh boot guest` (amd64 all green; 386: APE shared memory cannot grow, arm64: no segment(3), see `tree/MEMORY.md`) |
| VESA (`aux/realemu`) | tested | amd64: `gui`, `ui`, `draw`, `sdl`, `glfw`, `winit`, `uiserver`, `wayland`; 386: `ui` (2026-11-11, before `-O2`) |
| virtio-gpu 2D (`aux/virtiogpu`) | tested | `gpu` (mode switch, drawing, interrupts) |
| virtio-gpu-gl with virgl and venus (Vulkan, GL by zink) | tested | `gpu` (139 checks), `wayland` |
| install CD: BIOS and UEFI, as CD and as USB stick | tested | `iso` (all four profiles) |
| USB: xHCI, EHCI, UHCI (a stick) | tested | `usb` |
| USB: OHCI | fails | `usb` with `USB_CTLRS=ohci`; fails with 9front's own release too |
| e1000, virtio-net | tested | every guest boot (9P root over the network) |
| IDE disk (QEMU's default) | tested | `iso` (booted as a disk); `disk` (the hjfs install image) last before `-O2` |

## How to add a row

Run the CD (or `tests/hw`'s stick) on the machine, then put the machine,
the part, the level, the date and what ran into the table; a failure
gets what failed. The suites' names are in `tree/tests/README.md`.
