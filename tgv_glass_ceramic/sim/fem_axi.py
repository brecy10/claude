"""In-house axisymmetric Q4 finite-element code (B-bar, J2 plasticity with linear
kinematic hardening and temperature-dependent yield) for a Cu-filled TGV in a
substrate unit cell.  Strain/stress Voigt order: [rr, zz, tt, rz] (engineering rz)."""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

def graded(x0, x1, n, ratio):
    """n intervals from x0 to x1, last/first interval ratio = ratio (>1 refines toward x1)."""
    if abs(ratio - 1) < 1e-9:
        return np.linspace(x0, x1, n + 1)
    q = ratio ** (-1.0 / (n - 1))          # successive shrink factor
    h = q ** np.arange(n); h = h / h.sum() * (x1 - x0)
    return np.concatenate([[x0], x0 + np.cumsum(h)])

class AxiTGV:
    def __init__(self, a, R, h, nr_cu=16, nr_s=40, nz=48, tied_outer=False, liner=None):
        """a: via radius, R: outer radius, h: half thickness (z in [0,h], z=h top surface).
        liner: None (full fill) or Cu liner thickness -> r<a-liner is void/polymer core."""
        self.a, self.R, self.h = a, R, h
        r = np.concatenate([graded(0, a, nr_cu, 6.0), graded(a, R, nr_s, 1 / 60.0)[1:]])
        z = graded(0, h, nz, 25.0)
        self.r, self.z = r, z
        Rr, Zz = np.meshgrid(r, z, indexing="ij")
        self.X = np.c_[Rr.ravel(), Zz.ravel()]
        nr, nzz = len(r), len(z)
        idx = np.arange(nr * nzz).reshape(nr, nzz)
        e = []
        for i in range(nr - 1):
            for j in range(nzz - 1):
                e.append([idx[i, j], idx[i + 1, j], idx[i + 1, j + 1], idx[i, j + 1]])
        self.E = np.array(e)
        self.idx = idx
        self.nn = len(self.X); self.ndof = 2 * self.nn
        self.tied_outer = tied_outer
        self.liner = liner
        self._precompute()

    def _precompute(self):
        g = 1 / np.sqrt(3)
        gp = np.array([[-g, -g], [g, -g], [g, g], [-g, g]])
        Xe = self.X[self.E]                                    # (Ne,4,2)
        Ne = len(self.E)
        B = np.zeros((Ne, 4, 4, 8)); W = np.zeros((Ne, 4)); RZ = np.zeros((Ne, 4, 2))
        Bvol = np.zeros((Ne, 4, 8))
        for q, (xi, et) in enumerate(gp):
            N = 0.25 * np.array([(1 - xi) * (1 - et), (1 + xi) * (1 - et), (1 + xi) * (1 + et), (1 - xi) * (1 + et)])
            dN = 0.25 * np.array([[-(1 - et), -(1 - xi)], [(1 - et), -(1 + xi)], [(1 + et), (1 + xi)], [-(1 + et), (1 - xi)]])
            J = np.einsum("eia,ib->eab", Xe, dN)              # (Ne,2,2)
            detJ = J[:, 0, 0] * J[:, 1, 1] - J[:, 0, 1] * J[:, 1, 0]
            Jinv = np.linalg.inv(J)
            dNx = np.einsum("ib,eba->eia", dN, Jinv)          # (Ne,4,2) d/dr, d/dz
            rq = Xe[:, :, 0] @ N; zq = Xe[:, :, 1] @ N
            RZ[:, q, 0], RZ[:, q, 1] = rq, zq
            W[:, q] = detJ * 2 * np.pi * rq
            for i in range(4):
                B[:, q, 0, 2 * i] = dNx[:, i, 0]
                B[:, q, 1, 2 * i + 1] = dNx[:, i, 1]
                B[:, q, 2, 2 * i] = N[i] / rq
                B[:, q, 3, 2 * i] = dNx[:, i, 1]
                B[:, q, 3, 2 * i + 1] = dNx[:, i, 0]
                Bvol[:, q, 2 * i] = dNx[:, i, 0] + N[i] / rq
                Bvol[:, q, 2 * i + 1] = dNx[:, i, 1]
        Vol = W.sum(1)
        Bbar_vol = np.einsum("eq,eqk->ek", W, Bvol) / Vol[:, None]
        m = np.array([1, 1, 1, 0.0])
        self.B = B + (1 / 3) * m[None, None, :, None] * (Bbar_vol[:, None, None, :] - Bvol[:, :, None, :])
        self.W, self.RZ = W, RZ
        dofs = np.zeros((Ne, 8), dtype=int)
        dofs[:, 0::2] = 2 * self.E; dofs[:, 1::2] = 2 * self.E + 1
        self.dofs = dofs
        self.rows = np.repeat(dofs, 8, axis=1).ravel(); self.cols = np.tile(dofs, (1, 8)).ravel()
        cen = self.X[self.E].mean(1)
        self.cen = cen
        # region flags
        self.is_cu = cen[:, 0] < self.a
        if self.liner is not None:
            self.is_void = cen[:, 0] < self.a - self.liner
        else:
            self.is_void = np.zeros(Ne, bool)
        # boundary conditions
        fixed = list(2 * self.idx[0, :])                      # ur=0 on axis
        fixed += list(2 * self.idx[:, 0] + 1)                 # uz=0 at mid-plane
        self.fixed = np.unique(fixed)
        free = np.setdiff1d(np.arange(self.ndof), self.fixed)
        # transformation for tied outer radial dof
        if self.tied_outer:
            outer = 2 * self.idx[-1, :]
            master = outer[0]
            T = sp.lil_matrix((self.ndof, self.ndof))
            oset = set(outer.tolist())
            for d in range(self.ndof):
                if d in oset:
                    T[d, master] = 1.0
                else:
                    T[d, d] = 1.0
            keep = np.setdiff1d(free, outer[1:])
            self.T = T.tocsr()[:, keep]
        else:
            self.T = sp.eye(self.ndof, format="csr")[:, free]

    def set_materials(self, sub, cu, collar=None, void=None, poly_liner=None):
        """sub/cu: dicts with E, nu, alpha; Cu: sy0, sy400, Hk.  collar: function r-> (E,alpha)
        for substrate graded zone. void: dict for liner core filling (polymer) or None (empty)."""
        Ne = len(self.E)
        r = self.RZ[..., 0]
        E = np.full((Ne, 4), sub["E"]); nu = np.full((Ne, 4), sub["nu"]); al = np.full((Ne, 4), sub["alpha"])
        if collar is not None:
            Ec, ac = collar(r)
            sel = (~self.is_cu)[:, None] & np.isfinite(Ec)
            E = np.where(sel, Ec, E); al = np.where(sel, ac, al)
        cu_m = self.is_cu[:, None] & np.ones((1, 4), bool)
        E = np.where(cu_m, cu["E"], E); nu = np.where(cu_m, cu["nu"], nu); al = np.where(cu_m, cu["alpha"], al)
        if self.liner is not None:
            vm = self.is_void[:, None] & np.ones((1, 4), bool)
            vd = void if void is not None else dict(E=1e6, nu=0.3, alpha=0.0)
            E = np.where(vm, vd["E"], E); nu = np.where(vm, vd["nu"], nu); al = np.where(vm, vd["alpha"], al)
            cu_m = cu_m & ~vm
        if poly_liner is not None:
            tl, pm = poly_liner
            pmask = (self.is_cu & (self.cen[:, 0] > self.a - tl))[:, None] & np.ones((1, 4), bool)
            E = np.where(pmask, pm["E"], E); nu = np.where(pmask, pm["nu"], nu); al = np.where(pmask, pm["alpha"], al)
            cu_m = cu_m & ~pmask
        self.Eg, self.nug, self.alg = E, nu, al
        self.plastic = cu_m
        self.cu = cu
        self.Kg = E / (3 * (1 - 2 * nu)); self.Gg = E / (2 * (1 + nu))

    def sy(self, T):
        c = self.cu
        slope = (c["sy0"] - c["sy400"]) / (400 - 25)
        return np.maximum(c["sy0"] - slope * (T - 25), 20e6)

    def _increment(self, u, eps_p, beta, T, T0, elastic, tol, maxit=25, verbose=False):
        """One implicit increment to temperature T from committed state. Returns (ok, u, sig, dg, n)."""
        P, m, Cel, H = self._P, self._m, self._Cel, self.cu["Hk"]
        dT = T - T0
        eth = self.alg[..., None] * dT * m
        syT = self.sy(T)
        Gq = self.Gg
        ep_eng = eps_p.copy(); ep_eng[..., 3] *= 2
        n0 = None
        for it in range(maxit):
            ue = u[self.dofs]
            eps = np.einsum("eqik,ek->eqi", self.B, ue, optimize=True)
            sig_tr = np.einsum("eqij,eqj->eqi", Cel, eps - ep_eng - eth)
            s_dev = sig_tr - (sig_tr[..., :3].sum(-1, keepdims=True) / 3) * m
            xi = s_dev - beta
            nrm = np.sqrt(xi[..., 0]**2 + xi[..., 1]**2 + xi[..., 2]**2 + 2 * xi[..., 3]**2) + 1e-30
            f = nrm - np.sqrt(2 / 3) * syT
            yl = (f > 0) & self.plastic & (not elastic)
            dg = np.where(yl, f / (2 * Gq + 2 / 3 * H), 0.0)
            n = xi / nrm[..., None]
            sig = sig_tr - (2 * Gq * dg)[..., None] * n
            fint_e = np.einsum("eqik,eqi->ek", self.B, sig * self.W[..., None], optimize=True)
            fint = np.bincount(self.dofs.ravel(), fint_e.ravel(), minlength=self.ndof)
            Rr = self.T.T @ (-fint)
            nr = np.linalg.norm(Rr)
            # force scale: thermal load magnitude
            if n0 is None: n0 = max(nr, self._fscale * 1e-3)
            if verbose: print("   it", it, nr, nr / n0)
            if nr / n0 < tol or nr < 1e-10 * self._fscale:
                return True, u, sig, dg, n
            th = 1 - 2 * Gq * dg / nrm
            thb = 1 / (1 + H / (3 * Gq)) - (1 - th)
            corr = (2 * Gq * (th - 1))[..., None, None] * P[None, None] - (2 * Gq * thb)[..., None, None] * np.einsum("eqi,eqj->eqij", n, n)
            Ct = np.where(yl[..., None, None], Cel + corr, Cel)
            CB = np.einsum("eqij,eqjl->eqil", Ct, self.B, optimize=True) * self.W[..., None, None]
            Ke = np.einsum("eqik,eqil->ekl", self.B, CB, optimize=True)
            Kg = sp.coo_matrix((Ke.ravel(), (self.rows, self.cols)), shape=(self.ndof, self.ndof)).tocsr()
            Kr = (self.T.T @ Kg @ self.T).tocsc()
            du = spla.spsolve(Kr, Rr)
            u = u + self.T @ du
        return False, u, sig, dg, n

    def run(self, Tpath, T0=25.0, nsub=10, record=None, elastic=False, tol=1e-6, verbose=False):
        Ne = len(self.E)
        self._P = np.array([[2/3, -1/3, -1/3, 0], [-1/3, 2/3, -1/3, 0], [-1/3, -1/3, 2/3, 0], [0, 0, 0, 0.5]])
        self._m = m = np.array([1, 1, 1, 0.0])
        K, G = self.Kg[..., None, None], self.Gg[..., None, None]
        self._Cel = K * np.outer(m, m) + 2 * G * self._P
        self._fscale = float(np.abs(3 * self.Kg * self.alg).max() * 100 * self.W.sum() / self.h)
        eps_p = np.zeros((Ne, 4, 4)); beta = np.zeros((Ne, 4, 4))
        u = np.zeros(self.ndof)
        self.pacc = np.zeros((Ne, 4))
        H = self.cu["Hk"]
        hist = []
        self.n_cuts = 0
        temps = []
        for k in range(1, len(Tpath)):
            for s in range(1, nsub + 1):
                temps.append(Tpath[k - 1] + (Tpath[k] - Tpath[k - 1]) * s / nsub)
        Tprev = T0
        for Tt in temps:
            stack = [Tt]; Tcur = Tprev
            while stack:
                Tn = stack[-1]
                ok, u_new, sig, dg, n = self._increment(u, eps_p, beta, Tn, T0, elastic, tol, verbose=verbose)
                if not ok and abs(Tn - Tcur) > 0.05:
                    stack.append(0.5 * (Tcur + Tn)); self.n_cuts += 1
                    continue
                stack.pop()
                u = u_new
                eps_p = eps_p + dg[..., None] * n
                beta = beta + (2 / 3 * H * dg)[..., None] * n
                self.pacc = self.pacc + np.sqrt(2 / 3) * dg
                Tcur = Tn
            Tprev = Tt
            self.u, self.sig, self.eps_p, self.T_now = u, sig, eps_p, Tt
            if record is not None:
                hist.append(record(self, Tt))
        return hist

    # ---- post-processing helpers ----
    def gp_xy(self):
        return self.RZ.reshape(-1, 2)

    def field(self, comp):
        return self.sig[..., comp].reshape(-1)

    def peq_cu(self):
        e = self.eps_p
        return np.sqrt(2 / 3 * (e[..., 0]**2 + e[..., 1]**2 + e[..., 2]**2 + 2 * e[..., 3]**2))

    def node_u(self):
        return self.u.reshape(-1, 2)
