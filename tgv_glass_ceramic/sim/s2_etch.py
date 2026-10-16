"""S2: Selective wet etching of laser-modified tracks in glass-ceramics.
(a) via profile by eikonal (fast marching) vs Huygens analytic taper sin(theta)=1/S  (validation)
(b) sidewall roughness & effective bulk etch rate of a two-phase microstructure:
    fast-marching (deterministic) vs stochastic cellular automaton (independent method)
(c) selectivity amplification by slow-etching crystalline matrix -> achievable aspect ratio"""
import numpy as np
import skfmm
import matplotlib.pyplot as plt
from scipy import ndimage
from common import C, INK2, SEQ, savefig, save_results

RES = {}
rng = np.random.default_rng(7)

def via_profile(S, L=300.0, W=80.0, dx=0.25, double=False, t_extra=None):
    nx, nz = int(W / dx), int(L / dx)
    x = (np.arange(nx) - nx / 2 + 0.5) * dx; z = (np.arange(nz) + 0.5) * dx
    X, Z = np.meshgrid(x, z, indexing="xy")
    speed = np.ones_like(X); speed[np.abs(X) < 0.6] = S
    phi = np.ones_like(X); phi[0, :] = -1
    if double: phi[-1, :] = -1
    T = skfmm.travel_time(phi, speed, dx=dx, order=2)
    t_open = (L / S) if not double else (L / 2 / S)
    t = t_open + (t_extra if t_extra is not None else 0.15 * L / S * 0 + 12.0)
    etched = T <= t
    prof = np.array([x[row].max() if row.any() else 0 for row in etched])   # half-width per depth
    return z, prof, t

def part_a():
    Ss = [10, 20, 50, 100, 300]
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.3))
    meas, ana = [], []
    for i, S in enumerate(Ss):
        z, prof, t = via_profile(S)
        sel = (z > 0.2 * 300) & (z < 0.8 * 300)
        slope = -np.polyfit(z[sel], prof[sel], 1)[0]                # dr/dz
        th_m = np.degrees(np.arctan(slope)); th_a = np.degrees(np.arcsin(1 / S)) if S > 1 else 90
        th_a_tan = np.degrees(np.arctan(1 / np.sqrt(S**2 - 1)))
        meas.append(th_m); ana.append(th_a_tan)
        if S in (10, 50, 300):
            axs[0].plot(prof, z, color=C[i], label=f"S={S}"); axs[0].plot(-prof, z, color=C[i])
    axs[0].invert_yaxis(); axs[0].set_xlabel("x (µm)"); axs[0].set_ylabel("深度 z (µm)")
    axs[0].set_title("快速行进法(FMM)模拟的单面刻蚀TGV剖面"); axs[0].legend(fontsize=8); axs[0].set_aspect(0.35)
    Sx = np.geomspace(5, 1000, 100)
    axs[1].loglog(Sx, np.degrees(np.arctan(1 / np.sqrt(Sx**2 - 1))), color=C[0], label="解析 Huygens：tanθ=1/√(S²−1)")
    axs[1].loglog(Ss, meas, "o", mfc="white", mec=C[1], ms=8, label="FMM 数值")
    axs[1].set_xlabel("刻蚀选择比 S = r_track / r_bulk"); axs[1].set_ylabel("侧壁锥角 θ (°)")
    axs[1].set_title("验证8：锥角 — 程函方程数值 vs 解析"); axs[1].legend(fontsize=8)
    savefig(fig, "s2_via_profile.png")
    err = np.abs(np.array(meas) - np.array(ana)) / np.array(ana)
    RES["taper_validation"] = dict(S=Ss, theta_fmm=meas, theta_analytic=ana, rel_err=err.tolist())
    print("taper", meas, ana)

