"""S8: Microstructural residual stress in glass-ceramics and the transparency-toughness paradox.
(a) Selsing analytic vs axisymmetric FEM of a spherical crystal in glass (validation)
(b) interface/hoop stress vs crystal-to-glass CTE ratio; Davidge-Green spontaneous microcracking size
(c) transparency (S1 Mie) vs toughness (phenomenological) vs crystal size -> route selection"""
import numpy as np
import matplotlib.pyplot as plt
from common import C, INK2, PHASE, savefig, save_results
from fem_skfem import axi_solve
from fem_axi import graded
import miepython

RES = {}
Ts = 750.0           # stress-free temperature ~ residual-glass Tg (C)
dT = 25.0 - Ts

def selsing(p_mat, m_mat, dT):
    """radial interface stress (positive = tension) for sphere p in infinite matrix m."""
    return (m_mat["alpha"] - p_mat["alpha"]) * dT / ((1 + m_mat["nu"]) / (2 * m_mat["E"]) + (1 - 2 * p_mat["nu"]) / p_mat["E"])

def part_a():
    g = PHASE["glass"]; out = {}
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.1))
    for i, cname in enumerate(["cordierite", "forsterite"]):
        p = PHASE[cname]; R = 1.0e-6; L = 25 * R
        r = np.concatenate([graded(0, R, 30, 3.0), graded(R, L, 60, 1 / 60)[1:]]); z = r.copy()
        def mats(c):
            inside = np.hypot(c[0], c[1]) < R
            return (np.where(inside, p["E"], g["E"]), np.where(inside, p["nu"], g["nu"]), np.where(inside, p["alpha"], g["alpha"]))
        res = axi_solve(r, z, mats, dT)
        x = res["x"]; s = res["sig"]
        # radial line along z=small (equatorial plane): sigma_r = sr, hoop = st
        sel = x[1] < 0.03 * R
        rr = x[0][sel]
        P = selsing(p, g, dT)
        an_r = np.where(rr < R, P, P * (R / rr) ** 3); an_t = np.where(rr < R, P, -P / 2 * (R / rr) ** 3)
        o = np.argsort(rr)
        axs[i].plot(rr[o] / R, an_r[o] / 1e6, color=C[0], label="Selsing 解析 σ_r")
        axs[i].plot(rr[o] / R, an_t[o] / 1e6, color=C[1], label="Selsing 解析 σ_θ")
        k = o[:: max(1, len(o) // 60)]
        axs[i].plot(rr[k] / R, s["sr"][sel][k] / 1e6, "o", ms=4, mfc="white", mec=C[0], label="轴对称 FEM σ_r")
        axs[i].plot(rr[k] / R, s["st"][sel][k] / 1e6, "s", ms=4, mfc="white", mec=C[1], label="轴对称 FEM σ_θ")
        axs[i].set_xlim(0, 4); axs[i].set_xlabel("r / R（晶粒半径）"); axs[i].set_ylabel("应力 (MPa)")
        nm = PHASE[cname]["name"]
        axs[i].set_title(f"验证10：{nm}晶粒/残余玻璃（冷却 {Ts:.0f}→25 °C）")
        axs[i].legend(fontsize=7.5)
        far = (rr > 1.3 * R) & (rr < 3 * R)
        err = np.median(np.abs(s["sr"][sel][far] - an_r[far]) / np.abs(an_r[far]))
        out[cname] = dict(P_selsing=P, fem_err_matrix=float(err))
    savefig(fig, "s8_selsing_validation.png")
    RES["selsing"] = out
    print(out)

def part_b():
    g = PHASE["glass"]
    ratio = np.linspace(0.0, 4.0, 81)
    Kg = 0.75e6; Ep = g["E"] / (1 - g["nu"] ** 2); gam = Kg**2 / (2 * Ep)
    P, Rc = [], []
    for r_ in ratio:
        p = dict(E=150e9, nu=0.25, alpha=r_ * g["alpha"])
        Pp = selsing(p, g, dT); P.append(Pp)
        fac = (1 + g["nu"]) / g["E"] + 2 * (1 - 2 * p["nu"]) / p["E"]
        Rc.append(4 * gam / (Pp**2 * fac) if abs(Pp) > 1 else np.inf)
    P = np.array(P); Rc = np.array(Rc)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0))
    axs[0].plot(ratio, P / 1e6, color=C[0], label="界面径向应力 σ_r(R)（>0 拉，界面脱粘风险）")
    axs[0].plot(ratio, -P / 2 / 1e6, color=C[1], label="基体环向应力 σ_θ(R)（>0 拉，基体径向微裂）")
    axs[0].axhline(0, color=INK2, lw=0.8)
    axs[0].axvspan(2, 4, color="#eef4fc", zorder=0); axs[0].text(2.1, -350, "NEG 专利区间 α_c/α_g=2–8", fontsize=8, color=INK2)
    for nm_, rr_ in [("堇青石", PHASE["cordierite"]["alpha"] / g["alpha"]), ("镁橄榄石", PHASE["forsterite"]["alpha"] / g["alpha"])]:
        axs[0].axvline(rr_, color="#c9c8c2", lw=1); axs[0].text(rr_ + 0.03, 300, nm_, fontsize=8, color=INK2)
    axs[0].set_xlabel("晶相/玻璃相 CTE 比 α_c/α_g"); axs[0].set_ylabel("应力 (MPa)"); axs[0].legend(fontsize=7.5, loc="lower left")
    axs[0].set_title("晶-玻 CTE 失配的残余应力符号反转")
    axs[1].semilogy(ratio, np.clip(2 * Rc * 1e6, 1e-1, 1e4), color=C[2])
    axs[1].axhspan(0.01, 0.2, color="#e6f4ea", zorder=0); axs[1].text(0.1, 0.12, "纳米晶区（透明）", fontsize=8, color="#0b6b0b")
    axs[1].set_ylim(0.1, 1e4)
    axs[1].set_xlabel("α_c/α_g"); axs[1].set_ylabel("自发微裂临界晶粒直径 (µm)")
    axs[1].set_title("Davidge–Green 能量判据：d > d_c 自发微裂")
    savefig(fig, "s8_mismatch_microcrack.png")
    RES["mismatch"] = dict(ratio=ratio, P=P, dcrit_um=2 * Rc * 1e6)
    i1 = np.argmin(np.abs(ratio - PHASE["forsterite"]["alpha"] / g["alpha"])); i2 = np.argmin(np.abs(ratio - PHASE["cordierite"]["alpha"] / g["alpha"]))
    RES["dcrit_forsterite_um"] = float(2 * Rc[i1] * 1e6); RES["dcrit_cordierite_um"] = float(2 * Rc[i2] * 1e6)
    print("dcrit forsterite", RES["dcrit_forsterite_um"], "cordierite", RES["dcrit_cordierite_um"])

