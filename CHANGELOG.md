# Changelog

## 2026-05-29 14:32 — Phase-space angular frequency and locus density

### Added
- `TwoBodyReaction.generate_phase_space(p_beam, n_events)`: generate the
  two-body final state with the `phasespace` package (isotropic in the CM
  for two bodies) and boost to the lab via `boost_to`. Returns the
  ejectile `theta_lab_deg`, `p_lab` and event `weights`. `phasespace`
  (and hence tensorflow) is imported lazily, with TF logs quieted.
- `plotter.plot_angle_distribution`: histogram of the ejectile lab-angle
  frequency, overlaying the cases.
- `plotter.plot_locus_density`: 2D histogram of events in the
  (theta_lab, p_lab) plane, one panel per case, so the kinematic locus is
  coloured by where events concentrate.
- Opt-in via `plot.n_events` (>0) and `plot.angle_bins`; samples are
  generated once in `run.py` and shared by both phase-space plots.

### Notes
- Phase space only (matrix element assumed flat); the dynamical dsigma/
  dOmega angular dependence is not included.
- For K- + p/9Be -> pi+ + Sigma-/(8He+Lambda) at 1.5 GeV/c: the free
  proton peaks near theta_lab 30-45 deg, while 9Be peaks near 70-90 deg
  with a nearly flat (recoilless) locus.

## 2026-05-29 13:33 — Overlay multiple targets/momenta; nuclear targets

### Added
- Beam momentum may be a `scan` list and `target`/`recoil` may be lists,
  paired element-wise (a scalar is broadcast). All
  (target/recoil pair, momentum) combinations are overlaid on one plot,
  with a legend distinguishing the varying quantities.
- Composite mass syntax `'A + B'` (spaced, to avoid clashing with the
  `+` in charged names like `pi+`). A nuclear target's hypernuclear
  recoil is modelled as core nucleus + Lambda with zero separation
  energy (B_Lambda = 0); e.g. `recoil: "C11 + Lambda"`. Real hypernuclear
  masses are not available in the `particle` package, and Fermi motion
  is left for a future extension.
- `module/plotter.py`: `_draw_cases()` helper; plot functions now take a
  list of cases `(reaction, p_beam, label)` instead of a single
  reaction + momentum list.
- Example configs `config/dcx_kpi_scan.yaml` (momentum scan) and
  `config/ncx_pik_target_compare.yaml` (free n vs bound in 12C for
  (pi+, K+)Lambda; demonstrates the recoilless behaviour on a heavy
  nucleus).

## 2026-05-29 11:00 — Add (K-, pi+)Sigma- reaction; mathtext titles

### Added
- `config/dcx_kpi_1.50.yaml`: DCX, kpi probe `p(K-, pi+)Sigma-` at
  1.5 GeV/c. Exothermic (threshold 0); the light pi+ ejectile is emitted
  over the full 0-180 deg range (single-valued locus), unlike the
  threshold-confined pik reactions.
- `latex_name()` in `module/kinematics.py`: render particle names as
  mathtext via the `particle` package `latex_name` (e.g. pi-, Sigma-,
  Lambda). Plot titles now use proper math notation.

### Changed
- Fixed plot axis ranges via constants `THETA_LAB_MAX_DEG = 180` and
  `P_LAB_MAX_GEV = 2`, so different reactions/momenta share one scale.

## 2026-05-29 10:31 — Add separator comments above definitions

### Changed
- Apply new CLAUDE.md style rule: a 79-char separator comment is placed
  above every function and class definition (`run.py`, `module/*.py`).
  - Module level: `#` + 78 underscores.
  - Class methods (2-space indent): `  #` + 76 underscores.

## 2026-05-29 10:25 — Configurable output base name; fixed output dir

### Changed
- Output directory is now fixed to `output/` (constant `OUTPUT_DIR` in
  `module/plotter.py`); it is no longer set from the config.