def microstructure(n, dx, d_mean, f, sigma=0.25):
    """Boolean model of overlapping disks (2-D section) with lognormal diameters."""
    Lx = n * dx
    r_mean = d_mean / 2
    lam = -np.log(1 - f) / (np.pi * r_mean**2 * np.exp(2 * sigma**2))
    N = rng.poisson(lam * (Lx + 2 * d_mean) ** 2)
    cx = rng.uniform(-d_mean, Lx + d_mean, N); cz = rng.uniform(-d_mean, Lx + d_mean, N)
    rr = r_mean * np.exp(sigma * rng.standard_normal(N) - sigma**2 / 2) * 1.0
    grid = np.zeros((n, n), bool)
    xs = (np.arange(n) + 0.5) * dx
    for x0, z0, r in zip(cx, cz, rr):
        i0, i1 = max(0, int((z0 - r) / dx)), min(n, int((z0 + r) / dx) + 2)
        j0, j1 = max(0, int((x0 - r) / dx)), min(n, int((x0 + r) / dx) + 2)
        if i0 >= i1 or j0 >= j1: continue
        Zs, Xs = np.meshgrid(xs[i0:i1], xs[j0:j1], indexing="ij")
        grid[i0:i1, j0:j1] |= (Xs - x0) ** 2 + (Zs - z0) ** 2 <= r * r
    return grid

def roughness_fmm(cryst, dx, rho, depth):
    speed = np.where(cryst, 1.0, rho)              # crystal rate 1, glass rate rho (relative)
    phi = np.ones(cryst.shape); phi[:, 0] = -1      # cavity at x=0 side, etch toward +x
    T = skfmm.travel_time(phi, speed, dx=dx, order=1)
    # find time t such that the mean recession of the first-solid surface equals depth
    def surf(t):
        solid = T > t
        idx = np.argmax(solid, axis=1)
        return idx * dx
    lo, hi = 0, T[np.isfinite(T)].max()
    for _ in range(40):
        mid = (lo + hi) / 2
        if surf(mid).mean() < depth: lo = mid
        else: hi = mid
    xs = surf(hi)
    return xs.std(), depth / hi, xs

def roughness_ca(cryst, dx, rho, depth, rmax=None):
    """Stochastic cellular automaton: exposed cells dissolve with probability ~ local rate."""
    rates = np.where(cryst, 1.0, rho); rmax = rates.max()
    p = rates / rmax * 0.5
    etched = np.zeros(cryst.shape, bool); etched[:, 0] = True
    st = np.ones((3, 3), bool); st[0, 0] = st[0, 2] = st[2, 0] = st[2, 2] = False
    steps = 0
    while True:
        front = ndimage.binary_dilation(etched, structure=st) & ~etched
        rem = front & (rng.random(cryst.shape) < p)
        etched |= rem; steps += 1
        solid = ~etched
        xs = np.argmax(solid, axis=1) * dx
        if xs.mean() >= depth or steps > 20000: break
    return xs.std(), xs

