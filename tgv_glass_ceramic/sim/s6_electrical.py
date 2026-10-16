"""S6: Dielectric homogenization and TGV high-frequency performance.
(a) 2-D RVE complex-permittivity FEM vs Maxwell-Garnett / Bruggeman / HS bounds (validation;
    identical PDE validates thermal-conductivity homogenization), then 3-D GC Dk/Df vs crystallinity
(b) TGV two-wire / GSG capacitance by 2-D electrostatic FEM vs exact two-wire formula (validation);
    50-ohm GSG design chart
(c) insertion loss per TGV and per-mm line loss to 220 GHz incl. sidewall roughness (Hammerstad vs
    Groiss), benchmark against published measurements"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from skfem import MeshTri, ElementTriP1, ElementTriP2, ElementTriP0, Basis, BilinearForm, asm, condense
from skfem.helpers import dot, grad
from common import MAT, PHASE, C, INK2, savefig, save_results, maxwell_garnett_2d, bruggeman, gc_props
import skrf as rf

RES = {}
eps0, mu0, c0 = 8.8541878128e-12, 4e-7 * np.pi, 299792458.0
rng = np.random.default_rng(3)

@BilinearForm
def lap(u, v, w): return dot(grad(u), grad(v))

@BilinearForm
def lap_w(u, v, w): return w.chi * dot(grad(u), grad(v))

def rsa_disks(f, n_target=60):
    r = np.sqrt(f / (np.pi * n_target)); cs = np.zeros((0, 2))
    tries = 0
    while len(cs) < n_target and tries < 400000:
        p = rng.random(2); tries += 1
        if len(cs):
            dx = np.abs(cs - p); dx = np.minimum(dx, 1 - dx)
            if np.min((dx ** 2).sum(1)) < (2.02 * r) ** 2: continue
        cs = np.vstack([cs, p])
    return cs, r

def rve_eps(f, ec, eg, N=256):
    """Finite-volume (pixel) RVE: unit potential drop in x, insulated y faces, harmonic-mean face
    conductances, complex permittivity. Independent of the FEM machinery used elsewhere."""
    cs, r = rsa_disks(f)
    xc = (np.arange(N) + 0.5) / N
    X, Y = np.meshgrid(xc, xc, indexing="ij")          # X along potential drop
    inc = np.zeros((N, N), bool)
    for q in cs:
        for sx in (-1, 0, 1):
            for sy in (-1, 0, 1):
                inc |= (X - q[0] - sx) ** 2 + (Y - q[1] - sy) ** 2 < r * r
    e = np.where(inc, ec, eg).astype(complex)
    idx = np.arange(N * N).reshape(N, N)
    rows, cols, vals = [], [], []
    diag = np.zeros(N * N, complex); rhs = np.zeros(N * N, complex)
    gx = 2 * e[:-1, :] * e[1:, :] / (e[:-1, :] + e[1:, :])
    gy = 2 * e[:, :-1] * e[:, 1:] / (e[:, :-1] + e[:, 1:])
    for g, a_, b_ in ((gx, idx[:-1, :], idx[1:, :]), (gy, idx[:, :-1], idx[:, 1:])):
        a_, b_, g = a_.ravel(), b_.ravel(), g.ravel()
        rows += [a_, b_]; cols += [b_, a_]; vals += [-g, -g]
        np.add.at(diag, a_, g); np.add.at(diag, b_, g)
    gl = 2 * e[0, :]; gr = 2 * e[-1, :]
    np.add.at(diag, idx[0, :], gl); np.add.at(diag, idx[-1, :], gr)
    rhs[idx[-1, :]] += gr * 1.0
    A = sp.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N * N, N * N)).tocsr() + sp.diags(diag)
    phi = spla.spsolve(A.tocsc(), rhs).reshape(N, N)
    I = np.sum(gr * (1.0 - phi[-1, :]))
    return I, inc.mean()

def part_a():
    c, g = PHASE["cordierite"], PHASE["glass"]
    ec = c["Dk"] * (1 - 1j * c["Df"]); eg = g["Dk"] * (1 - 1j * g["Df"])
    fs = [0.1, 0.2, 0.3, 0.4, 0.5]
    fem = []
    for f in fs:
        e, fa = rve_eps(f, ec, eg); fem.append((fa, e))
    fem = np.array(fem)
    ff = np.linspace(0, 0.55, 100)
    mg2 = maxwell_garnett_2d(ff, ec, eg); br2 = bruggeman(ff, ec, eg, d=2)
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.0))
    axs[0].plot(ff, mg2.real, color=C[0], label="2D Maxwell-Garnett (=HS 下界)")
    axs[0].plot(ff, br2.real, color=C[1], ls="--", label="2D Bruggeman")
    axs[0].plot(fem[:, 0].real, fem[:, 1].real, "o", mfc="white", mec=C[2], ms=8, label="RVE 有限体积（随机圆盘, 256²）")
    axs[0].set_xlabel("晶相面积分数 f"); axs[0].set_ylabel("ε'_eff"); axs[0].legend(fontsize=7.5)
    axs[0].set_title("验证13：复介电常数均匀化 Re")
    Df = lambda e: -e.imag / e.real
    axs[1].plot(ff, Df(mg2) * 1e3, color=C[0]); axs[1].plot(ff, Df(br2) * 1e3, color=C[1], ls="--")
    axs[1].plot(fem[:, 0].real, Df(fem[:, 1]) * 1e3, "o", mfc="white", mec=C[2], ms=8)
    axs[1].set_xlabel("晶相面积分数 f"); axs[1].set_ylabel("Df_eff (×10⁻³)"); axs[1].set_title("验证13：损耗角正切 Df")
    errs = np.abs(fem[:, 1] - maxwell_garnett_2d(fem[:, 0].real, ec, eg)) / np.abs(maxwell_garnett_2d(fem[:, 0].real, ec, eg))
    RES["rve_validation"] = dict(f=fem[:, 0].real, eps_fem=fem[:, 1], rel_err_vs_MG2D=errs)
    # 3-D predictions for designed glass-ceramics
    f3 = np.linspace(0, 0.8, 81)
    for i, cr in enumerate(["cordierite", "forsterite"]):
        p = [gc_props(x, cr) for x in f3]
        axs[2].plot(f3, [q["Df"] * 1e3 for q in p], color=C[i], label=f"{PHASE[cr]['name']}型 Df@10GHz (×10⁻³)")
        axs[2].plot(f3, [q["Dk"] for q in p], color=C[i], ls="--", label=f"{PHASE[cr]['name']}型 Dk")
    axs[2].set_xlabel("晶化率（体积）"); axs[2].set_ylabel("Dk  /  Df×10³"); axs[2].legend(fontsize=7.5)
    axs[2].set_title("3D Maxwell-Garnett：晶化率调控介电性能")
    savefig(fig, "s6_dielectric_homogenization.png")
    print("rve err", errs)

# ---------- (b) TGV capacitance ----------
def conductor_mesh(centers, rv, W, h_far):
    pts = []
    for (cx, cy) in centers:
        for k, rr in enumerate(rv * (1 + np.r_[0, np.geomspace(0.01, 6, 28)])):
            n = int(np.clip(2 * np.pi * rr / (rv * 0.06 * (1 + 0.6 * k)), 60, 260))
            th = np.linspace(0, 2 * np.pi, n, endpoint=False) + 0.5 * k
            pts.append(np.c_[cx + rr * np.cos(th), cy + rr * np.sin(th)])
    g = np.linspace(-W, W, int(2 * W / h_far) + 1); Gx, Gy = np.meshgrid(g, g)
    bg = np.c_[Gx.ravel(), Gy.ravel()]
    P = np.vstack(pts + [bg])
    keep = np.ones(len(P), bool)
    for (cx, cy) in centers:
        dd = np.hypot(P[:, 0] - cx, P[:, 1] - cy)
        keep &= dd > rv * (1 - 1e-9)
        keep &= ~((dd > rv * 1.0001) & (dd < rv * 1.5) & np.isin(np.arange(len(P)), np.arange(len(P) - len(bg), len(P))))
    P = P[keep]
    P = np.unique(np.round(P, 12), axis=0)
    T = Delaunay(P).simplices
    cen = P[T].mean(axis=1)
    ok = np.ones(len(T), bool)
    for (cx, cy) in centers:
        ok &= np.hypot(cen[:, 0] - cx, cen[:, 1] - cy) > rv
    return MeshTri(P.T.copy(), T[ok].T.copy())

def capacitance(centers, volts, rv, W):
    m = conductor_mesh(centers, rv, W, W / 30)
    basis = Basis(m, ElementTriP2(), intorder=4)
    K = asm(lap, basis).tocsr()
    u = np.zeros(basis.N); D = []
    for (cx, cy), V in zip(centers, volts):
        d = basis.get_dofs(lambda x: np.hypot(x[0] - cx, x[1] - cy) < rv * 1.0005).all()
        u[d] = V; D.append(d)
    D = np.unique(np.concatenate(D)); I = np.setdiff1d(np.arange(basis.N), D)
    u[I] = spla.spsolve(K[I][:, I].tocsc(), -K[I][:, D] @ u[D])
    return eps0 * (u @ (K @ u))            # = C V^2 (per unit length, eps_r = 1)

def part_b():
    rv = 25e-6; out = []
    for s_over_d in [1.5, 2.0, 3.0, 4.0, 6.0]:
        s = s_over_d * 2 * rv
        W = 12 * s
        We = capacitance([(-s / 2, 0), (s / 2, 0)], [0.5, -0.5], rv, W)    # V diff = 1
        C_fem = We; C_ex = np.pi * eps0 / np.arccosh(s / (2 * rv))
        out.append(dict(s_over_d=s_over_d, C_fem=C_fem, C_exact=C_ex, rel=abs(C_fem - C_ex) / C_ex))
    RES["twowire_validation"] = out
    print(out)
    # GSG impedance chart
    pd = np.linspace(1.6, 5, 12); Zs = {}
    for key in ["FS", "BG", "GCC", "GCF"]:
        Zs[key] = []
    Cg = []
    for r_ in pd:
        p = r_ * 2 * rv; W = 14 * p
        Cs = capacitance([(-p, 0), (0, 0), (p, 0)], [0, 1, 0], rv, W)
        Cg.append(Cs)
    Cg = np.array(Cg)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0))
    sd = np.array([o["s_over_d"] for o in out])
    axs[0].plot(np.linspace(1.3, 6.2, 100), np.pi / np.arccosh(np.linspace(1.3, 6.2, 100)), color=C[0], label="精确解 C=πε/arccosh(s/d)")
    axs[0].plot(sd, [o["C_fem"] / eps0 for o in out], "o", mfc="white", mec=C[1], ms=8, label="FEM（P2, Delaunay 网格）")
    axs[0].set_xlabel("中心距/直径 s/d"); axs[0].set_ylabel("C / ε₀ (单位长度)"); axs[0].legend(fontsize=8)
    axs[0].set_title(f"验证14：差分TGV对电容 FEM vs 解析（最大误差 {max(o['rel'] for o in out)*100:.2f}%）")
    for i, key in enumerate(["FS", "BG", "GCC", "GCF"]):
        er = MAT[key]["Dk"]; Z = np.sqrt(er) / (c0 * Cg * er)
        Zs[key] = Z
        axs[1].plot(pd, Z, color=C[i], label=f"{MAT[key]['name']} (Dk={er})")
    axs[1].axhline(50, color=INK2, ls="--", lw=1)
    axs[1].set_xlabel("GSG 节距/直径 p/d"); axs[1].set_ylabel("GSG TGV 特性阻抗 Z₀ (Ω)")
    axs[1].set_title("GSG 垂直互连阻抗设计图（d=50 µm）"); axs[1].legend(fontsize=7.5)
    savefig(fig, "s6_tgv_impedance.png")
    RES["gsg"] = dict(p_over_d=pd, C_air=Cg, Z={k: v.tolist() for k, v in Zs.items()})
    return pd, Cg

# ---------- (c) insertion loss ----------
def tand(f, key):
    d = MAT[key]; gam = {"FS": 0.3, "BG": 0.33, "GCC": 0.25, "GCF": 0.25, "ORG": 0.2}[key]   # calibrated: FS 2e-4->4e-4 (10->100 GHz); glass stack 0.012 @140 GHz; NEG GCC-2 2.45->40 GHz
    return d["Df"] * (f / 10e9) ** gam

def K_hammerstad(Rq, delta): return 1 + 2 / np.pi * np.arctan(1.4 * (Rq / delta) ** 2)
def K_groiss(Rq, delta): return 1 + np.exp(-(delta / (2 * Rq)) ** 1.6)

def via_line(f, key, Z0, Cair, L, d=50e-6, s_over_d=2.5, Rq=50e-9, model="H"):
    er = MAT[key]["Dk"]; rho = 1.8e-8
    Rs = np.sqrt(np.pi * f * mu0 * rho); delta = np.sqrt(rho / (np.pi * f * mu0))
    Kr = K_hammerstad(Rq, delta) if model == "H" else K_groiss(Rq, delta)
    prox = 1 / np.sqrt(1 - (1 / s_over_d) ** 2)
    Rp = Rs * Kr * prox * (1 / (np.pi * d) + 1 / (2 * np.pi * d))
    Lp = mu0 * eps0 / Cair                    # TEM external inductance
    Cp = Cair * er; Gp = 2 * np.pi * f * Cp * tand(f, key)
    w = 2 * np.pi * f
    Zc = np.sqrt((Rp + 1j * w * Lp) / (Gp + 1j * w * Cp)); gam = np.sqrt((Rp + 1j * w * Lp) * (Gp + 1j * w * Cp))
    return Zc, gam

def design_50ohm(key, pd, Cg):
    er = MAT[key]["Dk"]; Z = np.sqrt(er) / (c0 * Cg * er)
    if Z.min() <= 50 <= Z.max():
        p_sel = float(np.interp(50, Z, pd))
    else:
        p_sel = float(pd[np.argmin(np.abs(Z - 50))])
    C_sel = float(np.interp(p_sel, pd, Cg))
    return p_sel, C_sel

def part_c(pd, Cg):
    f = np.linspace(1e9, 220e9, 441)
    freq = rf.Frequency.from_f(f, unit="Hz")
    fig, axs = plt.subplots(1, 3, figsize=(14.5, 4.1))
    out = {}; diss = {}; design = {}
    for i, key in enumerate(["FS", "BG", "GCC", "GCF", "ORG"]):
        p_sel, Cair = design_50ohm(key, pd, Cg)
        design[key] = p_sel
        Zc, gam = via_line(f, key, None, Cair, 300e-6, s_over_d=p_sel, Rq=50e-9)
        med = rf.media.DefinedGammaZ0(frequency=freq, gamma=gam, z0=Zc, z0_port=50)
        ntw = med.line(300e-6, "m")
        s21 = np.abs(ntw.s[:, 1, 0]); s11 = np.abs(ntw.s[:, 0, 0])
        il = -20 * np.log10(s21); ds = -10 * np.log10(s21**2 / (1 - s11**2))
        out[key] = il; diss[key] = ds
        axs[0].plot(f / 1e9, ds, color=C[i], label=f"{MAT[key]['name']} (p/d={p_sel:.2f})")
    axs[0].set_xlabel("频率 (GHz)"); axs[0].set_ylabel("单个 GSG TGV 耗散损耗 (dB)")
    axs[0].set_title("50 Ω 匹配设计下单孔耗散损耗（t=300 µm, d=50 µm, Rq=50 nm）", fontsize=10); axs[0].legend(fontsize=7)
    for i, key in enumerate(["FS", "BG", "GCC", "GCF", "ORG"]):
        ad = 8.686 * np.pi * f * np.sqrt(MAT[key]["Dk"]) * tand(f, key) / c0 * 1e-3
        axs[1].plot(f / 1e9, ad, color=C[i], label=MAT[key]["name"])
    axs[1].set_xlabel("频率 (GHz)"); axs[1].set_ylabel("介质损耗 α_d (dB/mm)")
    axs[1].set_title("基板介质损耗（TEM 近似，含 tanδ 频散）"); axs[1].legend(fontsize=7.5)
    rqs = [25e-9, 60e-9, 150e-9, 500e-9, 1.26e-6]
    for i, rq in enumerate(rqs):
        delta = np.sqrt(1.8e-8 / (np.pi * f * mu0))
        axs[2].plot(f / 1e9, K_hammerstad(rq, delta), color=C[i], label=f"Rq={rq*1e9:.0f} nm")
        axs[2].plot(f / 1e9, K_groiss(rq, delta), color=C[i], ls=":", lw=1.3)
    axs[2].set_xlabel("频率 (GHz)"); axs[2].set_ylabel("导体损耗粗糙度因子 K_r")
    axs[2].set_title("验证15：两种粗糙度模型（实线 Hammerstad / 点线 Groiss）", fontsize=10); axs[2].legend(fontsize=7)
    savefig(fig, "s6_insertion_loss.png")
    p_bg, C_bg = design_50ohm("BG", pd, Cg)
    Zc, gam = via_line(np.array([28e9]), "BG", None, C_bg, 100e-6, s_over_d=p_bg, Rq=50e-9)
    med = rf.media.DefinedGammaZ0(frequency=rf.Frequency.from_f([28e9], unit="Hz"), gamma=gam, z0=Zc, z0_port=50)
    il28 = float(-20 * np.log10(np.abs(med.line(100e-6, "m").s[0, 1, 0])))
    RES["benchmark_28GHz_100um_BG_dB"] = il28
    idx = {fq: int(np.argmin(np.abs(f - fq * 1e9))) for fq in (28, 77, 140, 170, 220)}
    RES["il_per_via_dB"] = {k: {fq: float(v[i]) for fq, i in idx.items()} for k, v in out.items()}
    RES["diss_per_via_dB"] = {k: {fq: float(v[i]) for fq, i in idx.items()} for k, v in diss.items()}
    RES["design_p_over_d_50ohm"] = design
    delta140 = np.sqrt(1.8e-8 / (np.pi * 140e9 * mu0))
    RES["Kr_140GHz"] = {f"{rq*1e9:.0f}nm": dict(H=float(K_hammerstad(rq, delta140)), G=float(K_groiss(rq, delta140))) for rq in rqs}
    # line-level: dissipative loss of a 10 mm CPW-like TEM line on each substrate at 140 GHz incl. conductor loss
    RES["alpha_d_140_dB_per_mm"] = {k: float(8.686 * np.pi * 140e9 * np.sqrt(MAT[k]["Dk"]) * tand(140e9, k) / c0 * 1e-3) for k in ["FS", "BG", "GCC", "GCF", "ORG"]}
    print(RES["diss_per_via_dB"], design, il28, RES["alpha_d_140_dB_per_mm"])

if __name__ == "__main__":
    part_a()
    pd, Cg = part_b()
    part_c(pd, Cg)
    save_results("s6_electrical", RES)
