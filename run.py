#!/usr/bin/env python3
"""Entry point for reaction kinematics calculation."""

import argparse
import sys
from module import TwoBodyReaction, load_config
from module.plotter import (
  plot_kinematic_locus,
  plot_cm_vs_lab_angle,
)


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

  reaction = TwoBodyReaction(
    beam=rxn_cfg["beam"],
    target=rxn_cfg["target"],
    ejectile=rxn_cfg["ejectile"],
    recoil=rxn_cfg["recoil"],
  )

  p_thr = reaction.threshold_momentum()
  print(f"Threshold momentum: {p_thr:.4f} GeV/c")

  bm = cfg["beam_momentum"]
  if "scan" in bm:
    beam_momenta = list(bm["scan"])
  else:
    beam_momenta = [float(bm["value"])]

  for p in beam_momenta:
    if p < p_thr:
      print(
        f"WARNING: p_beam={p} GeV/c is below threshold "
        f"({p_thr:.4f} GeV/c)"
      )
      sys.exit(1)

  plot_cfg = cfg["plot"]
  angle_range = tuple(plot_cfg["angle_range"])
  angle_steps = plot_cfg.get("angle_steps", 300)
  output_dir  = plot_cfg.get("output_dir", "output")

  label = (
    f"{rxn_cfg['beam']} + {rxn_cfg['target']} → "
    f"{rxn_cfg['ejectile']} + {rxn_cfg['recoil']}"
  )

  plot_kinematic_locus(
    reaction, beam_momenta, angle_range,
    angle_steps, output_dir, label,
  )
  plot_cm_vs_lab_angle(
    reaction, beam_momenta, angle_range,
    angle_steps, output_dir, label,
  )


if __name__ == "__main__":
  main()
