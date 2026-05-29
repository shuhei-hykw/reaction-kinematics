import os
import numpy as np
import matplotlib.pyplot as plt
from .kinematics import TwoBodyReaction

COLORS = plt.rcParams["axes.prop_cycle"].by_key()["color"]

# Fixed output directory; only the base file name is configurable.
OUTPUT_DIR = "output"
LOCUS_SUFFIX = "_kinematic_locus.png"
CM_LAB_SUFFIX = "_cm_vs_lab_angle.png"
ANGLE_DIST_SUFFIX = "_phase_space_angle.png"
LOCUS_DENSITY_SUFFIX = "_locus_density.png"

# Fixed plot axis ranges.
THETA_LAB_MAX_DEG = 180.0   # lab angle x-axis upper limit
P_LAB_MAX_GEV = 2.0         # lab momentum y-axis upper limit
P_LAB_BINS = 100            # p_lab bins for the 2D locus-density plot

# A case overlays one curve: (reaction, beam momentum [GeV/c], legend label).
Case = tuple[TwoBodyReaction, float, str]
# A phase-space sample: (scan_angle-like dict from generate_phase_space, label).
Sample = tuple[dict, str]


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


#______________________________________________________________________________
def plot_angle_distribution(
    samples: list[Sample],
    n_bins: int,
    output_name: str,
    title: str,
) -> None:
  """Histogram the phase-space lab-angle distribution for each sample."""
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  fig, ax = plt.subplots(figsize=(7, 5))

  bins = np.linspace(0.0, THETA_LAB_MAX_DEG, n_bins + 1)
  for i, (data, label) in enumerate(samples):
    ax.hist(
      data["theta_lab_deg"], bins=bins, weights=data["weights"],
      histtype="step", color=COLORS[i % len(COLORS)], label=label,
    )

  bin_width = THETA_LAB_MAX_DEG / n_bins
  ax.set_xlabel(r"$\theta_{lab}$ [deg]")
  ax.set_ylabel(f"events / {bin_width:.1f} deg")
  ax.set_title(f"Phase-space angular dist.: {title}")
  ax.set_xlim(0.0, THETA_LAB_MAX_DEG)
  ax.legend()
  ax.grid(True, alpha=0.3)

  out_path = os.path.join(OUTPUT_DIR, output_name + ANGLE_DIST_SUFFIX)
  fig.savefig(out_path, dpi=150, bbox_inches="tight")
  plt.close(fig)
  print(f"Saved: {out_path}")


#______________________________________________________________________________
def plot_locus_density(
    samples: list[Sample],
    n_bins: int,
    output_name: str,
    title: str,
) -> None:
  """2D histogram of phase-space events in the (theta_lab, p_lab) plane.

  One panel per sample, so the kinematic locus shows up as a band whose
  colour marks where events concentrate.
  """
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  n = len(samples)
  fig, axes = plt.subplots(
    1, n, figsize=(6 * n, 5), squeeze=False, sharex=True, sharey=True,
  )
  x_edges = np.linspace(0.0, THETA_LAB_MAX_DEG, n_bins + 1)
  y_edges = np.linspace(0.0, P_LAB_MAX_GEV, P_LAB_BINS + 1)

  for ax, (data, label) in zip(axes[0], samples):
    h = ax.hist2d(
      data["theta_lab_deg"], data["p_lab"],
      bins=[x_edges, y_edges], weights=data["weights"],
      cmin=1, cmap="viridis",
    )
    fig.colorbar(h[3], ax=ax, label="events")
    ax.set_xlabel(r"$\theta_{lab}$ [deg]")
    ax.set_title(label)
    ax.set_xlim(0.0, THETA_LAB_MAX_DEG)
    ax.set_ylim(0.0, P_LAB_MAX_GEV)

  axes[0][0].set_ylabel(r"$p_{lab}$ [GeV/c]")
  fig.suptitle(f"Locus density: {title}")

  out_path = os.path.join(OUTPUT_DIR, output_name + LOCUS_DENSITY_SUFFIX)
  fig.savefig(out_path, dpi=150, bbox_inches="tight")
  plt.close(fig)
  print(f"Saved: {out_path}")
