"""Shared settings: plotting style, material database, micromechanics helpers.
All property values are representative literature values (see report, Table 3-x);
they are inputs for feasibility screening, not measured data."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "figures")
RES = os.path.join(ROOT, "results")

# ---- plotting style (validated categorical order, light mode) ----
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({
    "font.sans-serif": ["WenQuanYi Zen Hei", "DejaVu Sans"],
    "font.family": ["WenQuanYi Zen Hei", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "font.size": 10, "mathtext.fontset": "dejavusans", "axes.titlesize": 11, "axes.labelsize": 10,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "lines.linewidth": 2.0, "lines.markersize": 6,
    "legend.frameon": False, "figure.dpi": 110, "savefig.dpi": 200,
    "savefig.bbox": "tight", "figure.facecolor": "white", "axes.facecolor": "white",
})

def savefig(fig, name):
    path = os.path.join(FIG, name)
    fig.savefig(path)
    plt.close(fig)
    print("saved", path)
    return path

def save_results(name, d):
    def conv(o):
        if isinstance(o, (np.floating,)): return float(o)
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, np.ndarray): return o.tolist()
        return str(o)
    with open(os.path.join(RES, name + ".json"), "w") as f:
        json.dump(d, f, indent=1, ensure_ascii=False, default=conv)

# ---- material database (SI units) ----
# E [Pa], nu, alpha [1/K], KIC [Pa m^0.5], k [W/mK], Dk, Df(@~10 GHz), n (1030 nm)
MAT = {
    # electroplated Cu: freestanding TGV-Cu yield ~123 MPa (Ahmed et al., TDMR 2020)
    "Cu":   dict(E=110e9, nu=0.34, alpha=17.0e-6, k=390.0, rho=1.8e-8, sy0=125e6, sy400=50e6, Hk=1.5e9),
    "FS":   dict(name="熔融石英 FS", E=73e9, nu=0.17, alpha=0.55e-6, KIC=0.75e6, k=1.38, Dk=3.87, Df=2e-4, m=10, s0=120e6),
    "BG":   dict(name="无碱硼铝硅玻璃 BG", E=74e9, nu=0.22, alpha=3.2e-6, KIC=0.75e6, k=1.1, Dk=5.1, Df=5e-3, m=10, s0=120e6),
    "GCC":  dict(name="微晶玻璃 GC-C(堇青石型,低CTE)", E=110e9, nu=0.25, alpha=3.5e-6, KIC=2.0e6, k=3.0, Dk=5.2, Df=5e-4, m=16, s0=250e6),
    "GCF":  dict(name="微晶玻璃 GC-F(镁橄榄石型,中CTE)", E=105e9, nu=0.25, alpha=7.5e-6, KIC=2.0e6, k=3.5, Dk=6.6, Df=5e-4, m=16, s0=250e6),
    "Si":   dict(name="硅 Si", E=130e9, nu=0.28, alpha=2.6e-6, k=148.0, Dk=11.9, Df=5e-3),
    "ORG":  dict(name="有机芯板 BT", E=28e9, nu=0.2, alpha=13e-6, k=0.6, Dk=4.2, Df=6e-3),
    "ABF":  dict(name="ABF 积层", E=5e9, nu=0.3, alpha=30e-6, k=0.3, Dk=3.3, Df=4.4e-3),
    "POLY": dict(name="聚合物衬层", E=3e9, nu=0.35, alpha=40e-6),
}
SUBS = ["FS", "BG", "GCC", "GCF"]
# two-phase constituents of glass-ceramics (representative values)
PHASE = {
    "glass":      dict(name="残余玻璃(低碱MAS/BAS)", E=80e9, nu=0.23, alpha=4.0e-6, k=1.2, Dk=5.5, Df=1.5e-3, n=1.530),
    "cordierite": dict(name="堇青石", E=140e9, nu=0.25, alpha=1.8e-6, k=4.0, Dk=4.8, Df=2e-4, n=1.540),
    "forsterite": dict(name="镁橄榄石", E=200e9, nu=0.24, alpha=9.8e-6, k=6.0, Dk=6.8, Df=1e-4, n=1.650),
    "bquartz":    dict(name="β-石英固溶体", E=95e9, nu=0.24, alpha=-0.5e-6, k=1.8, Dk=4.5, Df=3e-4, n=1.545),
}

def Kmod(E, nu): return E / (3 * (1 - 2 * nu))
def Gmod(E, nu): return E / (2 * (1 + nu))

def mori_tanaka(f, Ki, Gi, Km, Gm):
    """3-D Mori-Tanaka bulk/shear moduli for spherical inclusions (volume fraction f)."""
    K = Km + f * (Ki - Km) / (1 + (1 - f) * (Ki - Km) / (Km + 4 / 3 * Gm))
    zeta = Gm / 6 * (9 * Km + 8 * Gm) / (Km + 2 * Gm)
    G = Gm + f * (Gi - Gm) / (1 + (1 - f) * (Gi - Gm) / (Gm + zeta))
    return K, G

def hs_bounds_3d(f, Ki, Gi, Km, Gm):
    lo = mori_tanaka(f, Ki, Gi, Km, Gm)  # MT == HS lower when inclusion stiffer
    hi = mori_tanaka(1 - f, Km, Gm, Ki, Gi)
    return lo, hi

def levin_cte(f, a_i, a_m, K_i, K_m, K_eff):
    """Levin's exact relation for two-phase isotropic composite CTE."""
    return a_m + (a_i - a_m) * (1 / K_eff - 1 / K_m) / (1 / K_i - 1 / K_m)

