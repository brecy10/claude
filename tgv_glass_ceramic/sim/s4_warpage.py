"""S4: Substrate warpage (CLT vs axisymmetric P2 FEM) and the CTE-matching dilemma
(multi-objective analysis of core CTE: via cracking, die-level C4, board-level BGA, warpage)."""
import numpy as np
import matplotlib.pyplot as plt
from skfem import MeshTri, ElementTriP2, ElementVector, Basis, asm, solve, condense
from common import MAT, C, INK2, SEQ, savefig, save_results
from fem_skfem import axi_stiff, axi_therm, lame_coefs, p0_field
from fem_axi import graded
from analytic_mech import lame_gps, K_edge_crack_wf

RES = {}
ABF, CU = MAT["ABF"], MAT["Cu"]
fcu = 0.25
BU = dict(E=fcu * CU["E"] + (1 - fcu) * ABF["E"], nu=0.31)
BU["alpha"] = (fcu * CU["E"] * CU["alpha"] + (1 - fcu) * ABF["E"] * ABF["alpha"]) / BU["E"]
dT_lam = -(190 - 25)

def stack(core, tc=400e-6, ttop=120e-6, tbot=40e-6):
    return [(tbot, BU), (tc, core), (ttop, BU)]

def clt(layers, dT):
    z = np.concatenate([[0], np.cumsum([t for t, _ in layers])]); z = z - z[-1] / 2
    A = B = D = NT = MT = 0.0
    for (t, m), z0, z1 in zip(layers, z[:-1], z[1:]):
        M = m["E"] / (1 - m["nu"])
        A += M * (z1 - z0); B += M * (z1**2 - z0**2) / 2; D += M * (z1**3 - z0**3) / 3
        NT += M * m["alpha"] * dT * (z1 - z0); MT += M * m["alpha"] * dT * (z1**2 - z0**2) / 2
    e0, k = np.linalg.solve([[A, B], [B, D]], [NT, MT])
    return e0, k

def fem_disk(layers, dT, Rd=6e-3):
    zs = [0.0]; mats = []
    for t, m in layers:
        n = 4
        zs += list(zs[-1] + np.linspace(0, t, n + 1)[1:]); mats.append((zs[-1] - t, zs[-1], m))
    z = np.array(zs); r = graded(0, Rd, 60, 1.0)
    mesh = MeshTri.init_tensor(r, z)
    basis = Basis(mesh, ElementVector(ElementTriP2()), intorder=4)
    cen = mesh.p[:, mesh.t].mean(axis=1)
    E = np.zeros(cen.shape[1]); nu = np.zeros_like(E); al = np.zeros_like(E)
    for z0, z1, m in mats:
        s = (cen[1] >= z0) & (cen[1] <= z1); E[s] = m["E"]; nu[s] = m["nu"]; al[s] = m["alpha"]
    lam, G, K = lame_coefs(E, nu)
    fw = dict(lam=p0_field(basis, lam), G=p0_field(basis, G), K=p0_field(basis, K), alpha=p0_field(basis, al), dT=dT)
    A = asm(axi_stiff, basis, **fw); b = asm(axi_therm, basis, **fw)
    D = np.concatenate([basis.get_dofs(lambda x: np.isclose(x[0], 0)).all("u^1"),
                        basis.get_dofs(lambda x: np.isclose(x[0], 0) & np.isclose(x[1], 0)).nodal["u^2"]])
    u = solve(*condense(A, b, D=D))
    zmid = z[-1] / 2
    nd = basis.get_dofs(lambda x: np.isclose(x[1], z[np.argmin(np.abs(z - zmid))])).nodal["u^2"]
    rr = basis.doflocs[0, nd]; uz = u[nd]
    sel = rr < 0.5 * Rd
    k = np.polyfit(rr[sel] ** 2, uz[sel], 1)[0] * 2
    return k, rr, uz

