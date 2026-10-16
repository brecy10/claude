import sys, numpy as np
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib; matplotlib.use("Agg")
import s3_thermomech as S
from common import MAT, PHASE
a=S.a; h=S.h; gcf=MAT["GCF"]; w=5e-6
def collar_soft(r):
    s=np.clip((r-a)/w,0,1); sel=(r>=a)&(r<a+w)
    return np.where(sel,50e9+(gcf["E"]-50e9)*s,np.nan), np.where(sel,9e-6+(gcf["alpha"]-9e-6)*s,np.nan)
cases=[("GCF solid",dict()),("GCF+poly2um",dict(poly=(2e-6,MAT["POLY"]))),("GCF conformal8",dict(liner=8e-6)),("GCF soft collar",dict(collar=collar_soft))]
for name,kw in cases:
    m=S.make_model(gcf,**kw)
    m.run([25,400],nsub=12)
    sig=m.sig.reshape(-1,4); xy=m.gp_xy()
    sub=~np.repeat(m.is_cu,4)
    if hasattr(m,"is_void") and m.is_void is not None:
        pass
    st=sig[:,2]; s1=S.principal_max(sig)
    idx=np.where(sub)[0]
    i=idx[np.argmax(st[idx])]; j=idx[np.argmax(s1[idx])]
    mid=sub&(xy[:,1]<30e-6)
    # hoop vs r at midplane
    prof=[]
    for rr in [0.5,1.5,3,4.5,5.5,7,10,15]:
        sel=mid&(np.abs(xy[:,0]-(a+rr*1e-6))<0.8e-6)
        if sel.any(): prof.append((rr,round(st[sel].mean()/1e6,1)))
    print(name,"max hoop %.1f MPa at r-a=%.1f um, z=%.1f um (h=%.0f)"%(st[i]/1e6,(xy[i,0]-a)*1e6,xy[i,1]*1e6,h*1e6),
          "| max s1 %.1f at r-a=%.1f z=%.1f"%(s1[j]/1e6,(xy[j,0]-a)*1e6,xy[j,1]*1e6), "| midplane hoop profile (r-a um, MPa):",prof)