def turner_cte(f, a_i, a_m, K_i, K_m):
    return (f * a_i * K_i + (1 - f) * a_m * K_m) / (f * K_i + (1 - f) * K_m)

def kerner_cte(f, a_i, a_m, K_i, K_m, G_m):
    """Kerner (1956): a = <a> + f(1-f)(a_i-a_m)(K_i-K_m)/[(1-f)K_i + f K_m + 3K_iK_m/(4G_m)]"""
    return f * a_i + (1 - f) * a_m + f * (1 - f) * (a_i - a_m) * (K_i - K_m) / ((1 - f) * K_i + f * K_m + 3 * K_i * K_m / (4 * G_m))

def maxwell_garnett(f, ei, em):
    """3-D Maxwell-Garnett / Maxwell-Eucken (complex permittivity or conductivity)."""
    return em * (ei + 2 * em + 2 * f * (ei - em)) / (ei + 2 * em - f * (ei - em))

def bruggeman(f, ei, em, d=3):
    """Symmetric Bruggeman EMA in d dimensions (complex allowed)."""
    B = f * ((d - 1) * ei - em) + (1 - f) * ((d - 1) * em - ei)
    disc = np.sqrt(B * B + 4 * (d - 1) * ei * em + 0j)
    r1 = (B + disc) / (2 * (d - 1)); r2 = (B - disc) / (2 * (d - 1))
    return np.where(np.real(r1) > 0, r1, r2)

def maxwell_garnett_2d(f, ei, em):
    """2-D (cylindrical inclusions) Maxwell-Garnett / Rayleigh formula."""
    return em * (ei + em + f * (ei - em)) / (ei + em - f * (ei - em))

def lichtenecker(f, ei, em):
    return np.exp(f * np.log(ei) + (1 - f) * np.log(em))

def gc_props(f, crystal="cordierite", glass="glass"):
    """Effective properties of a two-phase glass-ceramic at crystallinity f (vol. fraction)."""
    c, g = PHASE[crystal], PHASE[glass]
    Ki, Gi, Km, Gm = Kmod(c["E"], c["nu"]), Gmod(c["E"], c["nu"]), Kmod(g["E"], g["nu"]), Gmod(g["E"], g["nu"])
    K, G = mori_tanaka(f, Ki, Gi, Km, Gm)
    E = 9 * K * G / (3 * K + G); nu = (3 * K - 2 * G) / (2 * (3 * K + G))
    a = levin_cte(f, c["alpha"], g["alpha"], Ki, Km, K)
    k = maxwell_garnett(f, c["k"], g["k"])
    ec = c["Dk"] * (1 - 1j * c["Df"]); eg = g["Dk"] * (1 - 1j * g["Df"])
    e = maxwell_garnett(f, ec, eg)
    return dict(E=E, nu=nu, alpha=a, k=k, Dk=e.real, Df=-e.imag / e.real, K=K, G=G)