def warpage_validation():
    out = []
    names = ["BG", "GCC", "GCF", "ORG"]
    for key in names:
        L = stack(MAT[key])
        e0, k_clt = clt(L, dT_lam)
        k_fem, rr, uz = fem_disk(L, dT_lam)
        out.append(dict(core=key, k_clt=k_clt, k_fem=k_fem, err=abs(abs(k_fem) - abs(k_clt)) / abs(k_clt), e0=e0 / dT_lam))
        print(key, k_clt, k_fem, out[-1]["err"], "alpha_eff", e0 / dT_lam)
    RES["validation"] = out
    # sweep core modulus & thickness for warpage over 50 mm body (center-to-corner)
    Ls = 50e-3; half_diag = Ls / np.sqrt(2)
    tcs = np.linspace(200e-6, 1200e-6, 26)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0))
    for i, key in enumerate(names):
        w = [abs(clt(stack(MAT[key], tc=t), dT_lam)[1]) * half_diag**2 / 2 * 1e6 for t in tcs]
        axs[0].plot(tcs * 1e6, w, color=C[i], label=MAT[key]["name"])
        fe = [abs(fem_disk(stack(MAT[key], tc=t), dT_lam)[0]) * half_diag**2 / 2 * 1e6 for t in (300e-6, 700e-6, 1100e-6)]
        axs[0].plot([300, 700, 1100], fe, "o", mfc="white", mec=C[i], ms=7)
    axs[0].set_yscale("log"); axs[0].set_xlabel("芯板厚度 (µm)"); axs[0].set_ylabel("50 mm 封装体翘曲 (µm, 中心-角)")
    axs[0].set_title("验证4：非对称积层翘曲 — 层合板理论(线) vs 轴对称FEM(圈)"); axs[0].legend(fontsize=8)
    # modulus-CTE map at tc = 400 um
    Es = np.linspace(20e9, 160e9, 50); als = np.linspace(1e-6, 13e-6, 50)
    W = np.array([[abs(clt(stack(dict(E=E, nu=0.24, alpha=a)), dT_lam)[1]) * half_diag**2 / 2 * 1e6 for E in Es] for a in als])
    cs = axs[1].contourf(Es / 1e9, als * 1e6, W, levels=[0, 25, 50, 75, 100, 150, 200, 300, 400, 600], cmap="Blues")
    fig.colorbar(cs, ax=axs[1], label="翘曲 (µm)")
    for i, key in enumerate(names):
        axs[1].plot(MAT[key]["E"] / 1e9, MAT[key]["alpha"] * 1e6, "o", color=C[i], mec="white", ms=9)
        axs[1].annotate(key, (MAT[key]["E"] / 1e9, MAT[key]["alpha"] * 1e6), xytext=(5, 5), textcoords="offset points", fontsize=8)
    axs[1].set_xlabel("芯板杨氏模量 E (GPa)"); axs[1].set_ylabel("芯板 CTE (ppm/K)"); axs[1].set_title("翘曲设计图（芯板 400 µm，3+1 非对称积层）")
    axs[1].grid(False)
    savefig(fig, "s4_warpage.png")

