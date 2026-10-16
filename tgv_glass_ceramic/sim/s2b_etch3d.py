"""S2b: 3-D check of the selectivity amplification (2-D sections overstate crystal blocking because
the residual-glass network percolates much more easily in 3-D)."""
import numpy as np, skfmm
from common import save_results
rng = np.random.default_rng(11)

def micro3d(n, dx, d, f):
    L = n * dx; r = d / 2
    lam = -np.log(1 - f) / (4 / 3 * np.pi * r**3)
    N = rng.poisson(lam * (L + 2 * d) ** 3)
    c = rng.uniform(-d, L + d, (N, 3))
    g = np.zeros((n, n, n), bool); x = (np.arange(n) + 0.5) * dx
    for p in c:
        i0 = [max(0, int((p[k] - r) / dx)) for k in range(3)]; i1 = [min(n, int((p[k] + r) / dx) + 2) for k in range(3)]
        if any(a >= b for a, b in zip(i0, i1)): continue
        X, Y, Z = np.meshgrid(x[i0[0]:i1[0]], x[i0[1]:i1[1]], x[i0[2]:i1[2]], indexing="ij")
        g[i0[0]:i1[0], i0[1]:i1[1], i0[2]:i1[2]] |= (X - p[0])**2 + (Y - p[1])**2 + (Z - p[2])**2 <= r * r
    return g

def amp(n, dx, d, f, rho):
    cr = micro3d(n, dx, d, f)
    speed = np.where(cr, 1.0, rho); phi = np.ones(cr.shape); phi[0] = -1
    T = skfmm.travel_time(phi, speed, dx=dx, order=1)
    depth = 0.6 * n * dx
    # time for the mean first-solid surface to reach 'depth'
    lo, hi = 0.0, float(T.max())
    for _ in range(40):
        mid = (lo + hi) / 2
        xs = np.argmax(T > mid, axis=0) * dx
        if xs.mean() < depth: lo = mid
        else: hi = mid
    return rho / (depth / hi), cr.mean()

res = {}
for rho in (10, 30):
    for f in (0.5, 0.7, 0.8):
        a, fa = amp(120, 0.005, 0.06, f, rho)
        res[f"rho{rho}_f{f}"] = dict(amp=a, f_actual=fa)
        print(rho, f, round(fa, 3), round(a, 3))
save_results("s2b_etch3d", res)
