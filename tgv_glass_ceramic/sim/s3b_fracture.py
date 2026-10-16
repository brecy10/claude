"""S3b/S9: Fracture mechanics of radial cracks at TGVs + Weibull weakest-link reliability.
Closed loop: K from (i) FEM energy release rate (scikit-fem P2, plane strain, crack opened by
releasing symmetry constraints) vs (ii) edge-crack weight function on the Lame crack-line stress."""
import time
import numpy as np
import matplotlib.pyplot as plt
from skfem import MeshTri, ElementVector, ElementTriP2, Basis, asm, solve, condense
from common import MAT, SUBS, C, INK2, savefig, save_results
from fem_skfem import ps_stiff, ps_therm, lame_coefs, p0_field
from analytic_mech import lame_gps, K_edge_crack_wf
from fem_axi import AxiTGV

RES = {}

def polar_mesh(a, Rout, cmax, n_cr=160, n_th=90):
    r_core = a * np.linspace(0.15, 1.0, 10)
    r_cr = a + np.linspace(0, 1.6 * cmax, n_cr + 1)[1:]
    r_out = a + 1.6 * cmax + (Rout - a - 1.6 * cmax) * (np.geomspace(1, 41, 26)[1:] - 1) / 40
    rs = np.r_[r_core, r_cr, r_out]
    th = np.pi * (np.linspace(0, 1, n_th + 1)) ** 2
    P = [[0.0, 0.0]]
    for r in rs:
        P += [[r * np.cos(t), r * np.sin(t)] for t in th]
    P = np.array(P)
    nt = n_th + 1
    T = []
    for j in range(n_th):                  # center fan
        T.append([0, 1 + j, 1 + j + 1])
    for i in range(len(rs) - 1):
        b0 = 1 + i * nt; b1 = 1 + (i + 1) * nt
        for j in range(n_th):
            p00, p01, p10, p11 = b0 + j, b0 + j + 1, b1 + j, b1 + j + 1
            T.append([p00, p10, p11]); T.append([p00, p11, p01])
    return MeshTri(P.T.copy(), np.array(T).T.copy())

def crack_G(a, sub, dT, c_list, Rout=None):
    Rout = Rout or 12 * a
    cmax = max(c_list)
    m = polar_mesh(a, Rout, cmax)
    basis = Basis(m, ElementVector(ElementTriP2()), intorder=4)
    cen = m.p[:, m.t].mean(axis=1); rr = np.hypot(*cen); isc = rr < a
    cu = MAT["Cu"]
    E = np.where(isc, cu["E"], sub["E"]); nu = np.where(isc, cu["nu"], sub["nu"]); al = np.where(isc, cu["alpha"], sub["alpha"])
    lam, G, K = lame_coefs(E, nu)
    fw = dict(lam=p0_field(basis, lam), G=p0_field(basis, G), K=p0_field(basis, K), alpha=p0_field(basis, al), dT=dT)
    A = asm(ps_stiff, basis, **fw); b = asm(ps_therm, basis, **fw)
    dy = basis.get_dofs(lambda x: np.isclose(x[1], 0.0, atol=1e-12))
    yn, yf = dy.nodal["u^2"], dy.facet["u^2"]
    xn, xf = basis.doflocs[0, yn], basis.doflocs[0, yf]
    ux0 = basis.get_dofs(lambda x: np.isclose(x[0], 0.0) & np.isclose(x[1], 0.0)).nodal["u^1"]
    Pi = []
    for c in c_list:
        crk = lambda x: (x > a + 1e-12) & (x < a + c - 1e-12)
        D = np.concatenate([yn[~crk(xn)], yf[~crk(xf)], ux0])
        u = solve(*condense(A, b, D=D))
        Pi.append(2 * (0.5 * u @ (A @ u) - u @ b))
    Pi = np.array(Pi)
    Gc = -np.gradient(Pi, c_list)
    return Gc, m.p.shape[1]

def validation():
    sub = MAT["BG"]; a = 25e-6; dT = 375.0
    c_list = np.linspace(0.0, 30e-6, 31)
    t0 = time.time()
    Gc, nn = crack_G(a, sub, dT, c_list)
    print("crack FEM time", time.time() - t0, "nodes", nn)
    Ep = sub["E"] / (1 - sub["nu"] ** 2)
    K_fem = np.sqrt(np.maximum(Gc, 0) * Ep)
    Rout = 12 * a
    def sig_line(x):
        return lame_gps(a, Rout, MAT["Cu"], sub, dT, a + x, mode="pstrain")["st"]
    K_wf = np.array([K_edge_crack_wf(sig_line, c) if c > 0 else 0 for c in c_list])
    s0 = sig_line(np.array([1e-9]))[0]
    sel = (c_list > 0.5e-6) & (c_list < c_list[-1] - 0.5e-6)
    rel = np.abs(K_fem[sel] - K_wf[sel]) / K_wf[sel]
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.plot(c_list[1:] / a, K_wf[1:] / 1e6, color=C[0], label="权函数解析（Tada 边裂纹格林函数 + Lamé 场）")
    ax.plot(c_list[sel] / a, K_fem[sel] / 1e6, "o", mfc="white", mec=C[1], label="FEM 能量释放率 G→K (scikit-fem P2)")
    for kk, col, lab in [(0.75, C[7], "玻璃 K_IC≈0.75"), (2.0, C[5], "微晶玻璃 K_IC≈2.0")]:
        ax.axhline(kk, color=col, ls="--", lw=1.2); ax.text(1.02, kk + 0.03, lab, color=col, fontsize=8, ha="right")
    ax.set_xlabel("裂纹长度 c / 通孔半径 a"); ax.set_ylabel("K_I (MPa·m$^{1/2}$)")
    ax.set_title(f"验证2：TGV 径向裂纹 K — FEM vs 解析（BG, d=50 µm, ΔT=+375 K）")
    ax.legend(fontsize=8, loc="lower right")
    savefig(fig, "s3b_fracture_validation.png")
    RES["validation"] = dict(c=c_list, K_fem=K_fem, K_wf=K_wf, s0=s0, rel_err_median=float(np.median(rel)), rel_err_max=float(rel.max()))
    print("fracture validation median rel err", np.median(rel), "max", rel.max())

