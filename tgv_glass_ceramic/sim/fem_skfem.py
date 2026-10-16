"""Independent FEM implementations with scikit-fem (quadratic P2 triangles) used to
cross-validate the in-house Q4 code and to compute crack energy release rates."""
import numpy as np
from skfem import (MeshTri, ElementTriP2, ElementTriP0, ElementVector, Basis,
                   BilinearForm, LinearForm, asm, solve, condense)

def lame_coefs(E, nu):
    lam = E * nu / ((1 + nu) * (1 - 2 * nu)); G = E / (2 * (1 + nu)); K = lam + 2 / 3 * G
    return lam, G, K

def p0_field(basis, vals):
    b0 = basis.with_element(ElementTriP0())
    return b0.interpolate(vals)

# ---------------- axisymmetric thermo-elastic ----------------
@BilinearForm
def axi_stiff(u, v, w):
    r = w.x[0]
    eu = [u.grad[0][0], u.grad[1][1], u.value[0] / r, u.grad[0][1] + u.grad[1][0]]
    ev = [v.grad[0][0], v.grad[1][1], v.value[0] / r, v.grad[0][1] + v.grad[1][0]]
    tru = eu[0] + eu[1] + eu[2]; trv = ev[0] + ev[1] + ev[2]
    return (w.lam * tru * trv + 2 * w.G * (eu[0] * ev[0] + eu[1] * ev[1] + eu[2] * ev[2] + 0.5 * eu[3] * ev[3])) * r

@LinearForm
def axi_therm(v, w):
    r = w.x[0]
    ev = [v.grad[0][0], v.grad[1][1], v.value[0] / r]
    return 3 * w.K * w.alpha * w.dT * (ev[0] + ev[1] + ev[2]) * r

def axi_solve(r_nodes, z_nodes, mat_of_elem, dT):
    """mat_of_elem(centroids)-> (E, nu, alpha) arrays per element."""
    m = MeshTri.init_tensor(r_nodes, z_nodes)
    basis = Basis(m, ElementVector(ElementTriP2()), intorder=4)
    cen = m.p[:, m.t].mean(axis=1)
    E, nu, al = mat_of_elem(cen)
    lam, G, K = lame_coefs(E, nu)
    fw = dict(lam=p0_field(basis, lam), G=p0_field(basis, G), K=p0_field(basis, K), alpha=p0_field(basis, al), dT=dT)
    A = asm(axi_stiff, basis, **fw)
    b = asm(axi_therm, basis, **fw)
    D = np.concatenate([basis.get_dofs(lambda x: np.isclose(x[0], 0.0)).all('u^1'),
                        basis.get_dofs(lambda x: np.isclose(x[1], 0.0)).all('u^2')])
    u = solve(*condense(A, b, D=D))
    # stresses at quadrature points
    uh = basis.interpolate(u)
    x = basis.global_coordinates().value  # (2, ne, nq)
    r = x[0]
    er, ez, et, grz = uh.grad[0][0], uh.grad[1][1], uh.value[0] / r, uh.grad[0][1] + uh.grad[1][0]
    lq, Gq, Kq, aq = fw['lam'].value, fw['G'].value, fw['K'].value, fw['alpha'].value
    tr = er + ez + et
    th = 3 * Kq * aq * dT
    sig = dict(sr=lq * tr + 2 * Gq * er - th, sz=lq * tr + 2 * Gq * ez - th,
               st=lq * tr + 2 * Gq * et - th, srz=Gq * grz)
    return dict(mesh=m, basis=basis, u=u, x=x, sig=sig)

# ---------------- plane-strain thermo-elastic with symmetry crack ----------------
@BilinearForm
def ps_stiff(u, v, w):
    eu = [u.grad[0][0], u.grad[1][1], u.grad[0][1] + u.grad[1][0]]
    ev = [v.grad[0][0], v.grad[1][1], v.grad[0][1] + v.grad[1][0]]
    tru = eu[0] + eu[1]; trv = ev[0] + ev[1]
    return w.lam * tru * trv + 2 * w.G * (eu[0] * ev[0] + eu[1] * ev[1] + 0.5 * eu[2] * ev[2])

