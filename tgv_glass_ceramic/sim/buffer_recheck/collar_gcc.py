import sys, numpy as np
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import matplotlib; matplotlib.use("Agg")
import s3_thermomech as S
from common import MAT
a=S.a; gcf=MAT["GCC"]
def mk(Ein,ain,w):
    def col(r):
        s=np.clip((r-a)/w,0,1); sel=(r>=a)&(r<a+w)
        return np.where(sel,Ein+(gcf["E"]-Ein)*s,np.nan), np.where(sel,ain+(gcf["alpha"]-ain)*s,np.nan)
    return col
variants=[("none",None),("E50 a9 w5",mk(50e9,9e-6,5e-6)),("E50 a3.5 w5",mk(50e9,3.5e-6,5e-6)),("E20 a3.5 w12.5",mk(20e9,3.5e-6,12.5e-6)),("E20 a9 w12.5",mk(20e9,9e-6,12.5e-6)),("E20 a13 w12.5",mk(20e9,13e-6,12.5e-6))]
for name,col in variants:
    m=S.make_model(gcf,collar=col)
    best={"st":-1e30,"s1":-1e30}; loc={}
    def rec(m_,T):
        sig=m_.sig.reshape(-1,4); xy=m_.gp_xy(); sub=~np.repeat(m_.is_cu,4)
        st=sig[:,2]; s1=S.principal_max(sig); idx=np.where(sub)[0]
        i=idx[np.argmax(st[idx])]; j=idx[np.argmax(s1[idx])]
        if st[i]>best["st"]: best["st"]=st[i]; loc["st"]=((xy[i,0]-a)*1e6,xy[i,1]*1e6,T)
        if s1[j]>best["s1"]: best["s1"]=s1[j]; loc["s1"]=((xy[j,0]-a)*1e6,xy[j,1]*1e6,T)
        ring=sub&(xy[:,0]<a+1.5e-6)
        return dict(sr=sig[ring,0].max(), mid=st[ring&(xy[:,1]<30e-6)].mean())
    hist=m.run([25,400,25],nsub=12,record=rec)
    print(f"{name:26s} global max hoop {best['st']/1e6:6.1f} MPa @ (r-a={loc['st'][0]:.1f},z={loc['st'][1]:.0f},T={loc['st'][2]:.0f}) | max s1 {best['s1']/1e6:6.1f} @ (r-a={loc['s1'][0]:.1f},z={loc['s1'][1]:.0f}) | near-wall mid hoop {max(hh['mid'] for hh in hist)/1e6:6.1f} | resid sr_int {hist[-1]['sr']/1e6:6.1f}")
