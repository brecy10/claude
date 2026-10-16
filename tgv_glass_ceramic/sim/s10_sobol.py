"""S10: Global variance-based (Sobol) sensitivity analysis of two surrogate models built on the
validated analytic kernels: (A) TGV radial-crack safety margin, (B) 140 GHz insertion loss per via."""
import numpy as np
import matplotlib.pyplot as plt
from SALib.sample import sobol as sobol_sample
from SALib.analyze import sobol
from common import C, INK2, savefig, save_results

RES = {}
eps0, mu0, c0 = 8.8541878128e-12, 4e-7 * np.pi, 299792458.0

def crack_margin(X):
    a_s, E_s, nu_s, d, Tpk, a_cu, E_cu, KIC, beta = X.T
    nu_c = 0.34; dT = Tpk - 25
    mis = ((1 + nu_c) * a_cu - (1 + nu_s) * a_s) * dT
    comp = (1 + nu_c) * (1 - 2 * nu_c) / E_cu + (1 + nu_s) / E_s
    s0 = mis / comp
    Kmax = beta * 0.885 * s0 * np.sqrt(d / 2)
    return np.log10(KIC / Kmax)

def il140(X):
    Dk, Df10, gam, Rq, d, pd, t = X.T
    f = 140e9; rho = 1.8e-8
    Rs = np.sqrt(np.pi * f * mu0 * rho); delta = np.sqrt(rho / (np.pi * f * mu0))
    Kr = 1 + 2 / np.pi * np.arctan(1.4 * (Rq / delta) ** 2)
    Cair = 2 * np.pi * eps0 / np.arccosh(pd)              # GSG ~ two parallel two-wire lines
    Lp = mu0 * eps0 / Cair; Cp = Cair * Dk
    Z0 = np.sqrt(Lp / Cp)
    prox = 1 / np.sqrt(1 - (1 / pd) ** 2)
    Rp = Rs * Kr * prox * 1.5 / (np.pi * d)
    tand = Df10 * (f / 10e9) ** gam
    alpha = Rp / (2 * Z0) + np.pi * f * np.sqrt(Dk) * tand / c0
    G = (Z0 - 50) / (Z0 + 50)
    mism = -10 * np.log10(1 - G**2)
    return 8.686 * alpha * t + mism

def run(name, func, names, bounds, N=4096):
    prob = dict(num_vars=len(names), names=names, bounds=bounds)
    X = sobol_sample.sample(prob, N, calc_second_order=False, seed=11)
    Y = func(X)
    Si = sobol.analyze(prob, Y, calc_second_order=False, seed=11)
    RES[name] = dict(names=names, S1=Si["S1"], ST=Si["ST"], S1_conf=Si["S1_conf"], ST_conf=Si["ST_conf"], Ymean=float(Y.mean()), Ystd=float(Y.std()))
    return Si

def main():
    nA = ["基板CTE α_s", "基板模量 E_s", "基板泊松比", "通孔直径 d", "峰值温度", "Cu CTE", "Cu 模量", "断裂韧性 K_IC", "界面粘结因子 β"]
    bA = [[0.5e-6, 10e-6], [60e9, 150e9], [0.17, 0.27], [10e-6, 100e-6], [200, 420], [16.5e-6, 17.7e-6], [100e9, 130e9], [0.7e6, 2.5e6], [0.5, 1.0]]
    SA = run("crack", crack_margin, nA, bA)
    nB = ["Dk", "Df@10GHz", "损耗频散指数", "侧壁粗糙度 Rq", "通孔直径 d", "节距/直径 p/d", "基板厚度 t"]
    bB = [[3.8, 7.0], [2e-4, 6e-3], [0.2, 0.7], [20e-9, 1e-6], [20e-6, 80e-6], [1.8, 4.0], [100e-6, 500e-6]]
    SB = run("il140", il140, nB, bB)
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 4.4))
    for ax, Si, nm, ttl in [(axs[0], SA, nA, "模型A：TGV 径向裂纹安全裕度 log10(K_IC/K_max)"), (axs[1], SB, nB, "模型B：140 GHz 单孔插损 (dB)")]:
        y = np.arange(len(nm)); o = np.argsort(Si["ST"])
        ax.barh(y - 0.18, Si["S1"][o], 0.34, color=C[0], label="一阶指数 S1", xerr=Si["S1_conf"][o], error_kw=dict(lw=0.8, ecolor=INK2))
        ax.barh(y + 0.18, Si["ST"][o], 0.34, color=C[1], label="总效应指数 ST", xerr=Si["ST_conf"][o], error_kw=dict(lw=0.8, ecolor=INK2))
        ax.set_yticks(y); ax.set_yticklabels([nm[i] for i in o]); ax.set_xlabel("Sobol 指数"); ax.set_title(ttl, fontsize=10)
        ax.legend(fontsize=8, loc="lower right"); ax.grid(axis="y", visible=False)
    savefig(fig, "s10_sobol.png")
    print({k: dict(zip(v["names"], np.round(v["ST"], 3))) for k, v in RES.items()})

if __name__ == "__main__":
    main()
    save_results("s10_sobol", RES)
