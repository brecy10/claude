"""S1: Laser-matter interaction in glass-ceramics.
(a) Mie vs Rayleigh scattering of nanocrystals (validation), dependent scattering (Percus-Yevick)
(b) transparency criterion for Bessel-beam TGV writing: max crystal size vs index contrast
(c) Monte-Carlo photon transport vs Beer-Lambert (validation) + diffuse background
(d) heat accumulation model for laser-written phase collars: analytic line-source superposition
    vs Crank-Nicolson finite differences (validation) -> collar radius process window"""
import numpy as np
import matplotlib.pyplot as plt
import miepython
from common import C, INK2, SEQ, PHASE, savefig, save_results

RES = {}
lam0 = 1030e-9; nm = PHASE["glass"]["n"]

def qsca(m, x):
    return miepython.efficiencies_mx(m, x)[1], miepython.efficiencies_mx(m, x)[3]

def mu_s(d, f, n_p, lam=lam0, n_m=nm, dependent=True):
    r = d / 2; x = np.pi * d * n_m / lam
    Q, g = qsca(n_p / n_m, x)
    mu = 3 * f * Q / (4 * r)
    if dependent:
        # PY structure factor (long-wavelength limit); only physically meaningful for x << 1,
        # blended to 1 for large particles -> gives the optimistic (lower) bound of mu_s
        S0 = (1 - f) ** 4 / (1 + 2 * f) ** 2
        w = 1 / (1 + (x / 0.5) ** 4)
        mu *= w * S0 + (1 - w)
    return mu, g

def mu_nucleant(d=15e-9, f=0.03, n_p=2.2, lam=lam0, n_m=nm):
    """Scattering of ZrO2/ZrTiO4 nucleating-agent nanocrystals (independent scattering)."""
    x = np.pi * d * n_m / lam
    Q, g = qsca(n_p / n_m, x)
    return 3 * f * Q / (2 * d)

