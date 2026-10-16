"""S3c: Closing the fracture-mechanics loop.
(1) Griffith check: center crack in a uniform (thermally generated) biaxial stress field,
    FEM energy-release rate vs exact K = s0 sqrt(pi c)  -> validates the FEM energy method
(2) free hole + crack-face loading (superposition), FEM crack-opening displacement vs weight function
    -> validates the weight-function (WF) approximation for an empty/debonded hole
(3) bonded Cu core: FEM energy vs FEM COD  -> reveals the core-constraint (shielding) effect"""
import time
import numpy as np
import matplotlib.pyplot as plt
from skfem import MeshTri, ElementVector, ElementTriP2, Basis, FacetBasis, LinearForm, asm, solve, condense
from common import MAT, C, INK2, savefig, save_results
from fem_skfem import ps_stiff, ps_therm, lame_coefs, p0_field
from analytic_mech import lame_gps, K_edge_crack_wf

RES = {}

def polar(r_start, rs_extra, n_th=80, full=False):
    rs = np.asarray(rs_extra)
    th = np.pi * np.linspace(0, 1, n_th + 1)
    th = np.pi * (0.5 - 0.5 * np.cos(np.pi * np.linspace(0, 1, n_th + 1)))   # refine near both crack lines (0 and pi)
    P = [] if r_start > 0 else [[0.0, 0.0]]
    for r in rs: P += [[r * np.cos(t), r * np.sin(t)] for t in th]
    P = np.array(P); nt = n_th + 1; T = []
    off = 0 if r_start > 0 else 1
    if r_start == 0:
        for j in range(n_th): T.append([0, 1 + j, 2 + j])
    for i in range(len(rs) - 1):
        b0 = off + i * nt; b1 = off + (i + 1) * nt
        for j in range(n_th):
            T.append([b0 + j, b1 + j, b1 + j + 1]); T.append([b0 + j, b1 + j + 1, b0 + j + 1])
    return MeshTri(P.T.copy(), np.array(T).T.copy())

def K_cod(basis, u, tip_x, c, Ep, direction=-1):
    """COD extrapolation on the upper crack face behind the tip (direction=-1: face lies at x<tip)."""
    d = basis.get_dofs(lambda x: np.isclose(x[1], 0.0))
    yn = d.nodal["u^2"]; xn = basis.doflocs[0, yn]
    s = (tip_x - xn) * (-direction)
    sel = (s > 0.03 * c) & (s < 0.2 * c)
    Ks = u[yn[sel]] * Ep / 4 * np.sqrt(2 * np.pi / s[sel])
    p = np.polyfit(s[sel], Ks, 1)
    return p[1]

def griffith():
    sub = MAT["BG"]; ring = dict(E=sub["E"], nu=sub["nu"], alpha=sub["alpha"] + 4e-6)
    R1, R2 = 200e-6, 600e-6; dT = 150.0           # ring expands more on heating -> uniform biaxial tension in disk
    s0 = lame_gps(R1, R2, sub, ring, dT, np.array([1e-7]), mode="pstrain")["st"][0]
    cs = np.linspace(4e-6, 20e-6, 9)
    rs = np.r_[np.linspace(0, 30e-6, 241)[1:], np.linspace(30e-6, R1, 30)[1:], np.linspace(R1, R2, 15)[1:]]
    m = polar(0, rs, n_th=80)
    basis = Basis(m, ElementVector(ElementTriP2()), intorder=4)
    cen = m.p[:, m.t].mean(axis=1); isr = np.hypot(*cen) > R1
    E = np.where(isr, ring["E"], sub["E"]); nu = np.where(isr, ring["nu"], sub["nu"]); al = np.where(isr, ring["alpha"], sub["alpha"])
    lam, G, K = lame_coefs(E, nu)
    fw = dict(lam=p0_field(basis, lam), G=p0_field(basis, G), K=p0_field(basis, K), alpha=p0_field(basis, al), dT=dT)
    A = asm(ps_stiff, basis, **fw); b = asm(ps_therm, basis, **fw)
    d = basis.get_dofs(lambda x: np.isclose(x[1], 0.0)); yn, yf = d.nodal["u^2"], d.facet["u^2"]
    xn, xf = basis.doflocs[0, yn], basis.doflocs[0, yf]
    ux0 = basis.get_dofs(lambda x: np.isclose(x[0], 0) & np.isclose(x[1], 0)).nodal["u^1"]
    Pi, Kc = [], []
    Ep = sub["E"] / (1 - sub["nu"] ** 2)
    for c in cs:
        crk = lambda x: np.abs(x) < c - 1e-12
        D = np.concatenate([yn[~crk(xn)], yf[~crk(xf)], ux0])
        u = solve(*condense(A, b, D=D)); Pi.append(2 * (0.5 * u @ (A @ u) - u @ b))
        Kc.append(K_cod(basis, u, c, c, Ep))
    Pi = np.array(Pi); Gt = -0.5 * np.gradient(Pi, cs)       # two tips
    K_en = np.sqrt(np.maximum(Gt, 0) * Ep); K_ex = s0 * np.sqrt(np.pi * cs)
    RES["griffith"] = dict(c=cs, K_energy=K_en, K_cod=Kc, K_exact=K_ex, s0=s0,
                          err_energy=float(np.median(np.abs(K_en - K_ex) / K_ex)), err_cod=float(np.median(np.abs(np.array(Kc) - K_ex) / K_ex)))
    print("griffith", RES["griffith"]["err_energy"], RES["griffith"]["err_cod"], "s0", s0 / 1e6)

