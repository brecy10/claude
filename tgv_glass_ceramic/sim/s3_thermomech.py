"""S3: Thermo-mechanical simulation of Cu-filled TGV in glass vs glass-ceramic.
(a) 3-way validation: GPS-Lame analytic / scikit-fem P2 / in-house Q4-Bbar
(b) elastoplastic anneal (25->400->25 C) + 2 thermal cycles (-55/125 C) for 4 substrates
(c) CTE/E parameter sweep, (d) stress-relief strategies incl. glass-ceramic phase collar"""
import sys, time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import tri as mtri
from common import MAT, SUBS, C, INK2, savefig, save_results, gc_props, PHASE
from fem_axi import AxiTGV, graded
from fem_skfem import axi_solve
from analytic_mech import lame_gps

RES = {}
a = 25e-6            # via radius (d = 50 um)
t_sub = 300e-6; h = t_sub / 2
pitch = 150e-6; Rcell = pitch / np.sqrt(np.pi)
PATH = [25, 400, 25, 125, -55, 125, -55, 25]
NSUB = 12

# ---------------- (a) validation ----------------
def validation():
    hv, Rv = 1000e-6, 250e-6
    dT = 375.0
    cu = dict(MAT["Cu"], sy0=1e12, sy400=1e12)
    m = AxiTGV(a, Rv, hv, nr_cu=16, nr_s=40, nz=40)
    m.set_materials(MAT["BG"], cu)
    m.run([25, 400], nsub=1, elastic=True)
    xy = m.gp_xy(); sel = xy[:, 1] < m.z[1]
    r_q4 = xy[sel, 0]; sq4 = {k: m.field(i)[sel] for k, i in (("sr", 0), ("sz", 1), ("st", 2))}
    rr = np.concatenate([graded(0, a, 12, 4.0), graded(a, Rv, 40, 1 / 40)[1:]]); zz = graded(0, hv, 30, 1.0)
    res = axi_solve(rr, zz, lambda c: (np.where(c[0] < a, MAT["Cu"]["E"], MAT["BG"]["E"]),
                                       np.where(c[0] < a, MAT["Cu"]["nu"], MAT["BG"]["nu"]),
                                       np.where(c[0] < a, MAT["Cu"]["alpha"], MAT["BG"]["alpha"])), dT)
    x = res["x"]; s2 = res["sig"]; sel2 = x[1] < 60e-6
    r_p2 = x[0][sel2]; sp2 = {k: s2[k][sel2] for k in ("sr", "st", "sz")}
    r_an = np.linspace(1e-7, 120e-6, 600); an = lame_gps(a, Rv, MAT["Cu"], MAT["BG"], dT, r_an)
    err = {}
    for k in ("sr", "st", "sz"):
        e_q4 = np.abs(sq4[k] - lame_gps(a, Rv, MAT["Cu"], MAT["BG"], dT, r_q4)[k])
        e_p2 = np.abs(sp2[k] - lame_gps(a, Rv, MAT["Cu"], MAT["BG"], dT, r_p2)[k])
        ref = np.abs(an[k]).max()
        err[k] = dict(q4_max_rel=float(e_q4.max() / ref), p2_max_rel=float(e_p2.max() / ref))
    fig, ax = plt.subplots(1, 1, figsize=(6.4, 4.0))
    labels = {"sr": "σ_r 径向", "st": "σ_θ 环向", "sz": "σ_z 轴向"}
    for i, k in enumerate(("sr", "st", "sz")):
        ax.plot(r_an * 1e6, an[k] / 1e6, color=C[i], lw=2, label=f"{labels[k]}  解析(GPS-Lamé)")
        o = np.argsort(r_p2); idx = o[:: max(1, len(o) // 45)]
        ax.plot(r_p2[idx] * 1e6, sp2[k][idx] / 1e6, "o", mfc="white", mec=C[i], ms=5, label="scikit-fem P2" if i == 0 else None)
        o = np.argsort(r_q4); idx = o[:: max(1, len(o) // 30)]
        ax.plot(r_q4[idx] * 1e6, sq4[k][idx] / 1e6, "x", color=C[i], ms=6, label="自编 Q4-Bbar" if i == 0 else None)
    ax.axvline(a * 1e6, color=INK2, lw=1, ls="--"); ax.text(a * 1e6 + 1.5, -480, "Cu/基板界面", color=INK2, fontsize=9)
    ax.set_xlim(0, 120); ax.set_xlabel("半径 r (µm)"); ax.set_ylabel("应力 (MPa)")
    ax.set_title("验证1：中面应力 — 解析解 vs 两套独立FEM（BG基板，ΔT=+375 K，弹性）")
    ax.legend(fontsize=8, ncol=1, loc="center right", bbox_to_anchor=(1.0, 0.33))
    savefig(fig, "s3_validation_lame_fem.png")
    RES["validation"] = err
    print("validation", err)

# ---------------- (b) elastoplastic histories ----------------
def principal_max(sig):
    sr, sz, st, srz = sig[..., 0], sig[..., 1], sig[..., 2], sig[..., 3]
    c = (sr + sz) / 2; rad = np.sqrt(((sr - sz) / 2) ** 2 + srz ** 2)
    return np.maximum(c + rad, st)

def make_model(sub, liner=None, collar=None, poly=None, tied=True, R=None):
    m = AxiTGV(a, R if R else Rcell, h, nr_cu=16, nr_s=30, nz=40, tied_outer=tied, liner=liner)
    m.set_materials(sub, MAT["Cu"], collar=collar, poly_liner=poly)
    return m

def recorder(m, T):
    sub = ~np.repeat(m.is_cu, 4)
    sig = m.sig.reshape(-1, 4)
    xy = m.gp_xy()
    ring = sub & (xy[:, 0] < a + 1.5e-6)
    u = m.node_u(); top = m.idx[:, -1]
    s1 = principal_max(sig)
    mid = ring & (xy[:, 1] < 30e-6)
    return dict(T=T, st_max=sig[sub, 2].max(), st_mid=sig[mid, 2].mean(), sr_int_max=sig[ring, 0].max(),
                s1_max=s1[sub].max(), protr=u[top[0], 1] - u[top[-1], 1], pacc=m.pacc.max())

def histories():
    out = {}
    fields = {}
    for key in SUBS:
        t0 = time.time()
        m = make_model(MAT[key])
        hist = m.run(PATH, nsub=NSUB, record=recorder)
        out[key] = {k: np.array([hh[k] for hh in hist]) for k in hist[0]}
        print(key, "done", round(time.time() - t0, 1), "s")
    # field snapshot at 400 C (end of heating) for BG and GCF
    for key in ("BG", "GCF"):
        m = make_model(MAT[key]); m.run([25, 400], nsub=NSUB)
        fields[key] = dict(xy=m.gp_xy().copy(), st=m.field(2).copy(), s1=principal_max(m.sig.reshape(-1, 4)), peq=np.repeat(m.pacc, 1).reshape(-1))
    return out, fields

def plot_histories(out, fields):
    nseg = len(PATH) - 1
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.9))
    steps = np.arange(len(out["BG"]["T"]))
    for i, key in enumerate(SUBS):
        o = out[key]
        axs[0].plot(steps, o["st_mid"] / 1e6, color=C[i], label=MAT[key]["name"])
        axs[1].plot(steps, o["sr_int_max"] / 1e6, color=C[i])
        axs[2].plot(steps, o["protr"] * 1e6, color=C[i])
    for ax in axs:
        for j in range(1, nseg):
            ax.axvline(j * NSUB - 0.5, color="#c9c8c2", lw=0.6)
        ax.set_xlabel("载荷步（退火25→400→25 °C；TC −55/125 °C ×2）")
    axs[0].set_ylabel("中面界面环向应力 σθ (MPa)"); axs[0].set_title("径向裂纹驱动力（升温阶段最大）")
    axs[1].set_ylabel("界面最大径向应力 σr (MPa)"); axs[1].set_title("界面分层驱动力（降温后为拉应力）")
    axs[2].set_ylabel("Cu 凸出量 (µm)"); axs[2].set_title("Cu protrusion（相对基板表面）")
    axs[0].legend(fontsize=8, loc="upper right")
    fig.suptitle("弹塑性有限元：退火与热循环全过程应力演化（d=50 µm, t=300 µm, pitch=150 µm）", y=1.02)
    savefig(fig, "s3_history_elastoplastic.png")
    if fields is None:
        return
    # field contour
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
    lv = np.linspace(-400, 400, 33)
    for ax, key in zip(axs, ("BG", "GCF")):
        f = fields[key]; xy = f["xy"]
        msk = (xy[:, 0] < 80e-6) & (xy[:, 1] > h - 110e-6)
        tr = mtri.Triangulation(xy[msk, 0] * 1e6, (xy[msk, 1] - h) * 1e6)
        cs = ax.tricontourf(tr, np.clip(f["st"][msk] / 1e6, -400, 400), levels=lv, cmap="RdBu_r")
        ax.axvline(a * 1e6, color="k", lw=0.8, ls="--")
        ax.set_title(f"{MAT[key]['name']}：400 °C 时 σθ")
        ax.set_xlabel("r (µm)"); ax.grid(False)
    axs[0].set_ylabel("z − 表面 (µm)")
    fig.colorbar(cs, ax=axs, label="σθ (MPa)", shrink=0.9)
    savefig(fig, "s3_field_hoop_400C.png")

# ---------------- (c) parametric sweep (analytic + FEM spot checks) ----------------
def cte_sweep():
    al = np.linspace(0.5e-6, 12e-6, 40)
    res = {}
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.0))
    for j, E in enumerate([70e9, 100e9, 150e9]):
        st_heat = []; sr_cool = []
        for x in al:
            sub = dict(E=E, nu=0.23, alpha=x)
            st_heat.append(lame_gps(a, Rcell, MAT["Cu"], sub, 375, np.array([a * 1.0001]))["st"][0])
        axs[0].plot(al * 1e6, np.array(st_heat) / 1e6, color=C[j], label=f"解析(弹性) E={E/1e9:.0f} GPa")
        res[f"E{E/1e9:.0f}"] = dict(alpha=al, st_heat=np.array(st_heat))
    # FEM elastoplastic spot checks at E=100 GPa
    pts = []
    for x in [0.5e-6, 3.5e-6, 7.5e-6, 10e-6]:
        m = make_model(dict(E=100e9, nu=0.23, alpha=x))
        hist = m.run([25, 400, 25], nsub=NSUB, record=recorder)
        stm = max(hh["st_mid"] for hh in hist); srr = hist[-1]["sr_int_max"]; pr = hist[-1]["protr"]
        pts.append((x, stm, srr, pr))
    pts = np.array(pts)
    axs[0].plot(pts[:, 0] * 1e6, pts[:, 1] / 1e6, "s", color=C[1], mfc="white", ms=8, label="弹塑性FEM (E=100 GPa)")
    axs[0].set_xlabel("基板 CTE (ppm/K)"); axs[0].set_ylabel("400 °C 时界面环向应力 σθ (MPa)")
    axs[0].set_title("CTE 越高 → 环向拉应力越低"); axs[0].legend(fontsize=8)
    axs[1].plot(pts[:, 0] * 1e6, pts[:, 2] / 1e6, "o-", color=C[0], label="退火后界面残余径向拉应力")
    axs[1].plot(pts[:, 0] * 1e6, pts[:, 3] * 1e6 * 100, "s--", color=C[2], label="残余Cu凸出 ×100 (µm)")
    axs[1].set_xlabel("基板 CTE (ppm/K)"); axs[1].set_ylabel("MPa  /  µm×100"); axs[1].legend(fontsize=8)
    axs[1].set_title("弹塑性FEM：退火后残余量")
    savefig(fig, "s3_sweep_cte.png")
    RES["cte_sweep_fem"] = pts.tolist()

