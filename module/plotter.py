import os
import numpy as np
import matplotlib.pyplot as plt
from .kinematics import TwoBodyReaction

COLORS = plt.rcParams["axes.prop_cycle"].by_key()["color"]


def plot_kinematic_locus(
    reaction: TwoBodyReaction,
    beam_momenta: list[float],
    angle_range: tuple[float, float],
    angle_steps: int,
    output_dir: str,
    reaction_label: str,
) -> None:
  """Plot ejectile momentum vs lab angle for each beam momentum."""
  os.makedirs(output_dir, exist_ok=True)
  fig, ax = plt.subplots(figsize=(7, 5))

  theta_min, theta_max = angle_range

  for i, p_beam in enumerate(beam_momenta):
    data = reaction.scan_angle(p_beam, n_points=angle_steps)
    mask = (data["theta_lab_deg"] >= theta_min) & \
           (data["theta_lab_deg"] <= theta_max)
    ax.plot(
      data["theta_lab_deg"][mask],
      data["p_lab"][mask],
      color=COLORS[i % len(COLORS)],
      label=f"$p_{{beam}}$ = {p_beam:.2f} GeV/c",
    )

  ax.set_xlabel(r"$\theta_{lab}$ [deg]")
  ax.set_ylabel(r"$p_{lab}$ [GeV/c]")
  ax.set_title(f"Kinematic locus: {reaction_label}")
  ax.legend()
  ax.grid(True, alpha=0.3)

  out_path = os.path.join(output_dir, "kinematic_locus.png")
  fig.savefig(out_path, dpi=150, bbox_inches="tight")
  plt.close(fig)
  print(f"Saved: {out_path}")


def plot_cm_vs_lab_angle(
    reaction: TwoBodyReaction,
    beam_momenta: list[float],
    angle_range: tuple[float, float],
    angle_steps: int,
    output_dir: str,
    reaction_label: str,
) -> None:
  """Plot CM angle vs lab angle for each beam momentum."""
  os.makedirs(output_dir, exist_ok=True)
  fig, ax = plt.subplots(figsize=(7, 5))

  theta_min, theta_max = angle_range

  for i, p_beam in enumerate(beam_momenta):
    data = reaction.scan_angle(p_beam, n_points=angle_steps)
    mask = (data["theta_lab_deg"] >= theta_min) & \
           (data["theta_lab_deg"] <= theta_max)
    ax.plot(
      data["theta_lab_deg"][mask],
      data["theta_cm_deg"][mask],
      color=COLORS[i % len(COLORS)],
      label=f"$p_{{beam}}$ = {p_beam:.2f} GeV/c",
    )

  ax.set_xlabel(r"$\theta_{lab}$ [deg]")
  ax.set_ylabel(r"$\theta_{CM}$ [deg]")
  ax.set_title(f"CM vs Lab angle: {reaction_label}")
  ax.legend()
  ax.grid(True, alpha=0.3)

  out_path = os.path.join(output_dir, "cm_vs_lab_angle.png")
  fig.savefig(out_path, dpi=150, bbox_inches="tight")
  plt.close(fig)
  print(f"Saved: {out_path}")