def hole_and_core():
    sub = MAT["BG"]; a = 25e-6; dT = 375.0; Rout = 12 * a
    Ep = sub["E"] / (1 - sub["nu"] ** 2)
    sig_line = lambda x: lame_gps(a, Rout, MAT["Cu"], sub, dT, a + np.asarray(x), mode="pstrain")["st"]
    cs = np.array([2.5, 5, 7.5, 10, 12.5, 15, 20, 25]) * 1e-6
    # (2) free hole, crack-face traction = uncracked hoop stress
    rs = np.r_[np.linspace(a, a + 40e-6, 201), (a + 40e-6) + (Rout - a - 40e-6) * (np.geomspace(1, 41, 20)[1:] - 1) / 40]
    mh = polar(a, rs, n_th=80)
    bh = Basis(mh, ElementVector(ElementTriP2()), intorder=4)
    lam, G, K = lame_coefs(np.full(mh.t.shape[1], sub["E"]), np.full(mh.t.shape[1], sub["nu"]))
    fwh = dict(lam=p0_field(bh, lam), G=p0_field(bh, G))
    Ah = asm(ps_stiff, bh, **fwh)
    d = bh.get_dofs(lambda x: np.isclose(x[1], 0.0)); yn, yf = d.nodal["u^2"], d.facet["u^2"]
    xn, xf = bh.doflocs[0, yn], bh.doflocs[0, yf]
    uxR = bh.get_dofs(lambda x: np.isclose(x[0], Rout) & np.isclose(x[1], 0)).nodal["u^1"]
    K_hole = []
    for c in cs:
        fb = FacetBasis(mh, ElementVector(ElementTriP2()), facets=mh.facets_satisfying(lambda x: np.isclose(x[1], 0) & (x[0] > a) & (x[0] < a + c)), intorder=6)
        @LinearForm
        def trac(v, w):
            return sig_line(w.x[0].ravel() - a).reshape(w.x[0].shape) * v.value[1]
        f = asm(trac, fb)
        crk = lambda x: (x > a - 1e-12) & (x < a + c - 1e-12)
        D = np.concatenate([yn[~crk(xn)], yf[~crk(xf)], uxR])
        u = solve(*condense(Ah, f, D=D))
        K_hole.append(K_cod(bh, u, a + c, c, Ep))
    K_wf = np.array([K_edge_crack_wf(sig_line, c) for c in cs])
    # (3) bonded core: COD on the thermal model
    rs2 = np.r_[a * np.linspace(0.15, 1, 10), np.linspace(a, a + 40e-6, 201)[1:], (a + 40e-6) + (Rout - a - 40e-6) * (np.geomspace(1, 41, 20)[1:] - 1) / 40]
    mc = polar(0, rs2, n_th=80)
    bc = Basis(mc, ElementVector(ElementTriP2()), intorder=4)
    cen = mc.p[:, mc.t].mean(axis=1); isc = np.hypot(*cen) < a
    cu = MAT["Cu"]
    E = np.where(isc, cu["E"], sub["E"]); nu = np.where(isc, cu["nu"], sub["nu"]); al = np.where(isc, cu["alpha"], sub["alpha"])
    lam, G, K = lame_coefs(E, nu)
    fw = dict(lam=p0_field(bc, lam), G=p0_field(bc, G), K=p0_field(bc, K), alpha=p0_field(bc, al), dT=dT)
    A = asm(ps_stiff, bc, **fw); b = asm(ps_therm, bc, **fw)
    d = bc.get_dofs(lambda x: np.isclose(x[1], 0.0)); yn, yf = d.nodal["u^2"], d.facet["u^2"]
    xn, xf = bc.doflocs[0, yn], bc.doflocs[0, yf]
    ux0 = bc.get_dofs(lambda x: np.isclose(x[0], 0) & np.isclose(x[1], 0)).nodal["u^1"]
    K_core_cod, Pi = [], []
    for c in cs:
        crk = lambda x: (x > a + 1e-12) & (x < a + c - 1e-12)
        D = np.concatenate([yn[~crk(xn)], yf[~crk(xf)], ux0])
        u = solve(*condense(A, b, D=D)); Pi.append(2 * (0.5 * u @ (A @ u) - u @ b))
        K_core_cod.append(K_cod(bc, u, a + c, c, Ep))
    K_core_en = np.sqrt(np.maximum(-np.gradient(np.array(Pi), cs), 0) * Ep)
    RES["hole_core"] = dict(c=cs, K_wf=K_wf, K_hole_cod=K_hole, K_core_cod=K_core_cod, K_core_energy=K_core_en,
                            err_wf_vs_hole=float(np.median(np.abs(K_wf - np.array(K_hole)) / np.array(K_hole))),
                            ratio_core_to_hole=float(np.median(np.array(K_core_cod) / np.array(K_hole))))
    print("hole/core", RES["hole_core"]["err_wf_vs_hole"], RES["hole_core"]["ratio_core_to_hole"])

