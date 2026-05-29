# reaction-kinematics

Analytical two-body reaction kinematics plotter for
`beam + target -> ejectile + recoil`. ROOT-free; particle masses are
taken from PDG data via the `particle` package.

## Setup

`phasespace` depends on `tensorflow`, which currently has no wheel for
Python 3.14. Use Python 3.12 for the virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python run.py config/ncx_pik_1.05.yaml
```

This prints the beam-momentum threshold and writes plots to the fixed
`output/` directory, named from the config `plot.name`:

- `{name}_kinematic_locus.png` — ejectile lab momentum vs lab angle
- `{name}_cm_vs_lab_angle.png` — CM angle vs lab angle

If `plot.n_events` is set (> 0), two phase-space plots are also written
(generated with the `phasespace` package, isotropic in the CM for two
bodies; matrix element assumed flat):

- `{name}_phase_space_angle.png` — lab-angle frequency histogram
- `{name}_locus_density.png` — 2D density on the (theta_lab, p_lab)
  plane, showing where events concentrate along the locus

## Configuration

Fields:

- `reaction`: particle names (`beam`, `target`, `ejectile`, `recoil`)
- `beam_momentum`: a single `value` or a `scan` list (GeV/c)
- `plot`: lab `angle_range` [deg], `angle_steps`, and `name`
  (output base name; the directory is fixed to `output/`).
  Optional: `n_events` (> 0 enables the phase-space plots) and
  `angle_bins` (histogram bins over 0-180 deg, default 90)

Particle names follow the `particle` package (e.g. `pi+`, `K+`,
`Sigma-`; nuclei as `C12`, `Be9`). Names must conserve charge,
baryon number and strangeness.

### Overlaying multiple conditions

`beam_momentum.scan` and a list-valued `target`/`recoil` are all
overlaid on a single plot. `target` and `recoil` are paired
element-wise (a scalar is broadcast to the other's length), since a
nuclear target needs its own recoil.

A hypernuclear recoil is written as a composite `'core + Lambda'`
(spaced `+`, to avoid clashing with the `+` in charged names). Its mass
is the sum of the components, i.e. core nucleus + Lambda with zero
separation energy (`B_Lambda = 0`); real hypernuclear masses are not in
`particle`, and Fermi motion is not modelled. Example:
`target: ["n", "C12"]`, `recoil: ["Lambda", "C11 + Lambda"]`.

### Example configs

Named `<cx>_<probe>_<momentum>.yaml`, encoding the charge-exchange
character and the probe (NCX/DCX alone is ambiguous, since both `pik`
and `kpi` are possible):

- `ncx_pik_1.05.yaml` — NCX: `n(pi+, K+)Lambda` at 1.05 GeV/c
  (baryon charge unchanged; standard Lambda hypernuclear production)
- `dcx_pik_1.20.yaml` — DCX: `p(pi-, K+)Sigma-` at 1.20 GeV/c
  (baryon charge changes by two units)
- `dcx_kpi_1.50.yaml` — DCX, kpi probe: `p(K-, pi+)Sigma-` at 1.50 GeV/c
- `dcx_kpi_scan.yaml` — `p(K-, pi+)Sigma-` over a momentum scan
- `ncx_pik_target_compare.yaml` — `(pi+, K+)Lambda` on a free neutron
  vs bound in 12C

## Module layout

- `module/kinematics.py` — `TwoBodyReaction` (threshold momentum,
  Lorentz boost from CM to lab, kinematic locus scan, phase-space MC via
  `phasespace`); `latex_name()` and composite-mass support
- `module/plotter.py` — matplotlib plots; overlays a list of cases, plus
  phase-space angle histogram and (theta_lab, p_lab) density
- `module/config.py` — YAML config loader
