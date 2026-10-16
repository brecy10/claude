"""S7: Ceramming (crystallization) kinetics and panel-level dimensional control.
(a) synthetic non-isothermal DSC from JMAK -> Kissinger/Ozawa analysis recovers Ea (closed loop for
    the experimental analysis method)
(b) isothermal schedule: crystallinity sensitivity to furnace non-uniformity; saturation strategy
(c) shrinkage-induced registration error on 510x515 mm panel: analytic thin-disk solution vs
    plane-stress FEM (validation), residual error after linear scale compensation"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import brentq
from skfem import MeshTri, ElementTriP2, ElementVector, Basis, BilinearForm, LinearForm, asm, solve, condense
from common import C, INK2, SEQ, savefig, save_results

RES = {}
Rg = 8.314
Ea, n = 400e3, 3.0

def k_of_T(T, k0): return k0 * np.exp(-Ea / (Rg * T))

def dsc(beta_Kmin, k0, T0=600 + 273.15, T1=1200 + 273.15):
    beta = beta_Kmin / 60
    T = np.linspace(T0, T1, 20001)
    I = cumulative_trapezoid(k_of_T(T, k0) / beta, T, initial=0)
    X = 1 - np.exp(-I**n)
    dXdT = np.gradient(X, T)
    return T, X, dXdT

def part_a():
    k0 = brentq(lambda k0: dsc(10, k0)[0][np.argmax(dsc(10, k0)[2])] - (950 + 273.15), 1e10, 1e22)
    betas = [5, 10, 15, 20, 30]
    Tp = []
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0))
    for i, b in enumerate(betas):
        T, X, dX = dsc(b, k0)
        Tp.append(T[np.argmax(dX)])
        axs[0].plot(T - 273.15, dX * 100, color=C[i % 8], label=f"β={b} K/min")
    axs[0].set_xlabel("温度 (°C)"); axs[0].set_ylabel("dX/dT (%/K)（合成 DSC 放热峰）"); axs[0].legend(fontsize=8)
    axs[0].set_title(f"JMAK 非等温晶化（输入 Ea={Ea/1e3:.0f} kJ/mol, n={n:.0f}）"); axs[0].set_xlim(850, 1050)
    Tp = np.array(Tp); b = np.array(betas) / 60
    pK = np.polyfit(1 / Tp, np.log(b / Tp**2), 1); Ea_K = -pK[0] * Rg
    pO = np.polyfit(1 / Tp, np.log(b), 1); Ea_O = -pO[0] * Rg / 1.052
    axs[1].plot(1e3 / Tp, np.log(b / Tp**2), "o", color=C[0], label=f"Kissinger：Ea={Ea_K/1e3:.1f} kJ/mol")
    axs[1].plot(1e3 / Tp, np.polyval(pK, 1 / Tp), color=C[0], lw=1)
    axs[1].set_xlabel("1000 / T_p (1/K)"); axs[1].set_ylabel("ln(β / T_p²)")
    axs[1].set_title(f"验证11：Kissinger 反演误差 {abs(Ea_K-Ea)/Ea*100:.2f}%（Ozawa {abs(Ea_O-Ea)/Ea*100:.1f}%）")
    axs[1].legend(fontsize=8)
    savefig(fig, "s7_kissinger.png")
    RES["kissinger"] = dict(Ea_in=Ea, Ea_kissinger=Ea_K, Ea_ozawa=Ea_O, Tp_C=(Tp - 273.15).tolist(), k0=k0)
    print(RES["kissinger"])
    return k0

def part_b(k0):
    Th = np.array([830, 845, 860]) + 273.15
    t = np.linspace(0, 10 * 3600, 2000)
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.0))
    sens = {}
    for i, T in enumerate(Th):
        X = 1 - np.exp(-(k_of_T(T, k0) * t) ** n)
        dXdT = (1 - np.exp(-(k_of_T(T + 0.5, k0) * t) ** n) - (1 - np.exp(-(k_of_T(T - 0.5, k0) * t) ** n)))
        axs[0].plot(t / 3600, X, color=C[i], label=f"{T-273.15:.0f} °C 保温")
        axs[1].semilogy(t / 3600, np.abs(dXdT) * 2 + 1e-9, color=C[i], label=f"{T-273.15:.0f} °C：|∂X/∂T|·2K")
        sens[f"{T-273.15:.0f}C"] = dict(t_h=t[::100] / 3600, dX_2K=(np.abs(dXdT) * 2)[::100])
    axs[0].set_xlabel("保温时间 (h)"); axs[0].set_ylabel("晶化分数 X"); axs[0].legend(fontsize=8)
    axs[0].set_title("等温晶化动力学（JMAK）")
    axs[1].axhline(1e-3, color=INK2, ls="--", lw=1); axs[1].text(0.2, 1.3e-3, "δX=10⁻³ 目标", fontsize=8, color=INK2)
    axs[1].set_xlabel("保温时间 (h)"); axs[1].set_ylabel("±2 K 炉温不均引起的 δX"); axs[1].set_ylim(1e-8, 1)
    axs[1].set_title("“饱和晶化”策略：保温至平台区，敏感度下降数个量级"); axs[1].legend(fontsize=8)
    savefig(fig, "s7_isothermal.png")
    RES["isothermal"] = sens

# ---------- panel registration ----------
@BilinearForm
def ps_plane_stress(u, v, w):
    E, nu = w.E, w.nu
    eu = [u.grad[0][0], u.grad[1][1], u.grad[0][1] + u.grad[1][0]]
    ev = [v.grad[0][0], v.grad[1][1], v.grad[0][1] + v.grad[1][0]]
    c = E / (1 - nu**2)
    return c * (eu[0] * ev[0] + eu[1] * ev[1] + nu * (eu[0] * ev[1] + eu[1] * ev[0]) + (1 - nu) / 2 * eu[2] * ev[2])

@LinearForm
def ps_eig(v, w):
    E, nu = w.E, w.nu
    return E / (1 - nu) * w.eps * (v.grad[0][0] + v.grad[1][1])

def solve_panel(mesh, eps_fun, E=100e9, nu=0.25):
    basis = Basis(mesh, ElementVector(ElementTriP2()), intorder=4)
    A = asm(ps_plane_stress, basis, E=E, nu=nu)
    xq = basis.global_coordinates().value
    b = asm(ps_eig, basis, E=E, nu=nu, eps=eps_fun(xq))
    # remove rigid body: fix center point both, and one point's y
    xc = mesh.p.mean(axis=1)
    i0 = np.argmin(np.sum((mesh.p - xc[:, None]) ** 2, axis=0))
    i1 = np.argmin((mesh.p[0] - mesh.p[0].max()) ** 2 + (mesh.p[1] - xc[1]) ** 2)
    D = np.array([2 * i0, 2 * i0 + 1, 2 * i1 + 1])
    u = solve(*condense(A, b, D=D))
    return basis, u

def part_c(k0):
    eps_max = 0.005   # 0.5 % linear ceramming shrinkage at full crystallinity (assumed)
    # validation: disk with parabolic eigenstrain e(r) = e0 (1 - r^2/b^2): analytic plane-stress radial displacement
    b = 0.25; e0 = 1e-4; nu = 0.25
    m = MeshTri.init_circle(6).scaled((b, b))
    basis, u = solve_panel(m, lambda x: -e0 * (1 - (x[0] ** 2 + x[1] ** 2) / b**2), nu=nu)
    pts = basis.doflocs; ux = u[basis.nodal_dofs[0]]; uy = u[basis.nodal_dofs[1]]
    P = m.p; r = np.hypot(P[0], P[1]); ur_fem = (ux * P[0] + uy * P[1]) / np.maximum(r, 1e-12)
    # analytic (Timoshenko thin disk with "thermal" strain aT = -e(r)): u = (1+nu)/r int_0^r aT r dr + (1-nu) r/b^2 int_0^b aT r dr
    def u_an(rr):
        I_r = -e0 * (rr**2 / 2 - rr**4 / (4 * b**2)); I_b = -e0 * (b**2 / 2 - b**2 / 4)
        return (1 + nu) / np.maximum(rr, 1e-12) * I_r + (1 - nu) * rr / b**2 * I_b
    sel = r > 0.05 * b
    err = np.max(np.abs(ur_fem[sel] - u_an(r[sel]))) / np.max(np.abs(u_an(r[sel])))
    RES["disk_validation_maxrel"] = float(err)
    print("disk validation", err)
    # panel 510 x 515 mm with furnace non-uniformity (center hotter, parabolic), various hold times
    Lx, Ly = 0.510, 0.515
    mp = MeshTri.init_tensor(np.linspace(-Lx / 2, Lx / 2, 41), np.linspace(-Ly / 2, Ly / 2, 41))
    Th = 845 + 273.15
    holds = np.array([1, 1.5, 2, 3, 4, 6, 8, 10]) * 3600
    out = []
    for dTn in [1.0, 2.0, 5.0]:
        res = []
        for th in holds:
            def X_of(dTloc): return 1 - np.exp(-(k_of_T(Th + dTloc, k0) * th) ** n)
            X0 = X_of(0.0)
            eps = lambda x: -eps_max * (X_of(dTn * (1 - (x[0] ** 2 + x[1] ** 2) / (Lx / 2) ** 2)) - X0) - eps_max * X0
            basis, u = solve_panel(mp, eps)
            ux = u[basis.nodal_dofs[0]]; uy = u[basis.nodal_dofs[1]]; X, Y = mp.p
            # best-fit uniform scale (design pre-compensation) + rigid motion
            A_ = np.c_[np.r_[X, Y], np.r_[np.ones_like(X), np.zeros_like(X)], np.r_[np.zeros_like(Y), np.ones_like(Y)], np.r_[-Y, X]]
            coef, *_ = np.linalg.lstsq(A_, np.r_[ux, uy], rcond=None)
            resid = np.r_[ux, uy] - A_ @ coef
            res.append(np.abs(resid).max() * 1e6)
        out.append(res)
    out = np.array(out)
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for i, dTn in enumerate([1.0, 2.0, 5.0]):
        ax.semilogy(holds / 3600, out[i], "o-", color=C[i], label=f"炉温不均匀度 ±{dTn:.0f} K")
    ax.axhline(2.0, color=INK2, ls="--", lw=1); ax.text(3.2, 2.4, "套刻容差 ±2 µm（100 µm 节距）", fontsize=8, color=INK2)
    ax.set_xlabel("845 °C 保温时间 (h)"); ax.set_ylabel("面板最大残余套刻误差 (µm)")
    ax.set_title("510×515 mm 面板：先成孔后晶化的套刻误差（已扣除线性缩放补偿）"); ax.legend(fontsize=8)
    savefig(fig, "s7_panel_registration.png")
    RES["registration"] = dict(holds_h=holds / 3600, dT=[1, 2, 5], err_um=out, eps_max=eps_max)
    print(out)

if __name__ == "__main__":
    k0 = part_a(); part_b(k0); part_c(k0)
    save_results("s7_ceramming", RES)
