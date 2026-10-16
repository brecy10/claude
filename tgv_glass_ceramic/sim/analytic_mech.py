"""Closed-form / semi-analytical thermo-mechanical models used to cross-check FEM."""
import numpy as np

def lame_gps(a, R, cu, sub, dT, r_eval, mode="gps", b=None, mid=None):
    """Concentric cylinders: core (0<r<a, Cu) + annulus (a<r<R, substrate).
    mode='gps' generalized plane strain (free axial, zero net force) or 'pstrain'.
    Optional intermediate layer mid=(b, mat) between a and b (b<R) for graded/collar.
    Returns dict of sigma_r, sigma_t, sigma_z at r_eval (array)."""
    layers = [(0.0, a, cu)]
    if mid is not None:
        layers.append((a, mid[0], mid[1])); layers.append((mid[0], R, sub))
    else:
        layers.append((a, R, sub))
    nL = len(layers)
    # unknowns: A_i, B_i (B_0=0) , ez
    nun = 2 * nL + 1
    M = np.zeros((nun, nun)); rhs = np.zeros(nun)
    def coef(mat):
        E, nu, al = mat["E"], mat["nu"], mat["alpha"]
        lam = E * nu / ((1 + nu) * (1 - 2 * nu)); G = E / (2 * (1 + nu))
        return lam, G, al, 3 * lam + 2 * G
    def sr_row(i, r):
        lam, G, al, k3 = coef(layers[i][2])
        row = np.zeros(nun)
        row[2 * i] = 2 * (lam + G)          # A term: er=et=A
        row[2 * i + 1] = -2 * G / r**2      # B term
        row[-1] = lam
        return row, k3 * al * dT
    eq = 0
    M[eq, 1] = 1.0; eq += 1                 # B_0 = 0
    for i in range(nL - 1):
        r = layers[i][1]
        M[eq, 2 * i] = r; M[eq, 2 * i + 1] = 1 / r; M[eq, 2 * (i + 1)] = -r; M[eq, 2 * (i + 1) + 1] = -1 / r; eq += 1
        r1, c1 = sr_row(i, r); r2, c2 = sr_row(i + 1, r)
        M[eq] = r1 - r2; rhs[eq] = c1 - c2; eq += 1
    rl, cl = sr_row(nL - 1, R); M[eq] = rl; rhs[eq] = cl; eq += 1
    if mode == "gps":
        # net axial force: sum over layers of int sigma_z 2 pi r dr = 0
        row = np.zeros(nun); c = 0.0
        for i, (r0, r1, mat) in enumerate(layers):
            lam, G, al, k3 = coef(mat)
            area = np.pi * (r1**2 - r0**2)
            row[2 * i] += 2 * lam * area     # sigma_z = 2 lam A + (lam+2G) ez - k3 al dT (B terms cancel in er+et)
            row[-1] += (lam + 2 * G) * area
            c += k3 * al * dT * area
        M[eq] = row; rhs[eq] = c
    else:
        M[eq, -1] = 1.0; rhs[eq] = 0.0
    sol = np.linalg.solve(M, rhs)
    r_eval = np.atleast_1d(r_eval)
    out = {k: np.zeros_like(r_eval, dtype=float) for k in ("sr", "st", "sz")}
    for i, (r0, r1, mat) in enumerate(layers):
        lam, G, al, k3 = coef(mat)
        A, B, ez = sol[2 * i], sol[2 * i + 1], sol[-1]
        msk = (r_eval >= r0) & (r_eval <= r1) if i > 0 else (r_eval <= r1)
        rr = r_eval[msk]
        er = A - B / rr**2; et = A + B / rr**2
        out["sr"][msk] = lam * (er + et + ez) + 2 * G * er - k3 * al * dT
        out["st"][msk] = lam * (er + et + ez) + 2 * G * et - k3 * al * dT
        out["sz"][msk] = lam * (er + et + ez) + 2 * G * ez - k3 * al * dT
    out["ez"] = sol[-1]
    return out

def interface_pressure_infinite(cu, sub, dT):
    """Plane-strain Cu cylinder in infinite substrate: interface radial stress (negative = compression on heating)."""
    Ec, nc, ac = cu["E"], cu["nu"], cu["alpha"]
    Es, ns, as_ = sub["E"], sub["nu"], sub["alpha"]
    # plane strain: misfit (1+nu)alpha
    mis = ((1 + nc) * ac - (1 + ns) * as_) * dT
    comp = (1 + nc) * (1 - 2 * nc) / Ec + (1 + ns) / Es
    return -mis / comp

def K_edge_crack_wf(sig_fun, c, n=4000):
    """Edge-crack Green's function (Tada et al.) applied to crack-line stress sig_fun(x), x from mouth.
    K = 2/sqrt(pi c) * int_0^c sig(x) [1.3-0.3 (x/c)^1.25] / sqrt(1-(x/c)^2) dx"""
    th = np.linspace(0, np.pi / 2, n)[:-1] + np.pi / 4 / n
    x = c * np.sin(th)
    g = 1.3 - 0.3 * (x / c) ** 1.25
    # dx/sqrt(1-(x/c)^2) = c dtheta
    integrand = sig_fun(x) * g * c
    return 2 / np.sqrt(np.pi * c) * np.trapezoid(integrand, th)

def K_hole_radial_crack(sig0, a, c, n=4000):
    """Radial crack of length c from a hole of radius a in hoop field sig0 (a/r)^2 (Lame decay)."""
    return K_edge_crack_wf(lambda x: sig0 * (a / (a + x)) ** 2, c, n)
