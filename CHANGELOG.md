# Changelog

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
