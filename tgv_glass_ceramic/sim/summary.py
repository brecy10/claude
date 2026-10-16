"""Collect key numbers from all simulation modules and draw the cross-validation matrix figure."""
import json, numpy as np
import matplotlib.pyplot as plt
from common import C, INK2, savefig, RES, save_results
J = lambda n: json.load(open(f"{RES}/{n}.json"))
s1, s2, s3, s3b, s3c, s4, s5, s6, s7, s8, s10 = [J(n) for n in ["s1_laser", "s2_etch", "s3_thermomech", "s3b_fracture", "s3c_fracture_check", "s4_warpage", "s5_thermal", "s6_electrical", "s7_ceramming", "s8_microstructure", "s10_sobol"]]
s2b = J("s2b_etch3d")
V = []
v = s3["validation"]
V.append(("V1a 热应力：GPS-Lamé 解析 vs 自编Q4-Bbar FEM", max(x["q4_max_rel"] for x in v.values()), "解析-数值"))
V.append(("V1b 热应力：GPS-Lamé 解析 vs scikit-fem P2", max(x["p2_max_rel"] for x in v.values()), "解析-数值"))
V.append(("V2a 断裂：Griffith 精确解 vs FEM 能量法", s3c["griffith"]["err_energy"], "解析-数值"))
V.append(("V2b 断裂：Griffith 精确解 vs FEM 张开位移法", s3c["griffith"]["err_cod"], "解析-数值"))
hc = s3c["hole_core"]
kc, ke = np.array(hc["K_core_cod"]), np.array(hc["K_core_energy"])
V.append(("V2c 断裂：粘结Cu芯 能量法 vs 张开位移法", float(np.median(np.abs(kc - ke) / kc)), "数值-数值"))
V.append(("V2d 断裂：权函数近似 vs 自由孔FEM（保守偏差）", hc["err_wf_vs_hole"], "近似-精确"))
V.append(("V4 翘曲：层合板理论 vs 轴对称FEM", max(x["err"] for x in s4["validation"]), "解析-数值"))
V.append(("V5 散射：Rayleigh 近似 vs Mie 精确(x<0.1)", max(s1["mie_rayleigh_maxrel_x<0.1"].values()), "近似-精确"))
mc = [o for o in s1["monte_carlo"] if o["ballistic_BL"] > 0.01]
V.append(("V6 光输运：蒙特卡洛 vs Beer–Lambert", max(abs(o["ballistic_MC"] - o["ballistic_BL"]) / o["ballistic_BL"] for o in mc), "统计-解析"))
V.append(("V7 热累积：线热源叠加 vs Crank–Nicolson", s1["heat_validation_maxrel"], "解析-数值"))
V.append(("V8 刻蚀锥角：FMM 数值 vs Huygens 解析", float(np.median(s2["taper_validation"]["rel_err"])), "解析-数值"))
rf, rc = s2["roughness"]["fmm"], s2["roughness"]["ca"]
diffs = [abs(a - b) / a for k in rf for a, b in zip(rf[k], rc[k])]
V.append(("V9 粗糙度：FMM vs 元胞自动机", float(np.median(diffs)), "数值-随机"))
V.append(("V10 晶粒应力：Selsing 解析 vs 轴对称FEM", max(x["fem_err_matrix"] for x in s8["selsing"].values()), "解析-数值"))
V.append(("V11a 晶化：Kissinger 反演 Ea vs 输入值", abs(s7["kissinger"]["Ea_kissinger"] - 4e5) / 4e5, "方法自洽"))
V.append(("V11b 套刻：薄盘本征应变解析 vs 平面应力FEM", s7["disk_validation_maxrel"], "解析-数值"))
V.append(("V12 热扩散：Fourier–Bessel 级数 vs FEM", max(x["rel"] for x in s5["validation"]), "解析-数值"))
V.append(("V13 介电均匀化：有限体积RVE vs 2D Maxwell-Garnett", max(s6["rve_validation"]["rel_err_vs_MG2D"]), "数值-解析"))
V.append(("V14 TGV电容：FEM vs 双线精确解", max(o["rel"] for o in s6["twowire_validation"]), "数值-解析"))
k140 = s6["Kr_140GHz"]["150nm"]
V.append(("V15 粗糙度损耗：Hammerstad vs Groiss (150 nm,140 GHz)", abs(k140["H"] - k140["G"]) / k140["H"], "模型-模型"))
fig, ax = plt.subplots(figsize=(9.5, 6.4))
cats = {"解析-数值": C[0], "数值-数值": C[2], "近似-精确": C[1], "统计-解析": C[6], "数值-随机": C[3], "方法自洽": C[5], "数值-解析": C[0], "模型-模型": C[7]}
y = np.arange(len(V))[::-1]
for yy, (n, e, c) in zip(y, V):
    ax.barh(yy, max(e, 1e-6) * 100, color=cats[c], height=0.62)
    ax.text(max(e, 1e-6) * 100 * 1.15, yy, f"{e*100:.3g}%", va="center", fontsize=7.5, color=INK2)
