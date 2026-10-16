"""S5: Heat spreading in glass / glass-ceramic substrates with thermal TGV arrays.
(a) exact orthotropic Fourier-Bessel series (flux channel with convective base) vs axisymmetric
    P2 FEM (validation); (b) hotspot temperature vs Cu via fraction for each substrate;
(c) thermal-mechanical co-design Pareto (hotspot temperature vs via hoop stress)."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j0, j1, jn_zeros
from skfem import MeshTri, ElementTriP2, Basis, FacetBasis, BilinearForm, LinearForm, asm, solve
from common import MAT, C, INK2, savefig, save_results
from fem_axi import graded
from analytic_mech import lame_gps

RES = {}
a_s, b_c, t_c, P, h = 2.5e-3, 10e-3, 0.4e-3, 5.0, 5e3

def k_eff(ks, phi, kcu=390.0):
    kz = (1 - phi) * ks + phi * kcu
    kr = ks * ((kcu + ks) + phi * (kcu - ks)) / ((kcu + ks) - phi * (kcu - ks))   # 2-D Maxwell (cylinders)
    return kr, kz

def series(kr, kz, a=a_s, b=b_c, t=t_c, P=P, h=h, N=400):
    q0 = P / (np.pi * a**2)
    lam = jn_zeros(1, N) / b
    th0 = q0 * a**2 / b**2 * (1 / h + t / kz)
    qn = 2 * q0 * a * j1(lam * a) / (lam * b**2 * j0(lam * b) ** 2)
    mu = lam * np.sqrt(kr / kz)
    # stable form: c*(cosh(mu t) + h/(kz mu) sinh(mu t)) = qn*(1 + h/(kz mu) tanh)/(kz mu tanh + h)
    tt = np.tanh(mu * t)
    top = qn * (1 + h / (kz * mu) * tt) / (kz * mu * tt + h)
    Tmean = th0 + np.sum(top * 2 * j1(lam * a) / (lam * a))
    Tmax = th0 + np.sum(top)
    return Tmax, Tmean

def fem(kr, kz, a=a_s, b=b_c, t=t_c, P=P, h=h):
    r = np.unique(np.r_[graded(0, a, 30, 1.0), graded(a, b, 50, 1 / 8)]); z = np.linspace(0, t, 13)
    m = MeshTri.init_tensor(r, z)
    e = ElementTriP2(); basis = Basis(m, e, intorder=4)
    @BilinearForm
    def cond(u, v, w): return (kr * u.grad[0] * v.grad[0] + kz * u.grad[1] * v.grad[1]) * w.x[0]
    fb_bot = FacetBasis(m, e, facets=m.facets_satisfying(lambda x: np.isclose(x[1], 0)), intorder=4)
    fb_top = FacetBasis(m, e, facets=m.facets_satisfying(lambda x: np.isclose(x[1], t) & (x[0] <= a + 1e-12)), intorder=4)
    @BilinearForm
    def robin(u, v, w): return h * u * v * w.x[0]
    q0 = P / (np.pi * a**2)
    @LinearForm
    def flux(v, w): return q0 * v * w.x[0]
    A = asm(cond, basis) + asm(robin, fb_bot); bvec = asm(flux, fb_top)
    u = solve(A, bvec)
    top = basis.get_dofs(lambda x: np.isclose(x[1], t)).all()
    xt = basis.doflocs[0, top]
    return u[top][np.argmin(xt)], (xt, u[top])

def main():
    # (a) validation
    val = []
    for key in ["BG", "GCF"]:
        for phi in [0.0, 0.1]:
            kr, kz = k_eff(MAT[key]["k"], phi)
            Ts, _ = series(kr, kz); Tf, prof = fem(kr, kz)
            val.append(dict(sub=key, phi=phi, T_series=Ts, T_fem=Tf, rel=abs(Tf - Ts) / Ts))
    RES["validation"] = val
    print(val)
    # (b) hotspot temperature vs phi
    phis = np.linspace(0, 0.25, 26)
    fig, axs = plt.subplots(1, 2, figsize=(11.8, 4.1))
    out = {}
    for i, key in enumerate(["ORG", "BG", "FS", "GCC", "GCF"]):
        Tm = [series(*k_eff(MAT[key]["k"], p))[0] for p in phis]
        out[key] = Tm
        axs[0].plot(phis * 100, Tm, color=C[i], label=MAT[key]["name"])
    for p_ in [0.0, 0.1, 0.2]:
        kr, kz = k_eff(MAT["BG"]["k"], p_); axs[0].plot(p_ * 100, fem(kr, kz)[0], "o", mfc="white", mec=INK2, ms=7)
        kr, kz = k_eff(MAT["GCF"]["k"], p_); axs[0].plot(p_ * 100, fem(kr, kz)[0], "s", mfc="white", mec=INK2, ms=7)
    axs[0].set_yscale("log"); axs[0].set_xlabel("热通孔 Cu 面积分数 φ (%)"); axs[0].set_ylabel("热点最高温升 ΔT_max (K)")
    axs[0].set_title("验证12：Fourier–Bessel 级数(线) vs FEM(点)；5 W/Ø5 mm 热点"); axs[0].legend(fontsize=7.5)
    RES["Tmax_vs_phi"] = dict(phi=phis, **out)
    # (c) co-design: hoop stress (Lame unit cell, d=50 um, heating dT=+100 K service) vs Tmax
    d = 50e-6
    for i, key in enumerate(["BG", "GCC", "GCF"]):
        st, Tm = [], []
        for p_ in phis[1:]:
            R = d / 2 / np.sqrt(p_)
            st.append(lame_gps(d / 2, R, MAT["Cu"], MAT[key], 100.0, np.array([d / 2 * 1.0001]))["st"][0] / 1e6)
            Tm.append(series(*k_eff(MAT[key]["k"], p_))[0])
        axs[1].plot(Tm, np.array(st) / (MAT[key]["KIC"] / 1e6), "o-", color=C[i + 1], ms=3, label=f"{MAT[key]['name']}")
    axs[1].set_xscale("log"); axs[1].set_xlabel("热点最高温升 ΔT_max (K)"); axs[1].set_ylabel("σθ(100 K 工况) / K_IC  (MPa / MPa·m$^{1/2}$)")
    axs[1].set_title("热-力协同 Pareto：越靠左下越优（φ 增大沿曲线向左）"); axs[1].legend(fontsize=7.5)
    savefig(fig, "s5_thermal.png")

if __name__ == "__main__":
    main()
    save_results("s5_thermal", RES)
