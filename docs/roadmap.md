# nfront: Weg zur Distribution

Ausgangspunkt war eine Bewertung des Projekts. Abweichend von deren
Empfehlung (Overlay auf 9front, Upstream-Merge als Option) ist nfront eine
**eigene Distribution** (Entscheidung 2026-11-12): eigener Name, eigene
Replica und ISOs. 9front `front` bleibt die Quelle, die regelmäßig
eingespielt wird (`upstream.md`); einzelne Korrekturen gehen weiter als
Patches an 9front (`patch-upstream/` im Tree).

## Stand (2026-11-12)

- Teile und Pfade: `../paths.env`, `../manifest.json`, `../bin/status`.
- Lizenzen: Im Tree und in seiner Git-Historie kein GPL-Code von Linux
  (LinuxKPI aus OpenBSD/FreeBSD-Vorlagen, `scripts/linux/provenance.py` in
  `tests/static`). Ausnahmen: Bison-Parser (GPL mit Bison-Ausnahme),
  doppelt lizenzierte Dateien (eine permissive Wahl), Firmware getrennt
  unter `/lib/firmware`.
- Tests: `tests/static`, `tests/gpu/run.sh` (QEMU, ~140 Prüfungen),
  RX 7600 per VFIO (`amdall.rc`); Laptop (i915) seit Linux 7.3 ungetestet.

## Phase 0: Reference Build (Wochen)

Ziel: ein reproduzierbarer Build, ein ISO, eine grüne Test-Suite.

- `bin/build-all`: Toolchains (nur wenn ihr Commit sich ändert) → Tree
  (`build.exe -D` je Arch) → ISO (`scripts/guest/mkiso.sh` mit Rust und Go).
- Umzug nach `~/Devel/nfront/` (Umbrella; nur `paths.env` ändert sich).
- `distfiles/` mit `SHA256SUMS` statt `9front-ui/src`; `bin/fetch`.
- ISO amd64 mit `desktop=wsys`; VESA, virtio-gpu, amdgpu, i915.
- Ergebnis: **0.1-preview**, intern.

## Phase 1: Daily Driver (Monate)

Ziel: ein Arbeitstag auf dem Desktop.

- wsys als Standard; term, ui-Programme, wbar, Theme.
- draw(3)-, Wayland- (foot) und Vulkan-Programme im Alltag.
- Replica + `pull` mit Rückweg; Kanal `current`.
- Referenz-Workflow ohne Browser: term, Editor (acme/sam),
  Dateimanager, ui-Client, draw(3)-Programm, Wayland-Programm, 9P im Netz.
- Ergebnis: **0.9-beta**, öffentlich, mit Hardware-Matrix.

## Phase 2: Stable

Ziel: **1.0** mit eingefrorener öffentlicher API.

- ui(4), uiview, libui, uigo, p9win eingefroren; Versionen.
- Rebase-Zyklus für Linux (DRM), Mesa, Rust, Go, gcc, wgpu/winit
  (`patches.md`).
- Sicherheitsmodell von wsys/ui (Dateirechte, Namespaces, Pufferbesitz).
- Signierte ISOs, SBOM (aus `manifest.json` und den distfiles), Kanal
  `release`.

## Phase 3: Plattform

arm64-GPU, riscv64 (Rust-Ziel, Treiber), weitere Treiber; Programme
daneben als Pakete (GPL dort zulässig, nicht im Tree).

## Die fünf 1.0-Kriterien

1. Ein Arbeitstag auf dem Laptop ohne Absturz (term, ui, draw(3),
   Wayland, Vulkan, Netz).
2. Reproduzierbarer Build auf zwei Maschinen byte-gleich, mit Rust-Bootstrap.
3. `pull` aktualisiert und rollt zurück (oder dokumentiert, was verloren geht).
4. Öffentliche API eingefroren, mit Manpages und Beispielen.
5. Hardware-Matrix veröffentlicht (getestet/läuft/ungetestet; VESA als
   Garantie).