# ---------------- (d) stress-relief strategies ----------------
def strategies():
    gcf = MAT["GCF"]
    glassy = PHASE["glass"]
    w = 5e-6
    def collar_glassy(r):
        sel = (r >= a) & (r < a + w)
        return np.where(sel, glassy["E"], np.nan), np.where(sel, glassy["alpha"], np.nan)
    def collar_graded(r):
        s = np.clip((r - a) / w, 0, 1); sel = (r >= a) & (r < a + w)
        Ein, ain = 160e9, 9.8e-6 * 0.85 + 0.15 * 4e-6     # forsterite-rich collar (~85 vol%)
        return np.where(sel, Ein + (gcf["E"] - Ein) * s, np.nan), np.where(sel, ain + (gcf["alpha"] - ain) * s, np.nan)
    def collar_soft(r):
        s = np.clip((r - a) / w, 0, 1); sel = (r >= a) & (r < a + w)
        Ein, ain = 50e9, 9.0e-6                       # porous/soft high-CTE graded shell (target design)
        return np.where(sel, Ein + (gcf["E"] - Ein) * s, np.nan), np.where(sel, ain + (gcf["alpha"] - ain) * s, np.nan)
    cases = [
        ("BG 实心Cu(基准)", dict(sub=MAT["BG"])),
        ("GC-F 实心Cu", dict(sub=gcf)),
        ("GC-F + 2µm聚合物衬层", dict(sub=gcf, poly=(2e-6, MAT["POLY"]))),
        ("GC-F 共形Cu 8µm", dict(sub=gcf, liner=8e-6)),
        ("GC-F + 玻璃相环(激光非晶化)", dict(sub=gcf, collar=collar_glassy)),
        ("GC-F + 富晶梯度环(激光晶化)", dict(sub=gcf, collar=collar_graded)),
        ("GC-F + 低模量高CTE梯度环", dict(sub=gcf, collar=collar_soft)),
    ]
    out = []
    for name, kw in cases:
        m = make_model(kw["sub"], liner=kw.get("liner"), collar=kw.get("collar"), poly=kw.get("poly"))
        hist = m.run([25, 400, 25], nsub=NSUB, record=recorder)
        out.append(dict(name=name, st_heat=max(hh["st_max"] for hh in hist), st_mid=max(hh["st_mid"] for hh in hist),
                        s1_heat=max(hh["s1_max"] for hh in hist), sr_res=hist[-1]["sr_int_max"], protr_res=hist[-1]["protr"],
                        protr_max=max(hh["protr"] for hh in hist)))
        print(name, {k: (round(v / 1e6, 1) if "s" in k[:2] else v) for k, v in out[-1].items() if k != "name"})
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.3), sharey=True)
    names = [o["name"] for o in out]; y = np.arange(len(out))
    for ax, key, lab, col in zip(axs, ["st_mid", "sr_res", "protr_max"],
                                 ["400 °C 中面界面 σθ (MPa)", "退火后界面残余 σr (MPa)", "最大 Cu 凸出 (µm)"], [C[0], C[1], C[2]]):
        vals = np.array([o[key] for o in out]) * (1e-6 if key != "protr_max" else 1e6)
        ax.barh(y, vals, color=col, height=0.6)
        for yy, v in zip(y, vals):
            ax.text(v, yy, f" {v:.1f}" if key != "protr_max" else f" {v:.2f}", va="center", fontsize=8, color=INK2)
        ax.set_xlabel(lab); ax.grid(axis="y", visible=False)
    axs[0].set_yticks(y); axs[0].set_yticklabels(names); axs[0].invert_yaxis()
    fig.suptitle("应力缓释策略对比（弹塑性FEM，退火 25→400→25 °C）", y=1.01)
    savefig(fig, "s3_strategies.png")
    RES["strategies"] = out

