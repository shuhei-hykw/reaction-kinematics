#!/usr/bin/env python3
"""Entry point for reaction kinematics calculation."""

import argparse
import sys
from module import TwoBodyReaction, load_config, latex_name
from module.plotter import (
  plot_kinematic_locus,
  plot_cm_vs_lab_angle,
)


#______________________________________________________________________________
def main():
  parser = argparse.ArgumentParser(
    description="Two-body reaction kinematics plotter"
  )
  parser.add_argument(
    "config", help="Path to YAML config file"
  )
  args = parser.parse_args()

  cfg = load_config(args.config)
  rxn_cfg = cfg["reaction"]
  beam = rxn_cfg["beam"]
  ejectile = rxn_cfg["ejectile"]

  # target and recoil may each be a single value or a list; they are
  # paired (a nuclear target needs its own hypernuclear recoil). A scalar
  # is broadcast to the other's length. The beam momentum may also be a
  # scan; all (target/recoil pair, momentum) combinations are overlaid.
  targets = rxn_cfg["target"]
  if isinstance(targets, str):
    targets = [targets]
  recoils = rxn_cfg["recoil"]
  if isinstance(recoils, str):
    recoils = [recoils]
  if len(targets) == 1:
    targets = targets * len(recoils)
  elif len(recoils) == 1:
    recoils = recoils * len(targets)
  if len(targets) != len(recoils):
    print("ERROR: target and recoil lists must have equal length")
    sys.exit(1)

  bm = cfg["beam_momentum"]
  if "scan" in bm:
    beam_momenta = [float(p) for p in bm["scan"]]
  else:
    beam_momenta = [float(bm["value"])]

  multi_case = len(targets) > 1

  cases = []  # (reaction, p_beam, legend label) per overlaid curve
  for tgt, rec in zip(targets, recoils):
    reaction = TwoBodyReaction(beam, tgt, ejectile, rec)
    p_thr = reaction.threshold_momentum()
    print(
      f"Threshold momentum ({beam}+{tgt}->{ejectile}+{rec}): "
      f"{p_thr:.4f} GeV/c"
    )
    for p in beam_momenta:
      if p < p_thr:
        print(
          f"WARNING: skip p_beam={p} GeV/c "
          f"({tgt}->{rec} threshold {p_thr:.4f} GeV/c)"
        )
        continue
      mom = f"$p_{{beam}}$ = {p:.2f} GeV/c"
      label = f"{latex_name(tgt)}, {mom}" if multi_case else mom
      cases.append((reaction, p, label))

  if not cases:
    print("ERROR: no (target, momentum) combination above threshold")
    sys.exit(1)

  plot_cfg = cfg["plot"]
  angle_range = tuple(plot_cfg["angle_range"])
  angle_steps = plot_cfg.get("angle_steps", 300)
  output_name = plot_cfg["name"]

  # de-duplicate (a broadcast scalar repeats) while keeping order
  target_str = "/".join(latex_name(t) for t in dict.fromkeys(targets))
  recoil_str = "/".join(latex_name(r) for r in dict.fromkeys(recoils))
  title = (
    f"{latex_name(beam)} + {target_str} $\\to$ "
    f"{latex_name(ejectile)} + {recoil_str}"
  )

  plot_kinematic_locus(
    cases, angle_range, angle_steps, output_name, title,
  )
  plot_cm_vs_lab_angle(
    cases, angle_range, angle_steps, output_name, title,
  )


if __name__ == "__main__":
  main()
