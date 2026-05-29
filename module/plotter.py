import os
import numpy as np
import matplotlib.pyplot as plt
from .kinematics import TwoBodyReaction

COLORS = plt.rcParams["axes.prop_cycle"].by_key()["color"]

# Fixed output directory; only the base file name is configurable.
OUTPUT_DIR = "output"
LOCUS_SUFFIX = "_kinematic_locus.png"
CM_LAB_SUFFIX = "_cm_vs_lab_angle.png"

# Fixed plot axis ranges.
THETA_LAB_MAX_DEG = 180.0   # lab angle x-axis upper limit
P_LAB_MAX_GEV = 2.0         # lab momentum y-axis upper limit

# A case overlays one curve: (reaction, beam momentum [GeV/c], legend label).
Case = tuple[TwoBodyReaction, float, str]


#______________________________________________________________________________
def _draw_cases(
    ax,
    cases: list[Case],
    angle_range: tuple[float, float],
    angle_steps: int,
    y_key: str,
) -> None:
  """Overlay one curve per case, taking the y values from data[y_key]."""
  theta_min, theta_max = angle_range
  for i, (reaction, p_beam, label) in enumerate(cases):
    data = reaction.scan_angle(p_beam, n_points=angle_steps)
    mask = (data["theta_lab_deg"] >= theta_min) & \
           (data["theta_lab_deg"] <= theta_max)
    ax.plot(
      data["theta_lab_deg"][mask],
      data[y_key][mask],
      color=COLORS[i % len(COLORS)],
      label=label,
    )


#______________________________________________________________________________
def plot_kinematic_locus(
    cases: list[Case],
    angle_range: tuple[float, float],
    angle_steps: int,
    output_name: str,
    title: str,
) -> None:
  """Plot ejectile momentum vs lab angle for each case."""
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  fig, ax = plt.subplots(figsize=(7, 5))

  _draw_cases(ax, cases, angle_range, angle_steps, "p_lab")

  ax.set_xlabel(r"$\theta_{lab}$ [deg]")
  ax.set_ylabel(r"$p_{lab}$ [GeV/c]")
  ax.set_title(f"Kinematic locus: {title}")
  ax.set_xlim(0.0, THETA_LAB_MAX_DEG)
  ax.set_ylim(0.0, P_LAB_MAX_GEV)
  ax.legend()
  ax.grid(True, alpha=0.3)

  out_path = os.path.join(OUTPUT_DIR, output_name + LOCUS_SUFFIX)
  fig.savefig(out_path, dpi=150, bbox_inches="tight")
  plt.close(fig)
  print(f"Saved: {out_path}")


#______________________________________________________________________________
def plot_cm_vs_lab_angle(
    cases: list[Case],
    angle_range: tuple[float, float],
    angle_steps: int,
    output_name: str,
    title: str,
) -> None:
  """Plot CM angle vs lab angle for each case."""
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  fig, ax = plt.subplots(figsize=(7, 5))

  _draw_cases(ax, cases, angle_range, angle_steps, "theta_cm_deg")

  ax.set_xlabel(r"$\theta_{lab}$ [deg]")
  ax.set_ylabel(r"$\theta_{CM}$ [deg]")
  ax.set_title(f"CM vs Lab angle: {title}")
  ax.set_xlim(0.0, THETA_LAB_MAX_DEG)
  ax.legend()
  ax.grid(True, alpha=0.3)

  out_path = os.path.join(OUTPUT_DIR, output_name + CM_LAB_SUFFIX)
  fig.savefig(out_path, dpi=150, bbox_inches="tight")
  plt.close(fig)
  print(f"Saved: {out_path}")