def collar_map():
    """Design map: collar (5 um graded interphase) modulus x CTE -> peak hoop stress (elastoplastic heating to 400 C)."""
    gcf = MAT["GCF"]; w = 5e-6
    Es = np.array([20, 40, 60, 80, 105, 140]) * 1e9; als = np.array([4, 7.5, 10, 13, 16]) * 1e-6
    Z = np.zeros((len(als), len(Es))); Zr = np.zeros_like(Z)
    for i, ac in enumerate(als):
        for j, Ec in enumerate(Es):
            def col(r, Ec=Ec, ac=ac):
                s_ = np.clip((r - a) / w, 0, 1); sel = (r >= a) & (r < a + w)
                return np.where(sel, Ec + (gcf["E"] - Ec) * s_, np.nan), np.where(sel, ac + (gcf["alpha"] - ac) * s_, np.nan)
            m = make_model(gcf, collar=col)
            hist = m.run([25, 400, 25], nsub=8, record=recorder)
            Z[i, j] = max(hh["st_mid"] for hh in hist) / 1e6; Zr[i, j] = hist[-1]["sr_int_max"] / 1e6
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0))
    for ax, D, lab in ((axs[0], Z, "400 °C 中面界面 σθ (MPa)"), (axs[1], Zr, "退火后界面残余 σr (MPa)")):
        cs = ax.contourf(Es / 1e9, als * 1e6, D, levels=12, cmap="Blues")
        cl = ax.contour(Es / 1e9, als * 1e6, D, levels=6, colors="k", linewidths=0.6); ax.clabel(cl, fmt="%.0f", fontsize=7)
        fig.colorbar(cs, ax=ax, label=lab)
        ax.plot(gcf["E"] / 1e9, gcf["alpha"] * 1e6, "o", color=C[1], mec="white", ms=9); ax.annotate("无环(GC-F本体)", (gcf["E"] / 1e9, gcf["alpha"] * 1e6), xytext=(-60, 8), textcoords="offset points", fontsize=8)
        ax.set_xlabel("相环内侧模量 E_c (GPa)"); ax.set_ylabel("相环内侧 CTE α_c (ppm/K)"); ax.grid(False)
    axs[0].set_title("相环设计图：低模量+高CTE 可大幅降低环向应力")
    axs[1].set_title("相环设计图：界面残余径向应力")
    savefig(fig, "s3_collar_map.png")
    RES["collar_map"] = dict(E=Es, alpha=als, st_mid=Z, sr_res=Zr)