- Output file name is now driven by the config `plot.name` (base name).
  Each run writes `{name}_kinematic_locus.png` and
  `{name}_cm_vs_lab_angle.png`, so different reactions no longer
  overwrite each other in the shared directory.
- `run.py` reads `plot.name` instead of `plot.output_dir`.

## 2026-05-29 10:20 — Reorganise example configs by reaction type

### Changed
- Replace the ambiguous, charge-violating `config/example.yaml`
  (pi- + p -> K+ + Lambda violates charge conservation) with explicitly
  named configs.
- Naming scheme `<cx>_<probe>_<momentum>.yaml`, encoding the
  charge-exchange character and the probe, since NCX/DCX alone is
  ambiguous (both pik and kpi are possible):
  - `ncx_pik_1.05.yaml`: NCX, n(pi+, K+)Lambda at 1.05 GeV/c
    (baryon charge unchanged; standard Lambda hypernuclear production).
  - `dcx_pik_1.20.yaml`: DCX, p(pi-, K+)Sigma- at 1.20 GeV/c
    (baryon charge changes by two units).

### Notes
- Both reactions sit just above threshold (0.887 and 1.035 GeV/c), so
  the ejectile is confined to a forward cone with a maximum lab angle
  (~57 deg for NCX, ~50 deg for DCX) and the kinematic locus is
  double-valued.

## 2026-05-29 10:04 — Fix double square-root of Mandelstam s

### Fixed
- `module/kinematics.py`: `sqrt_s()` returns sqrt(s), but callers
  treated it as the Mandelstam variable `s` and applied `np.sqrt()`
  again, corrupting the kinematics.
  - `_beta_gamma_cm`: `gamma = e_tot / np.sqrt(s)` used the already
    square-rooted value, giving gamma=1.907 instead of 1.325 at
    p_beam=1.8 GeV/c.
  - `ejectile_lab`: passed sqrt(s) into `_cm_momentum()` as `s`, making
    the Kallen lambda negative; clamped to zero it forced p3_cm=0, so
    the ejectile carried no CM momentum. Result: theta_lab was 0 for all
    CM angles and p_lab was a constant 0.6175 GeV/c.
  - Fix: use sqrt_s directly for gamma; compute `s = sqrt_s**2` before
    calling `_cm_momentum`.
- Now physically correct for pi- + p -> K+ + Lambda at 1.8 GeV/c:
  theta_lab spans 0-180 deg, p_lab=1.513 GeV/c forward and 0.133 GeV/c
  backward; theta_lab=42 deg at theta_cm=90 deg.

### Notes
- Created Python 3.12 `.venv` (default python3 is 3.14, for which
  tensorflow has no wheel; phasespace requires tensorflow).

## 2026-05-27 17:15 — Update CLAUDE.md coding rules

### Changed
- Add Git rule: never include "Co-Authored-By: Claude" in commit messages
- Add Documentation rule: CHANGELOG.md must be updated in every commit

## 2026-05-27 16:00 — Initial implementation of two-body kinematics

### Added
- `run.py`: entry point, reads YAML config and generates plots
- `module/kinematics.py`: analytical two-body kinematics (`TwoBodyReaction`)
  - threshold momentum calculation
  - Lorentz boost from CM to lab frame
  - kinematic locus scan over full CM angle range
- `module/plotter.py`: matplotlib-based plots
  - ejectile momentum vs lab angle (kinematic locus)
  - CM angle vs lab angle
  - supports multiple beam momenta (scan mode)
- `module/config.py`: YAML config loader
- `config/example.yaml`: example config for pi- + p -> K+ + Lambda

### Dependencies
- `numpy`, `matplotlib`, `pyyaml` (via conda)
- `vector`, `particle`, `phasespace` (via conda-forge)
- Python 3.12 (`py3.12` conda environment)

### Notes
- ROOT-free implementation; phase space MC (`phasespace`) available for
  future use
- Particle masses fetched from PDG data via the `particle` package