ax.set_xscale("log"); ax.set_yticks(y); ax.set_yticklabels([n for n, _, _ in V], fontsize=8)
ax.axvline(1, color=INK2, ls="--", lw=1); ax.text(1.05, len(V) - 0.6, "1% 线", fontsize=8, color=INK2)
ax.set_xlabel("相对偏差 (%)，对数坐标"); ax.set_xlim(1e-3, 300); ax.grid(axis="y", visible=False)
ax.set_title("多方法交叉验证闭环汇总（15 组独立方法对）")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=C[0], label="解析 ↔ 数值"), Patch(color=C[2], label="数值 ↔ 数值"), Patch(color=C[1], label="近似 ↔ 精确（偏差=近似的保守度）"),
                   Patch(color=C[6], label="统计 ↔ 解析"), Patch(color=C[3], label="确定性 ↔ 随机"), Patch(color=C[5], label="反演自洽"), Patch(color=C[7], label="模型 ↔ 模型")],
          fontsize=7.5, loc="lower right")
savefig(fig, "fig_validation_matrix.png")
out = dict(validation=[dict(name=n, rel=e, cat=c) for n, e, c in V])
# key numbers
sm = s3["summary"]
out["thermomech"] = {k: dict(st_mid_MPa=v["st_mid_max"] / 1e6, s1_MPa=v["s1_max"] / 1e6, sr_res_MPa=v["sr_res_after_anneal"] / 1e6,
                              protr400_um=v["protr_400"] * 1e6, protr_res_um=v["protr_res"] * 1e6, dpacc_cycle=v["dpacc_cycle"],
                              Nf_CM=0.5 * (max(v["dpacc_cycle"] / 2, 1e-6) / (2 * 0.3)) ** (1 / -0.6)) for k, v in sm.items()}
out["strategies"] = [dict(name=o["name"], st_mid=o["st_mid"] / 1e6, sr_res=o["sr_res"] / 1e6, protr_max=o["protr_max"] * 1e6) for o in s3["strategies"]]
out["dcrit_400C_um"] = s3b["dcrit_400C_um"]; out["Fmax"] = s3b["Fmax"]
out["weibull"] = s3b["weibull"]
out["K_core_vs_hole"] = hc["ratio_core_to_hole"]
out["dilemma"] = s4["cte_dilemma"]["feasible"]
out["warp_val"] = s4["validation"]
out["s1"] = dict(dmax=s1["dmax_nm_T0.9_f0.5"])
out["s5"] = {k: [s5["Tmax_vs_phi"][k][i] for i in (0, 5, 10, 20)] for k in ["ORG", "BG", "FS", "GCC", "GCF"]}
out["s6"] = dict(diss=s6["diss_per_via_dB"], design=s6["design_p_over_d_50ohm"], ad140=s6["alpha_d_140_dB_per_mm"], bench28=s6["benchmark_28GHz_100um_BG_dB"], Kr=s6["Kr_140GHz"])
out["s7"] = dict(kissinger=s7["kissinger"], reg=s7["registration"])
out["s8"] = dict(P=s8["selsing"], dcrit_f=s8["dcrit_forsterite_um"], dcrit_c=s8["dcrit_cordierite_um"])
out["s10"] = {k: dict(zip(v["names"], v["ST"])) for k, v in s10.items()}
out["s2b"] = s2b
save_results("summary", out)
print(json.dumps({k: out[k] for k in ["thermomech", "strategies", "dcrit_400C_um", "K_core_vs_hole", "dilemma", "s5", "s6", "s8"]}, ensure_ascii=False, indent=0, default=str)[:6000])