def part_c():
    ds = np.geomspace(10e-9, 10e-6, 200)
    Kg, Kmax, f, fref, d0 = 0.8, 3.1, 0.6, 0.8, 1.27e-6
    KIC = Kg + (Kmax - Kg) * f / fref * (1 - np.exp(-ds / d0))
    nm = PHASE["glass"]["n"]; lam = 1030e-9; L = 500e-6
    def T(d, npr):
        x = np.pi * d * nm / lam; Q = miepython.efficiencies_mx(npr / nm, x)[1]
        return np.exp(-3 * f * Q / (2 * d) * L)
    Tf = np.array([T(d, PHASE["forsterite"]["n"]) for d in ds]); Tc = np.array([T(d, PHASE["cordierite"]["n"]) for d in ds])
    fig, axs = plt.subplots(2, 1, figsize=(7.0, 5.6), sharex=True)
    axs[0].semilogx(ds * 1e9, Tc, color=C[0], label="堇青石型 (Δn≈0.01)"); axs[0].semilogx(ds * 1e9, Tf, color=C[1], label="镁橄榄石型 (Δn≈0.12)")
    axs[0].axhline(0.9, color=INK2, ls="--", lw=1); axs[0].set_ylabel("500 µm 弹道透过率"); axs[0].legend(fontsize=8)
    axs[0].set_title("“透明–韧性”悖论：激光加工要纳米晶，增韧要微米晶")
    axs[1].semilogx(ds * 1e9, KIC, color=C[2], label="K_IC 唯象模型（锚点：Zerodur 0.9；LS2 3.05）")
    axs[1].plot([65], [0.9], "o", color=C[2]); axs[1].annotate("Zerodur", (65, 0.9), xytext=(5, 5), textcoords="offset points", fontsize=8)
    axs[1].plot([3000], [Kg + (Kmax - Kg) * 0.8 / fref * (1 - np.exp(-3e-6 / d0))], "o", color=C[2])
    axs[1].annotate("LS2 (80%)", (3000, 2.9), xytext=(5, -12), textcoords="offset points", fontsize=8)
    axs[1].axhline(2.0, color=C[5], ls="--", lw=1); axs[1].text(12, 2.05, "目标 K_IC ≥ 2.0", fontsize=8, color=C[5])
    axs[1].axvspan(10, 150, color="#eef4fc", zorder=0); axs[1].axvspan(1500, 10000, color="#e6f4ea", zorder=0)
    axs[1].text(14, 2.6, "阶段A：成孔态（纳米晶）", fontsize=8, color=INK2); axs[1].text(1600, 1.2, "阶段B：晶化长大后", fontsize=8, color="#0b6b0b")
    axs[1].set_xlabel("晶粒直径 d (nm)"); axs[1].set_ylabel("K_IC (MPa·m$^{1/2}$)"); axs[1].legend(fontsize=7.5, loc="upper left")
    savefig(fig, "s8_paradox.png")
    RES["paradox"] = dict(d_nm=ds * 1e9, T_forsterite=Tf, T_cordierite=Tc, KIC=KIC)

if __name__ == "__main__":
    part_a(); part_b(); part_c()
    save_results("s8_microstructure", RES)