@LinearForm
def ps_therm(v, w):
    # plane strain: thermal stress 3K alpha dT acting on in-plane trace
    return 3 * w.K * w.alpha * w.dT * (v.grad[0][0] + v.grad[1][1])

def halfdisk_mesh(a, Rout, c_max, n_ang=72, refine=1):
    """Half-disk (y>=0) triangular mesh with radial grading near r=a and fine crack-line
    nodes on y=0 between a and a+c_max."""
    from scipy.spatial import Delaunay
    # radial stations
    r_in = a * (1 - np.geomspace(1, 1e-3, 18))[::-1]  # inside Cu (toward a)
    r_in = np.unique(np.r_[0.0, a * np.linspace(0.1, 0.9, 6), a * (1 - np.geomspace(0.1, 0.002, 10))])
    r_crack = a + np.linspace(0, c_max * 1.5, int(240 * refine) + 1)[1:]
    r_out = a + c_max * 1.5 + (Rout - a - c_max * 1.5) * (np.geomspace(1, 51, 30) - 1) / 50
    rs = np.unique(np.r_[r_in, a, r_crack, r_out[1:]])
    pts = [[0.0, 0.0]]
    for r in rs[1:]:
        # angular resolution proportional to r but bounded
        n = int(np.clip(np.pi * r / max(1e-12, np.diff(rs).max() if r > a + 1.5 * c_max else (rs[1] if r < a else c_max * 1.5 / (240 * refine)) * 4), 12, n_ang * 6))
        n = int(np.clip(n, 12, 900))
        th = np.linspace(0, np.pi, n + 1)
        pts += [[r * np.cos(t), r * np.sin(t)] for t in th]
    P = np.array(pts)
    tri = Delaunay(P)
    T = tri.simplices
    # drop slivers outside half-disk (none expected) & orient
    m = MeshTri(P.T.copy(), T.T.copy())
    return m

def crack_energy(a, Rout, cu, sub, dT, c_list, refine=1.0):
    """Stored elastic energy of full body (2x half model) vs crack length c, plane strain.
    Returns c_list, U(c), G=-dU/dc (central differences)."""
    cmax = max(c_list) * 1.05
    m = halfdisk_mesh(a, Rout, cmax, refine=refine)
    basis = Basis(m, ElementVector(ElementTriP2()), intorder=4)
    cen = m.p[:, m.t].mean(axis=1)
    rr = np.hypot(cen[0], cen[1])
    isc = rr < a
    E = np.where(isc, cu["E"], sub["E"]); nu = np.where(isc, cu["nu"], sub["nu"]); al = np.where(isc, cu["alpha"], sub["alpha"])
    lam, G, K = lame_coefs(E, nu)
    fw = dict(lam=p0_field(basis, lam), G=p0_field(basis, G), K=p0_field(basis, K), alpha=p0_field(basis, al), dT=dT)
    A = asm(ps_stiff, basis, **fw)
    b = asm(ps_therm, basis, **fw)
    dofs_y0 = basis.get_dofs(lambda x: np.isclose(x[1], 0.0))
    # node coordinates of y0 dofs (nodal + facet midpoints)
    y_n = dofs_y0.nodal['u^2']; y_f = dofs_y0.facet['u^2']
    xn = basis.doflocs[0, y_n]; xf = basis.doflocs[0, y_f]
    ux_center = basis.get_dofs(lambda x: np.isclose(x[0], 0.0) & np.isclose(x[1], 0.0)).nodal['u^1']
    out = []
    # thermal initial-strain energy: U = 1/2 u^T A u - u^T b + U0 where U0 = 1/2 int eth:C:eth
    for c in c_list:
        crack = lambda x: (x > a + 1e-12) & (x < a + c - 1e-12)
        D = np.concatenate([y_n[~crack(xn)], y_f[~crack(xf)], ux_center])
        u = solve(*condense(A, b, D=D))
        Pi = 0.5 * u @ (A @ u) - u @ b
        out.append(2 * Pi)  # full body (two symmetric halves), per unit thickness (U0 const omitted)
    out = np.array(out)
    return np.array(c_list), out, m
