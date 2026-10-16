import sys, numpy as np
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib; matplotlib.use("Agg")
import s3_thermomech as S
from common import MAT
a=S.a; gcf=MAT["GCF"]
for name,kw in [("solid",{}),("conformal8",dict(liner=8e-6)),("conformal4",dict(liner=4e-6)),("conformal12",dict(liner=12e-6))]:
    m=S.make_model(gcf,**kw); m.run([25,400,25],nsub=12)
    sig=m.sig.reshape(-1,4); xy=m.gp_xy(); sub=~np.repeat(m.is_cu,4)
    ring=sub&(xy[:,0]<a+1.5e-6); idx=np.where(ring)[0]; i=idx[np.argmax(sig[idx,0])]
    mid=ring&(xy[:,1]<30e-6); deep=ring&(xy[:,1]<130e-6)
    print(f"{name:12s} resid sr max {sig[i,0]/1e6:6.1f} MPa at z={xy[i,1]*1e6:.1f} (surface=150) | midplane sr {sig[mid,0].mean()/1e6:6.1f} | max sr below z<130um {sig[deep,0].max()/1e6:6.1f}")