def replot_histories():
    import json
    d = json.load(open("../results/s3_thermomech.json"))
    out = {k: {kk: np.array(vv) for kk, vv in v.items()} for k, v in d["histories"].items()}
    plot_histories(out, None)

if __name__ == "__main__":
    validation()
    out, fields = histories()
    plot_histories(out, fields)
    RES["histories"] = {k: {kk: vv.tolist() for kk, vv in v.items()} for k, v in out.items()}
    summ = {}
    for k in SUBS:
        o = out[k]; nA = 2 * NSUB
        cyc = slice(nA + 2 * NSUB, nA + 4 * NSUB)   # second TC cycle (125->-55->125)
        summ[k] = dict(st_mid_max=float(o["st_mid"].max()), st_max=float(o["st_max"].max()), s1_max=float(o["s1_max"].max()),
                       sr_res_after_anneal=float(o["sr_int_max"][nA - 1]), protr_400=float(o["protr"][NSUB - 1]),
                       protr_res=float(o["protr"][nA - 1]),
                       dpacc_cycle=float(o["pacc"][nA + 4 * NSUB - 1] - o["pacc"][nA + 2 * NSUB - 1]))
    RES["summary"] = summ
    print(summ)
    cte_sweep()
    strategies()
    save_results("s3_thermomech", RES)
    collar_map()
    save_results("s3_thermomech", RES)