def part_a_b():
    # (a) Mie vs Rayleigh
    xs = np.geomspace(0.01, 3, 200)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.1))
    errs = {}
    for i, (nmname, npr) in enumerate([("堇青石/玻璃 Δn≈0.01", PHASE["cordierite"]["n"]), ("镁橄榄石/玻璃 Δn≈0.12", PHASE["forsterite"]["n"])]):
        m = npr / nm
        Qm = np.array([qsca(m, x)[0] for x in xs])
        Qr = 8 / 3 * xs**4 * abs((m**2 - 1) / (m**2 + 2)) ** 2
        axs[0].loglog(xs, Qm, color=C[i], label=f"Mie 精确解 {nmname}")
        axs[0].loglog(xs, Qr, color=C[i], ls="--", lw=1.2, label="Rayleigh 近似")
        sel = xs < 0.1
        errs[nmname] = float(np.max(np.abs(Qm[sel] - Qr[sel]) / Qm[sel]))
    axs[0].set_xlabel("尺寸参数 x = π d n_m / λ"); axs[0].set_ylabel("散射效率 Q_sca"); axs[0].legend(fontsize=7.5)
    axs[0].set_title("验证5：Mie vs Rayleigh（x<0.1 偏差<1%）")
    RES["mie_rayleigh_maxrel_x<0.1"] = errs
    # (b) transmission over 500 um vs crystal diameter, f=0.5
    ds = np.geomspace(5e-9, 3e-6, 140); L = 500e-6
    cases = [("β-石英ss Δn=0.015", PHASE["bquartz"]["n"], C[2]), ("堇青石 Δn=0.010", PHASE["cordierite"]["n"], C[0]),
             ("镁橄榄石 Δn=0.12", PHASE["forsterite"]["n"], C[1])]
    out = {}
    for name, npr, col in cases:
        T_dep = np.array([np.exp(-mu_s(d, 0.5, npr)[0] * L) for d in ds])
        T_ind = np.array([np.exp(-mu_s(d, 0.5, npr, dependent=False)[0] * L) for d in ds])
        axs[1].semilogx(ds * 1e9, T_ind, color=col, label=f"{name}（独立散射，保守）")
        axs[1].fill_between(ds * 1e9, T_ind, T_dep, color=col, alpha=0.15, lw=0)
        dmax = ds[np.where(T_ind > 0.9)[0].max()] if (T_ind > 0.9).any() else np.nan
        dmax_opt = ds[np.where(T_dep > 0.9)[0].max()] if (T_dep > 0.9).any() else np.nan
        out[name] = dict(conservative=float(dmax * 1e9), optimistic=float(dmax_opt * 1e9))
    for k_, (dnu, col) in enumerate([(10e-9, C[6]), (25e-9, C[7])]):
        Tn = np.exp(-mu_nucleant(d=dnu) * L)
        axs[1].axhline(Tn, color=col, ls="-.", lw=1.1)
        axs[1].text(5.5, 0.84 - 0.06 * k_, f"仅成核剂 ZrTiO4 {dnu*1e9:.0f} nm, 3 vol%: T={Tn:.2f}", fontsize=7, color=col)
        out[f"nucleant_{dnu*1e9:.0f}nm_T"] = float(Tn)
    axs[1].axhline(0.9, color=INK2, lw=1, ls="--"); axs[1].text(6, 0.92, "T_ballistic>0.9 判据", fontsize=8, color=INK2)
    axs[1].set_xlabel("晶粒直径 d (nm)"); axs[1].set_ylabel("500 µm 弹道透过率 @1030 nm")
    axs[1].set_title("透明性判据（f=0.5；色带=PY相关散射修正的乐观界）"); axs[1].legend(fontsize=7.5, loc="lower left")
    savefig(fig, "s1_scattering.png")
    RES["dmax_nm_T0.9_f0.5"] = out
    print("dmax", out, "mie err", errs)
    # map: max diameter vs dn and f
    dns = np.linspace(0.002, 0.15, 40); fs = np.linspace(0.1, 0.8, 36)
    Dm = np.zeros((len(fs), len(dns)))
    dgrid = np.geomspace(5e-9, 2e-6, 90)
    for i, f in enumerate(fs):
        for j, dn in enumerate(dns):
            T = np.array([np.exp(-mu_s(d, f, nm + dn, dependent=False)[0] * L) for d in dgrid])
            ok = np.where(T > 0.9)[0]
            Dm[i, j] = dgrid[ok.max()] * 1e9 if len(ok) else 5
    fig, ax = plt.subplots(figsize=(6.4, 4.3))
    cs = ax.contourf(dns, fs, np.log10(Dm), levels=np.linspace(0.7, 3.3, 14), cmap="Blues")
    cl = ax.contour(dns, fs, Dm, levels=[30, 50, 100, 200, 500], colors="k", linewidths=0.7)
    ax.clabel(cl, fmt="%d nm", fontsize=8)
    for name, npr, col in cases:
        ax.axvline(npr - nm if npr > nm else nm - npr, color=col, ls="--", lw=1.2)
    cb = fig.colorbar(cs, ax=ax); cb.set_label("log10(最大允许晶粒直径 / nm)")
    ax.set_xlabel("晶相/玻璃相折射率差 Δn"); ax.set_ylabel("晶化率 f"); ax.grid(False)
    ax.set_title("贝塞尔光束直写的“纳米晶透明窗口”（500 µm, T>0.9, 保守）")
    savefig(fig, "s1_transparency_map.png")
    RES["transparency_map"] = dict(dn=dns, f=fs, dmax_nm=Dm)