def Fmax():
    """Dimensionless max of K/(s0 sqrt(a)) over crack length for hoop field s0 (a/r)^2."""
    a = 1.0
    cs = np.linspace(1e-3, 3, 600)
    F = np.array([K_edge_crack_wf(lambda x: (a / (a + x)) ** 2, c) for c in cs])
    i = np.argmax(F)
    return F[i], cs[i], cs, F

def design_map():
    Fm, cpk, cs, F = Fmax()
    RES["Fmax"] = dict(Fmax=Fm, c_at_max=cpk)
    print("Fmax", Fm, "at c/a", cpk)
    dTs = np.linspace(50, 450, 81)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.2))
    axs[0].plot(cs, F, color=C[0]); axs[0].axvline(cpk, color=INK2, ls=":")
    axs[0].set_xlabel("c / a"); axs[0].set_ylabel("K / (σ₀√a)"); axs[0].set_title(f"衰减场中 K 存在极大值 F_max={Fm:.2f} (c≈{cpk:.2f}a)")
    out = {}
    for i, key in enumerate(SUBS):
        sub = MAT[key]
        dc = []
        for dT in dTs:
            s0 = lame_gps(25e-6, 25e-6 * 6, MAT["Cu"], sub, dT, np.array([25e-6 * 1.0001]))["st"][0]
            dcrit = 2 * (sub["KIC"] / (Fm * s0)) ** 2 if s0 > 0 else np.inf
            dc.append(dcrit)
        dc = np.array(dc)
        out[key] = dc
        axs[1].semilogy(dTs + 25, np.clip(dc * 1e6, 1, 1e5), color=C[i], label=MAT[key]["name"])
    axs[1].axhspan(10, 100, color="#eef4fc", zorder=0)
    axs[1].text(60, 13, "主流TGV直径区间 10–100 µm", color=INK2, fontsize=8)
    axs[1].set_xlabel("退火/峰值温度 (°C)"); axs[1].set_ylabel("无裂纹临界直径 d_c (µm)")
    axs[1].set_title("断裂力学设计图：d < d_c 时任何径向裂纹均止裂"); axs[1].legend(fontsize=8)
    axs[1].set_ylim(1, 1e5)
    savefig(fig, "s3b_crack_design_map.png")
    RES["design_map"] = dict(T=dTs + 25, **{k: v for k, v in out.items()})
    # scalar summary at 400 C
    j = np.argmin(np.abs(dTs - 375))
    RES["dcrit_400C_um"] = {k: float(out[k][j] * 1e6) for k in SUBS}
    print("d_crit at 400C (um):", RES["dcrit_400C_um"])

def weibull():
    """Surface weakest-link on the via wall using elastoplastic FEM hoop stress at 400 C."""
    a = 25e-6; h = 150e-6; R = 150e-6 / np.sqrt(np.pi)
    A0 = 1e-6  # 1 mm^2 reference area
    res = {}
    params = {"FS": (8, 250e6), "BG": (8, 250e6), "GCC": (15, 400e6), "GCF": (15, 400e6)}
    Ts = [150, 250, 300, 350, 400]
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for i, key in enumerate(SUBS):
        m_w, s0w = params[key]
        pf = []
        for T in Ts:
            mdl = AxiTGV(a, R, h, nr_cu=16, nr_s=30, nz=40, tied_outer=True)
            mdl.set_materials(MAT[key], MAT["Cu"])
            mdl.run([25, T], nsub=8)
            xy = mdl.gp_xy(); sig = mdl.sig.reshape(-1, 4)
            # first GP ring in substrate adjacent to wall: hoop stress -> wall surface integral
            ring = (~np.repeat(mdl.is_cu, 4)) & (xy[:, 0] < a + 0.3e-6)
            zr = xy[ring, 1]; st = np.maximum(sig[ring, 2], 0)
            o = np.argsort(zr); zr, st = zr[o], st[o]
            dA = 2 * np.pi * a * np.gradient(zr) * 2   # both halves (symmetric)
            risk = np.sum((st / s0w) ** m_w * dA) / A0
            pf.append(1 - np.exp(-risk))
        pf = np.array(pf); res[key] = pf
        ax.semilogy(Ts, np.clip(pf, 1e-16, 1), "o-", color=C[i], label=f"{MAT[key]['name']} (m={m_w}, σ₀={s0w/1e6:.0f} MPa)")
    ax.axhline(1e-6, color=INK2, ls="--", lw=1); ax.text(152, 1.5e-6, "单孔 1 ppm（10⁶ 孔/面板 ≈ 63% 面板失效）", fontsize=8, color=INK2)
    ax.set_xlabel("峰值温度 (°C)"); ax.set_ylabel("单孔孔壁断裂概率 P_f")
    ax.set_title("验证3：Weibull 最弱链统计（弹塑性 FEM 应力场）"); ax.legend(fontsize=7.5)
    ax.set_ylim(1e-16, 1)
    savefig(fig, "s9_weibull.png")
    RES["weibull"] = dict(T=Ts, params={k: list(v) for k, v in params.items()}, pf={k: v.tolist() for k, v in res.items()})

if __name__ == "__main__":
    validation()
    design_map()
    weibull()
    save_results("s3b_fracture", RES)