def part_b():
    n = 600; depth = 0.8
    ds = [0.03, 0.06, 0.12, 0.25]   # um
    rhos = [3, 10, 30]
    f = 0.5
    out = {"fmm": {}, "ca": {}}
    fig, axs = plt.subplots(1, 3, figsize=(15.5, 4.3)); fig.subplots_adjust(wspace=0.38)
    for j, rho in enumerate(rhos):
        Rq_f, Rq_c = [], []
        for d in ds:
            dx = d / 12
            cr = microstructure(n, dx, d, f)
            rq, reff, xs = roughness_fmm(cr, dx, rho, min(depth, n * dx * 0.4))
            rqc, xsc = roughness_ca(cr, dx, rho, min(depth, n * dx * 0.4))
            Rq_f.append(rq); Rq_c.append(rqc)
        out["fmm"][rho] = Rq_f; out["ca"][rho] = Rq_c
        axs[0].loglog(np.array(ds) * 1e3, np.array(Rq_f) * 1e3, "o-", color=C[j], label=f"FMM ρ=r_g/r_c={rho}")
        axs[0].loglog(np.array(ds) * 1e3, np.array(Rq_c) * 1e3, "s--", color=C[j], mfc="white", label=f"元胞自动机 ρ={rho}")
    dd = np.array([20, 300]); axs[0].loglog(dd, dd * 0.5, color=INK2, lw=0.8, ls=":"); axs[0].text(150, 60, "Rq ∝ d", fontsize=8, color=INK2)
    axs[0].set_xticks([30, 60, 120, 250]); axs[0].set_xticklabels(["30", "60", "120", "250"]); axs[0].minorticks_off()
    axs[0].set_xlabel("晶粒平均直径 d (nm)"); axs[0].set_ylabel("侧壁粗糙度 Rq (nm)")
    axs[0].set_title("验证9：两种独立刻蚀模型的粗糙度标度"); axs[0].legend(fontsize=6.5, ncol=2)
    # example microstructure + front
    d = 0.06; dx = d / 12; cr = microstructure(n, dx, d, f)
    rq, reff, xs = roughness_fmm(cr, dx, 10, 0.8 * n * dx * 0.4 / 0.4 * 0.4)
    axs[1].imshow(cr.T[:300, :], cmap="Greys", origin="upper", extent=[0, n * dx * 1e3, 300 * dx * 1e3, 0], alpha=0.6)
    axs[1].plot(np.arange(n) * dx * 1e3, xs * 1e3, color=C[1], lw=1.2)
    axs[1].set_xlabel("沿孔壁方向 (nm)"); axs[1].set_ylabel("刻蚀推进方向 (nm)"); axs[1].grid(False)
    axs[1].set_title(f"微结构与刻蚀前沿\n(d=60 nm, f=0.5, ρ=10, Rq={rq*1e3:.0f} nm)", fontsize=10)
    # (c) effective bulk rate vs crystallinity -> selectivity amplification
    fs = [0.1, 0.3, 0.5, 0.6, 0.7, 0.8]
    amp = {}
    for j, rho in enumerate(rhos):
        a_ = []
        for ff in fs:
            dx = 0.06 / 12; cr = microstructure(400, dx, 0.06, ff)
            _, reff, _ = roughness_fmm(cr, dx, rho, 400 * dx * 0.5)
            a_.append(rho / reff)                       # r_glass / r_eff,bulk
        amp[rho] = a_
        harm = rho / (1 / (np.array(fs) / 1 + (1 - np.array(fs)) / rho))
        axs[2].semilogy(fs, a_, "o-", color=C[j], label=f"FMM ρ={rho}")
        axs[2].semilogy(fs, harm, ls=":", color=C[j], lw=1.2, label="串联极限（放大因子上界）" if j == 0 else None)
    try:
        import json as _j
        d3 = _j.load(open("../results/s2b_etch3d.json"))
        for j, rho in enumerate(rhos):
            pts = [(v["f_actual"], v["amp"]) for k, v in d3.items() if k.startswith(f"rho{rho}_")]
            if pts:
                pts = np.array(pts); axs[2].semilogy(pts[:, 0], pts[:, 1], "^", color=C[j], mfc="white", ms=8, label="3D 校核" if rho == 10 else None)
    except FileNotFoundError:
        pass
    axs[2].set_xlabel("晶化率 f"); axs[2].set_ylabel("选择比放大因子 r_glass / r_bulk,eff")
    axs[2].set_title("慢刻蚀晶相基体对选择比的放大\n（实心=2D，三角=3D）", fontsize=10); axs[2].legend(fontsize=7)
    savefig(fig, "s2_roughness_selectivity.png")
    RES["roughness"] = dict(d_um=ds, f=f, fmm={str(k): v for k, v in out["fmm"].items()}, ca={str(k): v for k, v in out["ca"].items()})
    RES["selectivity_amplification"] = dict(f=fs, **{str(k): v for k, v in amp.items()})
    print(RES["roughness"]); print(RES["selectivity_amplification"])

def part_ar():
    S = np.geomspace(5, 3000, 100)
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    for k, (ratio, col) in enumerate([(0.8, C[0]), (0.6, C[1])]):
        ax.loglog(S, (1 - ratio) / 2 * S, color=col, label=f"单面刻蚀, D_bot/D_top={ratio}")
        ax.loglog(S, (1 - ratio) * S, color=col, ls="--", label=f"双面刻蚀(沙漏形), D_waist/D_top={ratio}")
    for s_, lab in [(66, "HF 熔石英"), (955, "KOH 熔石英"), (2103, "贝塞尔+KOH")]:
        ax.axvline(s_, color="#c9c8c2", lw=1); ax.text(s_ * 1.05, 0.7, lab, fontsize=7, color=INK2, rotation=90)
    ax.axhspan(10, 20, color="#e6f4ea", zorder=0); ax.text(6, 13, "目标 AR 10–20", fontsize=8, color="#0b6b0b")
    ax.set_xlabel("刻蚀选择比 S"); ax.set_ylabel("可实现深宽比 AR"); ax.set_ylim(0.5, 2000)
    ax.set_title("选择比-深宽比标度律：AR ≈ (1−D_b/D_t)·S/2"); ax.legend(fontsize=7)
    savefig(fig, "s2_selectivity_ar.png")

if __name__ == "__main__":
    part_a()
    part_b()
    part_ar()
    save_results("s2_etch", RES)