def part_c_mc():
    """MC photon transport with Henyey-Greenstein phase function."""
    rng = np.random.default_rng(1)
    L = 500e-6
    out = []
    for d, npr in [(150e-9, PHASE["forsterite"]["n"]), (250e-9, PHASE["forsterite"]["n"]), (600e-9, PHASE["cordierite"]["n"]), (1500e-9, PHASE["cordierite"]["n"])]:
        mus, g = mu_s(d, 0.5, npr)
        N = 200000
        z = np.zeros(N); uz = np.ones(N); alive = np.ones(N, bool); nsc = np.zeros(N, int)
        trans = np.zeros(N, bool); ux = np.zeros(N); uy = np.zeros(N)
        for it in range(300):
            if not alive.any(): break
            idx = np.where(alive)[0]
            s = -np.log(rng.random(len(idx))) / mus
            znew = z[idx] + s * uz[idx]
            out_top = znew >= L; out_bot = znew < 0
            trans[idx[out_top]] = True
            alive[idx[out_top | out_bot]] = False
            sc = idx[~(out_top | out_bot)]
            z[sc] = znew[~(out_top | out_bot)]
            # HG sampling
            xi = rng.random(len(sc))
            if abs(g) > 1e-6:
                ct = (1 + g**2 - ((1 - g**2) / (1 - g + 2 * g * xi)) ** 2) / (2 * g)
            else:
                ct = 2 * xi - 1
            phi = 2 * np.pi * rng.random(len(sc)); st = np.sqrt(1 - ct**2)
            u0x, u0y, u0z = ux[sc], uy[sc], uz[sc]
            den = np.sqrt(np.maximum(1 - u0z**2, 1e-12))
            nx = np.where(den > 1e-5, st * (u0x * u0z * np.cos(phi) - u0y * np.sin(phi)) / den + u0x * ct, st * np.cos(phi))
            ny = np.where(den > 1e-5, st * (u0y * u0z * np.cos(phi) + u0x * np.sin(phi)) / den + u0y * ct, st * np.sin(phi))
            nz = np.where(den > 1e-5, -st * np.cos(phi) * den + u0z * ct, np.sign(u0z) * ct)
            ux[sc], uy[sc], uz[sc] = nx, ny, nz
            nsc[sc] += 1
        ball_mc = np.mean(trans & (nsc == 0)); ball_bl = np.exp(-mus * L)
        out.append(dict(d_nm=d * 1e9, dn=npr - nm, mus_per_mm=mus * 1e-3, g=g, ballistic_MC=ball_mc, ballistic_BL=ball_bl,
                        total_T=np.mean(trans), diffuse=np.mean(trans & (nsc > 0))))
    RES["monte_carlo"] = out
    for o in out: print("MC", o)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    xl = [f"d={o['d_nm']:.0f} nm\nΔn={o['dn']:.2f}" for o in out]; x = np.arange(len(out))
    ax.bar(x - 0.27, [o["ballistic_BL"] for o in out], 0.25, color=C[0], label="Beer–Lambert 解析 弹道透过")
    ax.bar(x, [o["ballistic_MC"] for o in out], 0.25, color=C[2], label="蒙特卡洛 弹道透过")
    ax.bar(x + 0.27, [o["diffuse"] for o in out], 0.25, color=C[1], label="蒙特卡洛 漫射透过（焦线外背景）")
    ax.set_xticks(x); ax.set_xticklabels(xl, fontsize=8); ax.set_ylabel("比例（500 µm, f=0.5）")
    ax.set_title("验证6：光子输运蒙特卡洛 vs Beer–Lambert"); ax.legend(fontsize=7.5); ax.set_ylim(0, 1.05)
    savefig(fig, "s1_montecarlo.png")

