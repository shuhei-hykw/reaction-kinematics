import numpy as np
from particle import Particle


def _mass(name: str) -> float:
  """Return particle mass in GeV."""
  return Particle.from_name(name).mass * 1e-3  # MeV -> GeV


class TwoBodyReaction:
  """Analytical two-body kinematics: beam + target -> ejectile + recoil.

  All quantities in natural units (GeV, GeV/c, GeV/c^2).
  """

  def __init__(self, beam: str, target: str,
               ejectile: str, recoil: str):
    self.m1 = _mass(beam)
    self.m2 = _mass(target)
    self.m3 = _mass(ejectile)
    self.m4 = _mass(recoil)

  def threshold_momentum(self) -> float:
    """Beam momentum threshold for the reaction (GeV/c)."""
    s_thr = (self.m3 + self.m4) ** 2
    e1_thr = (s_thr - self.m1**2 - self.m2**2) / (2 * self.m2)
    p_thr = np.sqrt(max(e1_thr**2 - self.m1**2, 0.0))
    return p_thr

  def sqrt_s(self, p_beam: float) -> float:
    """Invariant mass sqrt(s) for a given beam momentum (GeV/c)."""
    e1 = np.sqrt(p_beam**2 + self.m1**2)
    return np.sqrt(self.m2**2 + self.m1**2 + 2 * self.m2 * e1)

  def _cm_momentum(self, s: float, m_a: float, m_b: float) -> float:
    """CM momentum for a two-particle state."""
    lam = (s - (m_a + m_b)**2) * (s - (m_a - m_b)**2)
    return np.sqrt(np.maximum(lam, 0.0)) / (2 * np.sqrt(s))

  def _beta_gamma_cm(self, p_beam: float):
    """CM frame beta and gamma."""
    e1 = np.sqrt(p_beam**2 + self.m1**2)
    e_tot = e1 + self.m2
    p_tot = p_beam
    s = self.sqrt_s(p_beam)
    beta = p_tot / e_tot
    gamma = e_tot / np.sqrt(s)
    return beta, gamma

  def ejectile_lab(self, p_beam: float,
                   cos_cm: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Compute ejectile lab momentum and lab angle from CM cos(theta).

    Parameters
    ----------
    p_beam : float
        Beam momentum in GeV/c.
    cos_cm : array-like
        CM frame cos(theta) of the ejectile.

    Returns
    -------
    p_lab : ndarray  — lab momentum (GeV/c)
    theta_lab : ndarray  — lab angle (rad)
    """
    cos_cm = np.asarray(cos_cm)
    s = self.sqrt_s(p_beam)
    sq_s = np.sqrt(s)

    p3_cm = self._cm_momentum(s, self.m3, self.m4)
    e3_cm = np.sqrt(p3_cm**2 + self.m3**2)

    beta, gamma = self._beta_gamma_cm(p_beam)

    # Lorentz boost to lab
    p3_z_lab = gamma * (p3_cm * cos_cm + beta * e3_cm)
    p3_t_lab = p3_cm * np.sqrt(np.maximum(1.0 - cos_cm**2, 0.0))

    p_lab = np.sqrt(p3_z_lab**2 + p3_t_lab**2)
    theta_lab = np.arctan2(p3_t_lab, p3_z_lab)
    return p_lab, theta_lab

  def scan_angle(self, p_beam: float,
                 n_points: int = 300) -> dict:
    """Compute kinematic locus over full CM angle range.

    Returns a dict with keys: theta_lab_deg, p_lab, cos_cm, theta_cm_deg.
    """
    cos_cm = np.linspace(-1.0, 1.0, n_points)
    p_lab, theta_lab = self.ejectile_lab(p_beam, cos_cm)
    return {
      "cos_cm":       cos_cm,
      "theta_cm_deg": np.degrees(np.arccos(cos_cm)),
      "p_lab":        p_lab,
      "theta_lab_deg": np.degrees(theta_lab),
    }