def plot():
    g = RES["griffith"]; h = RES["hole_core"]
    fig, axs = plt.subplots(1, 2, figsize=(11.8, 4.2))
    axs[0].plot(np.array(g["c"]) * 1e6, np.array(g["K_exact"]) / 1e6, color=C[0], label="Griffith 精确解 σ₀√(πc)")
    axs[0].plot(np.array(g["c"]) * 1e6, np.array(g["K_energy"]) / 1e6, "o", mfc="white", mec=C[1], label=f"FEM 能量法 (中位误差 {g['err_energy']*100:.1f}%)")
    axs[0].plot(np.array(g["c"]) * 1e6, np.array(g["K_cod"]) / 1e6, "x", color=C[2], label=f"FEM 张开位移法 (中位误差 {g['err_cod']*100:.1f}%)")
    axs[0].set_xlabel("半裂纹长 c (µm)"); axs[0].set_ylabel("K_I (MPa·m$^{1/2}$)"); axs[0].legend(fontsize=8)
    axs[0].set_title("验证2a：FEM 断裂算法基准（均匀双轴应力）")
    c = np.array(h["c"]) * 1e6
    axs[1].plot(c, np.array(h["K_wf"]) / 1e6, color=C[0], label="权函数（自由孔/界面脱粘）")
    axs[1].plot(c, np.array(h["K_hole_cod"]) / 1e6, "o", mfc="white", mec=C[0], label=f"FEM 自由孔+裂面载荷 (与权函数差 {h['err_wf_vs_hole']*100:.0f}%)")
    axs[1].plot(c, np.array(h["K_core_cod"]) / 1e6, "s-", color=C[1], mfc="white", label="FEM 粘结Cu芯（张开位移法）")
    axs[1].plot(c, np.array(h["K_core_energy"]) / 1e6, "x", color=C[1], label="FEM 粘结Cu芯（能量法）")
    for kk, col, lab in [(0.75, C[7], "玻璃 K_IC"), (2.0, C[5], "微晶玻璃 K_IC")]:
        axs[1].axhline(kk, color=col, ls="--", lw=1); axs[1].text(c[-1], kk + 0.04, lab, color=col, fontsize=8, ha="right")
    axs[1].set_xlabel("裂纹长度 c (µm)"); axs[1].set_ylabel("K_I (MPa·m$^{1/2}$)")
    axs[1].set_title(f"验证2b：界面粘结使 K 降至脱粘情形的 {h['ratio_core_to_hole']*100:.0f}%"); axs[1].legend(fontsize=7.5, loc="lower right")
    savefig(fig, "s3c_fracture_closedloop.png")

if __name__ == "__main__":
    t = time.time(); griffith(); print("t", time.time() - t)
    hole_and_core(); print("t", time.time() - t)
    plot()
    save_results("s3c_fracture_check", RES)