def cte_dilemma():
    """Feasible design region in (core CTE, package body size) for glass vs glass-ceramic cores.
    Constraints (assumptions listed in report Table 6-x):
      die level : chip-package-interaction mismatch |a_eff - a_Si| <= 50 % of organic-core baseline
      board level: BGA h 0.4 mm, board-level underfill/corner-bond factor 0.2, 0/100 C, DNP = 0.707 B,
                   Engelmaier N >= 1000
      TGV crack : K_max = beta*F_max*sigma_theta*sqrt(a) < K_IC, d = 50 um, anneal 350 C,
                  F_max = 0.885 (WF); beta = 1 (locally debonded, worst case; bonded beta~0.5 dashed)
      warpage   : 3+3 build-up with Cu imbalance (30%/20%), lamination dT = -125 K, w(B) <= 0.0035*B (JEITA-like)"""
    al = np.linspace(1e-6, 13e-6, 121); Bs = np.linspace(10e-3, 80e-3, 71)
    a_si, a_pcb = 2.6e-6, 17e-6
    gmax = 0.65 * (2 * 1000) ** (-0.45)         # Engelmaier: N = 0.5 (dg/(2 ef))^(1/c) >= 1000, ef=0.325, c=-0.45
    def bu(fcu):
        E = fcu * CU["E"] + (1 - fcu) * ABF["E"]
        return dict(E=E, nu=0.31, alpha=(fcu * CU["E"] * CU["alpha"] + (1 - fcu) * ABF["E"] * ABF["alpha"]) / E)
    res = {}
    aeff = []; kap = []; Kmax = []
    for x in al:
        core = dict(E=105e9, nu=0.24, alpha=x)
        L = [(90e-6, bu(0.20)), (400e-6, core), (90e-6, bu(0.30))]
        e0, k = clt(L, -125.0)
        aeff.append(e0 / -125.0); kap.append(abs(k))
        s0 = lame_gps(25e-6, 150e-6, CU, core, 325, np.array([25.0001e-6]))["st"][0]
        Kmax.append(1.0 * 0.885 * s0 * np.sqrt(25e-6))
    aeff, kap, Kmax = map(np.array, (aeff, kap, Kmax))
    org = clt([(90e-6, bu(0.20)), (400e-6, MAT["ORG"]), (90e-6, bu(0.30))], -125.0)[0] / -125.0
    die_ok = np.abs(aeff - a_si) <= 0.5 * (org - a_si)
    RES["organic_aeff"] = float(org)
    feas = {}
    for name, KIC in (("glass", 0.75e6), ("gc", 2.0e6)):
        F = np.zeros((len(Bs), len(al)), int)
        for i, B in enumerate(Bs):
            bl_ok = (a_pcb - aeff) * 0.2 * 100 * 0.707 * B / 0.4e-3 <= gmax
            warp_ok = kap * (0.707 * B) ** 2 / 2 <= 0.0035 * B
            crack_ok = Kmax <= KIC
            F[i] = die_ok.astype(int) + bl_ok + warp_ok + crack_ok
        feas[name] = F
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.3), sharey=True)
    cmap = plt.matplotlib.colors.ListedColormap(["#f3d3d3", "#f7e3c4", "#fbf1c7", "#dbeefc", "#bfe5c6"])
    for ax, (name, ttl) in zip(axs, (("glass", "玻璃芯板（K_IC=0.75）"), ("gc", "微晶玻璃芯板（K_IC=2.0）"))):
        F = feas[name]
        cs = ax.contourf(al * 1e6, Bs * 1e3, F, levels=[-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], cmap=cmap)
        ax.contour(al * 1e6, Bs * 1e3, (F == 4).astype(float), levels=[0.5], colors="#0b6b0b", linewidths=1.6)
        ok = F == 4
        if ok.any():
            ii, jj = np.where(ok)
            ax.text(al[jj].mean() * 1e6, Bs[ii].mean() * 1e3, "全部约束\n满足", ha="center", fontsize=9, color="#0b6b0b")
            res[name] = dict(alpha_range=[float(al[jj].min() * 1e6), float(al[jj].max() * 1e6)], Bmax_mm=float(Bs[ii].max() * 1e3))
        else:
            res[name] = dict(alpha_range=None, Bmax_mm=0.0)
            ax.text(7.5, 50, "无鲁棒可行窗口", ha="center", fontsize=11, color="#a32020")
            ax.annotate("若界面完全粘结(β=0.5)：\n5–7 ppm/K 窄窗口，但该CTE\n玻璃需高碱成分→Df 升高", xy=(6.2, 25), xytext=(8.3, 18),
                        fontsize=7.5, color=INK2, arrowprops=dict(arrowstyle="->", color=INK2, lw=0.8))
        KICv = 0.75e6 if name == "glass" else 2.0e6
        for bet, ls_, lab in ((1.0, "--", "TGV无裂纹边界(脱粘)"), (0.5, ":", "(粘结)")):
            okk = bet * Kmax <= KICv
            if okk.any() and not okk.all():
                xl = al[np.argmax(okk)] * 1e6
                ax.axvline(xl, color=C[7], ls=ls_, lw=1.2); ax.text(xl + 0.1, 75 if bet == 1 else 68, lab, fontsize=8, color=C[7])
        die_line = al[die_ok].max() * 1e6
        ax.axvline(die_line, color=C[0], ls="--", lw=1.2); ax.text(die_line - 0.1, 12, "芯片级CPI边界", fontsize=8, color=C[0], ha="right")
        ax.set_xlabel("芯板 CTE (ppm/K)"); ax.set_title(ttl); ax.grid(False)
    axs[0].set_ylabel("封装体尺寸 B (mm)")
    cb = fig.colorbar(cs, ax=axs, ticks=[0, 1, 2, 3, 4]); cb.set_label("满足的约束数（CPI/BGA/翘曲/TGV裂纹）")
    fig.suptitle("CTE 匹配两难的定量求解：可行设计域（假设见表）", y=1.0)
    savefig(fig, "s4_cte_dilemma.png")
    RES["cte_dilemma"] = dict(alpha=al, aeff=aeff, Kmax=Kmax, feasible=res)
    print("dilemma", res)