def part_d_heat():
    rho_c = 2.6e3 * 850.0
    def analytic(r, Ep, frep, N, k, eta=0.4, Lf=300e-6, w0=1.0e-6, t_after=None):
        D = k / rho_c; Q = eta * Ep / Lf
        t_after = t_after if t_after is not None else 1 / frep * 0.999
        ts = t_after + np.arange(N)[::-1] / frep * 0 + np.arange(N) / frep
        T = np.zeros_like(r)
        for t in ts:
            T += Q / (np.pi * rho_c * (4 * D * t + w0**2)) * np.exp(-r**2 / (4 * D * t + w0**2))
        return T
    def fd(r_max, Ep, frep, N, k, eta=0.4, Lf=300e-6, w0=1.0e-6, nr=600):
        D = k / rho_c; Q = eta * Ep / Lf
        r = np.linspace(0, r_max, nr + 1); dr = r[1] - r[0]
        T = np.zeros_like(r)
        src = Q / (np.pi * rho_c * w0**2) * np.exp(-r**2 / w0**2)
        dt_target = 1 / frep
        nsub = max(4, int(np.ceil(dt_target / (0.25 * dr**2 / D) / 20)))
        dt = dt_target / nsub
        # Crank-Nicolson in cylindrical coords (symmetry at r=0, T=0 at r_max)
        import scipy.sparse as sp, scipy.sparse.linalg as spla
        main = np.zeros(nr + 1); lo = np.zeros(nr); up = np.zeros(nr)
        for i in range(1, nr):
            ri = r[i]
            lo[i - 1] = D / dr**2 * (1 - dr / (2 * ri)); up[i] = D / dr**2 * (1 + dr / (2 * ri)); main[i] = -2 * D / dr**2
        main[0] = -4 * D / dr**2; up[0] = 4 * D / dr**2
        Lop = sp.diags([lo, main, up], [-1, 0, 1], format="csc")
        I = sp.eye(nr + 1, format="csc")
        A = (I - 0.5 * dt * Lop).tolil(); B = (I + 0.5 * dt * Lop).tolil()
        A[nr, :] = 0; A[nr, nr] = 1; B[nr, :] = 0
        solver = spla.factorized(A.tocsc()); B = B.tocsr()
        Tmax = np.zeros_like(r)
        for p in range(N):
            T = T + src
            Tmax = np.maximum(Tmax, T)
            for s in range(nsub):
                T = solver(B @ T)
        return r, T, Tmax
    k_gc = 2.0
    Ep, frep, N = 10e-6, 1e6, 200
    r = np.linspace(0, 40e-6, 400)
    rr, Tfd, _ = fd(200e-6, Ep, frep, N, k_gc)
    Tan = analytic(rr, Ep, frep, N, k_gc, t_after=1 / frep)
    sel = rr < 40e-6
    err = float(np.max(np.abs(Tfd[sel] - Tan[sel])) / Tan[sel].max())
    RES["heat_validation_maxrel"] = err
    print("heat validation err", err)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.1))
    axs[0].plot(rr[sel] * 1e6, Tan[sel], color=C[0], label="解析：高斯线热源叠加")
    axs[0].plot(rr[sel][::12] * 1e6, Tfd[sel][::12], "o", mfc="white", mec=C[1], label="数值：Crank–Nicolson 有限差分")
    axs[0].set_xlabel("距焦线距离 r (µm)"); axs[0].set_ylabel("温升 ΔT (K)（第200个脉冲到达前）")
    axs[0].set_title(f"验证7：热累积模型（E_p=10 µJ, 1 MHz, k={k_gc} W/mK）"); axs[0].legend(fontsize=8)
    # process window: collar radius where peak T exceeds thresholds vs rep rate at fixed pulse energy
    freps = np.geomspace(1e5, 2e7, 40); out = {}
    T_x, T_m = 950.0 - 25, 1450.0 - 25
    for Ep, col in [(5e-6, C[0]), (10e-6, C[1]), (20e-6, C[2])]:
        rx, rm = [], []
        for fr in freps:
            Tb = analytic(r, Ep, fr, 300, k_gc, t_after=1 / fr)                # baseline before last pulse
            Tpk = Tb + 0.4 * Ep / 300e-6 / (np.pi * rho_c * (1.0e-6) ** 2) * np.exp(-r**2 / 1.0e-12)
            rx.append(r[Tb > T_x].max() * 1e6 if (Tb > T_x).any() else 0)     # sustained above crystallization onset
            rm.append(r[Tpk > T_m].max() * 1e6 if (Tpk > T_m).any() else 0)   # transient melting (amorphization)
        out[f"{Ep*1e6:.0f}uJ"] = dict(frep=freps, r_cryst=rx, r_melt=rm)
        axs[1].semilogx(freps / 1e6, rx, color=col, label=f"持续>T_x 晶化环半径 E_p={Ep*1e6:.0f} µJ")
        axs[1].semilogx(freps / 1e6, rm, color=col, ls="--", lw=1.3, label=f"瞬态>T_m 熔化/非晶化半径")
    axs[1].set_xlabel("重复频率 (MHz)"); axs[1].set_ylabel("相变环半径 (µm)")
    axs[1].set_title("激光“相环”工艺窗口：重频调控晶化/非晶化环宽"); axs[1].legend(fontsize=7)
    savefig(fig, "s1_heat_accumulation.png")
    RES["collar_window"] = out

if __name__ == "__main__":
    part_a_b()
    part_c_mc()
    part_d_heat()
    save_results("s1_laser", RES)