def ctedf_map():
    # (CTE ppm/K, Df, label, type) representative literature values (see report table)
    pts = [
        (0.55, 4e-4, "熔融石英 @100 GHz", "g"), (3.2, 6e-3, "铝硼硅玻璃 @10 GHz", "g"), (3.2, 4e-3, "铝硼硅玻璃 @35 GHz", "g"),
        (3.25, 5e-3, "Borofloat33 (典型)", "g"), (7.2, 7e-3, "D263 (典型)", "g"), (9.0, 1.5e-2, "钠钙玻璃 (典型)", "g"),
        (10.0, 1.02e-2, "APEX 光敏微晶 0–20 GHz", "p"),
        (6.1, 1.6e-3, "NEG GCC-1 @40 GHz", "c"), (8.9, 4e-4, "NEG GCC-2 @40 GHz", "c"), (7.4, 7e-4, "NEG GCC-3 @40 GHz", "c"),
        (4.5, 3e-4, "Pyroceram 9606 @8.6 GHz", "c"),
    ]
    fig, ax = plt.subplots(figsize=(6.8, 4.3))
    sty = {"g": (C[0], "o", "玻璃"), "p": (C[3], "s", "光敏微晶玻璃(高碱)"), "c": (C[1], "D", "低碱微晶玻璃/玻璃陶瓷")}
    used = set()
    for x, y, lab, t in pts:
        col, mk, nm = sty[t]
        ax.semilogy(x, y, mk, color=col, ms=8, mec="white", label=nm if t not in used else None); used.add(t)
        ax.annotate(lab, (x, y), xytext=(5, 3), textcoords="offset points", fontsize=7, color=INK2)
    xx = np.linspace(0.5, 10, 50)
    ax.semilogy(xx, 4e-4 * np.exp(0.38 * xx), color=C[0], ls="--", lw=1, label="玻璃趋势：提高CTE需加碱→损耗↑")
    ax.axvspan(5.5, 8.5, color="#e6f4ea", zorder=0)
    ax.text(7.0, 1.3e-4, "板级友好CTE窗口", ha="center", fontsize=8, color="#0b6b0b")
    ax.set_xlabel("CTE (ppm/K)"); ax.set_ylabel("介质损耗 Df"); ax.set_ylim(1e-4, 5e-2)
    ax.set_title("CTE–Df 解耦：微晶玻璃打破玻璃的“碱-损耗”耦合")
    ax.legend(fontsize=7.5, loc="lower right")
    savefig(fig, "s4_cte_df_map.png")

if __name__ == "__main__":
    warpage_validation()
    cte_dilemma()
    ctedf_map()
    save_results("s4_warpage", RES)
