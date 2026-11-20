import os,json,time
from urllib.request import urlopen,Request
from random import Random
# PeSTO tapered tables (a8..h1 order), middlegame / endgame.
MP=(0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-20,-20,10,10,5,0,0,0,0,0,0,0,0)
EP=(0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,30,30,30,30,30,30,30,30,20,20,20,20,20,20,20,20,10,10,10,10,10,10,10,10,5,5,5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
MN=(-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50)
MB=(-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20)
MR=(0,0,0,0,0,0,0,0,5,10,10,10,10,10,10,5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,-5,0,0,0,0,0,0,-5,0,0,0,5,5,0,0,0)
MQ=(-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20)
MK=(-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-30,-40,-40,-50,-50,-40,-40,-30,-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20)
EK=(-50,-40,-30,-20,-20,-30,-40,-50,-30,-20,-10,0,0,-10,-20,-30,-30,-10,20,30,30,20,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,20,30,30,20,-10,-30,-30,-30,0,0,0,0,-30,-30,-50,-30,-30,-30,-30,-30,-30,-50)
TB={1:(MP,EP),2:(MN,MN),3:(MB,MB),4:(MR,MR),5:(MQ,MQ),6:(MK,EK)}
V=(0,82,337,365,477,1025,0)
W=(0,0,1,1,2,4,0)
KN=(14,18,31,33,-14,-18,-31,-33)
KG=(1,15,16,17,-1,-15,-16,-17)
DG=(15,17,-15,-17)
SR=(1,16,-1,-16)
MATE=100000
BUD=120000
R=Random(20261119)
ZK=[[R.getrandbits(64) for _ in range(128)] for _ in range(13)]
ZS=R.getrandbits(64)
ZC=[R.getrandbits(64) for _ in range(16)]
ZE=[R.getrandbits(64) for _ in range(8)]
PM=[[0]*128 for _ in range(13)]
PE=[[0]*128 for _ in range(13)]
for _p in range(-6,7):
 if not _p:continue
 _mg,_eg=TB[abs(_p)]
 for _s in range(128):
  if _s&0x88:continue
  _f=_s&7;_r=_s>>4
  _i=((7-_r) if _p>0 else _r)*8+_f
  _g=1 if _p>0 else -1
  PM[_p+6][_s]=(V[abs(_p)]+_mg[_i])*_g
  PE[_p+6][_s]=(V[abs(_p)]+_eg[_i])*_g
B=[0]*128;S=0;C=0;E=-1;H=0;Z=0;MG=0;EG=0;PH=0;BC=[0,0];KS=[0,0]
GS=set();TT={};RP=set();ND=0;AB=0;EU=""
K1=[0]*256;K2=[0]*256;HS=[[0]*128 for _ in range(13)]
def F(fn):
 global B,S,C,E,H,Z,MG,EG,PH,BC,KS
 B=[0]*128;S=0;C=0;E=-1;H=0;Z=0;MG=0;EG=0;PH=0;BC=[0,0];KS=[0,0]
 q=fn.split();r=7
 for row in q[0].split('/'):
  f=0
  for ch in row:
   if ch.isdigit():f+=int(ch)
   else:
    p="PNBRQKpnbrqk".index(ch)+1
    v=p if p<7 else 6-p
    s=(r<<4)+f
    B[s]=v;MG+=PM[v+6][s];EG+=PE[v+6][s];Z^=ZK[v+6][s];PH+=W[abs(v)]
    if abs(v)==3:BC[0 if v>0 else 1]+=1
    if abs(v)==6:KS[0 if v>0 else 1]=s
    f+=1
  r-=1
 S=0 if q[1]=='w' else 1
 if S:Z^=ZS
 for ch in q[2]:
  if ch=='K':C|=1
  elif ch=='Q':C|=2
  elif ch=='k':C|=4
  elif ch=='q':C|=8
 Z^=ZC[C]
 if len(q)>3 and q[3]!='-':
  E=(ord(q[3][0])-97)+((int(q[3][1])-1)<<4);Z^=ZE[E&7]
 if len(q)>4:H=int(q[4])
def AT(q,by):
 if by==0:
  for d in (-15,-17):
   if not (q+d)&0x88 and B[q+d]==1:return 1
 else:
  for d in (15,17):
   if not (q+d)&0x88 and B[q+d]==-1:return 1
 for d in KN:
  x=q+d
  if not x&0x88 and B[x]==(2 if by==0 else -2):return 1
 for d in KG:
  x=q+d
  if not x&0x88 and B[x]==(6 if by==0 else -6):return 1
 for d in DG:
  x=q+d
  while not x&0x88:
   p=B[x]
   if p:
    if p==(3 if by==0 else -3) or p==(5 if by==0 else -5):return 1
    break
   x+=d
 for d in SR:
  x=q+d
  while not x&0x88:
   p=B[x]
   if p:
    if p==(4 if by==0 else -4) or p==(5 if by==0 else -5):return 1
    break
   x+=d
 return 0
def G(cap=0):
 ms=[]
 for s in range(128):
  if s&0x88:continue
  p=B[s]
  if not p or (p>0)!=(S==0):continue
  t=abs(p)
  if t==1:
   d=16 if S==0 else -16
   x=s+d
   if not x&0x88 and B[x]==0 and (not cap or (x>>4) in (0,7)):
    if (x>>4) in (0,7):
     for pr in (5,4,3,2):ms.append(s|(x<<7)|(pr<<14))
    else:
     ms.append(s|(x<<7))
     if ((S==0 and (s>>4)==1) or (S==1 and (s>>4)==6)) and B[s+2*d]==0:ms.append(s|((s+2*d)<<7))
   for dd in (d-1,d+1):
    x=s+dd
    if x&0x88:continue
    q=B[x]
    if q and (q>0)!=(S==0):
     if (x>>4) in (0,7):
      for pr in (5,4,3,2):ms.append(s|(x<<7)|(pr<<14))
     else:ms.append(s|(x<<7))
    elif x==E:ms.append(s|(x<<7))
  elif t==2 or t==6:
   for dd in (KN if t==2 else KG):
    x=s+dd
    if x&0x88:continue
    q=B[x]
    if cap and not q:continue
    if not q or (q>0)!=(S==0):ms.append(s|(x<<7))
   if t==6 and not cap:
    if S==0:
     if C&1 and not B[5] and not B[6] and B[7]==4 and not AT(4,1) and not AT(5,1) and not AT(6,1):ms.append(4|(6<<7))
     if C&2 and not B[3] and not B[2] and not B[1] and B[0]==4 and not AT(4,1) and not AT(3,1) and not AT(2,1):ms.append(4|(2<<7))
    else:
     if C&4 and not B[117] and not B[118] and B[119]==-4 and not AT(116,0) and not AT(117,0) and not AT(118,0):ms.append(116|(118<<7))
     if C&8 and not B[115] and not B[114] and not B[113] and B[112]==-4 and not AT(116,0) and not AT(115,0) and not AT(114,0):ms.append(116|(114<<7))
  else:
   for dd in (DG if t==3 else SR if t==4 else KG):
    x=s+dd
    while not x&0x88:
     q=B[x]
     if q:
      if (q>0)!=(S==0):ms.append(s|(x<<7))
      break
     if not cap:ms.append(s|(x<<7))
     x+=dd
 return ms
def M(m):
 global S,C,E,H,Z,MG,EG,PH
 f=m&127;t=(m>>7)&127;pr=m>>14
 p=B[f];cq=B[t];cs=t
 if abs(p)==1 and t==E and not cq:
  cs=t-16 if S==0 else t+16;cq=B[cs]
 rs=rd=-1
 if abs(p)==6 and t-f in (2,-2):
  rs,rd=(f+3,f+1) if t>f else (f-4,f-1)
 u=(m,cq,cs,rs,rd,C,E,H,Z,MG,EG,PH,BC[0],BC[1],KS[S])
 MG-=PM[p+6][f];EG-=PE[p+6][f];Z^=ZK[p+6][f];B[f]=0
 if cq:
  MG-=PM[cq+6][cs];EG-=PE[cq+6][cs];Z^=ZK[cq+6][cs];B[cs]=0;PH-=W[abs(cq)]
  if abs(cq)==3:BC[0 if cq>0 else 1]-=1
 if rs>=0:
  rp=B[rs];MG-=PM[rp+6][rs];EG-=PE[rp+6][rs];Z^=ZK[rp+6][rs];B[rs]=0
  B[rd]=rp;MG+=PM[rp+6][rd];EG+=PE[rp+6][rd];Z^=ZK[rp+6][rd]
 np=(pr if S==0 else -pr) if pr else p
 B[t]=np;MG+=PM[np+6][t];EG+=PE[np+6][t];Z^=ZK[np+6][t]
 if pr:
  PH+=W[pr]
  if pr==3:BC[S]+=1
 if abs(p)==6:KS[S]=t
 o=C
 if abs(p)==6:C&=~(3 if S==0 else 12)
 if f==7 or t==7:C&=~1
 if f==0 or t==0:C&=~2
 if f==119 or t==119:C&=~4
 if f==112 or t==112:C&=~8
 Z^=ZC[o]^ZC[C]
 if E>=0:Z^=ZE[E&7]
 E=(f+16 if S==0 else f-16) if abs(p)==1 and abs(t-f)==32 else -1
 if E>=0:Z^=ZE[E&7]
 H=0 if abs(p)==1 or cq else H+1
 Z^=ZS;S^=1
 return u
def U(u):
 global S,C,E,H,Z,MG,EG,PH
 m,cq,cs,rs,rd,C,E,H,Z,MG,EG,PH,b0,b1,ks=u
 f=m&127;t=(m>>7)&127;pr=m>>14
 S^=1
 p=B[t]
 mp=(1 if S==0 else -1) if pr else p
 B[t]=0
 if rs>=0:
  rp=B[rd];B[rd]=0;B[rs]=rp
 if cq:B[cs]=cq
 B[f]=mp
 if abs(mp)==6:KS[S]=ks
 BC[0]=b0;BC[1]=b1
def D():
 s=(MG*PH+EG*(24-PH))//24+8
 pr=(25*PH+40*(24-PH))//24
 s+=pr*((BC[0]>=2)-(BC[1]>=2))
 k=KS[0];s+=sum(B[q]==1 for q in(k+15,k+16,k+17)if not q&0x88)*PH//2
 k=KS[1];s-=sum(B[q]==-1 for q in(k-15,k-16,k-17)if not q&0x88)*PH//2
 return s if S==0 else -s
def O(m,pl):
 f=m&127;t=(m>>7)&127;pr=m>>14
 if pr:return 2000000+pr
 q=B[t]
 if q:return 1000000+V[abs(q)]*10-V[abs(B[f])]
 if t==E:return 900000
 if m==K1[pl]:return 800000
 if m==K2[pl]:return 700000
 return HS[B[f]+6][t]
def sg(s,pl):
 if s>MATE-1000:return s+pl
 if s<-MATE+1000:return s-pl
 return s
def T(d,a,b,pl):
 global ND,AB,E,H,Z,S
 ND+=1
 if ND>BUD:AB=1;return 0
 if H>=100 or Z in GS or Z in RP:return 0
 a=max(a,pl-MATE);b=min(b,MATE-pl)
 if a>=b:return a
 RP.add(Z)
 try:
  e=TT.get(Z);tm=0
  if e:
   tm=e[3]
   if e[0]>=d:
    s=e[2]
    if s>MATE-1000:s-=pl
    elif s<-MATE+1000:s+=pl
    if e[1]==0:return s
    if e[1]==1 and s>=b:return s
    if e[1]==2 and s<=a:return s
  kc=AT(KS[S],S^1)
  if d<=0:
   if pl>=100:return D()
   s=D()
   if not kc:
    if s>=b:return s
    if s>a:a=s
   ms=G(0 if kc else 1)
   ms.sort(key=lambda m:O(m,pl),reverse=True)
   fd=0
   for m in ms:
    u=M(m)
    if AT(KS[S^1],S):U(u);continue
    fd=1
    s=-T(0,-b,-a,pl+1);U(u)
    if AB:return 0
    if s>=b:return s
    if s>a:a=s
   if kc and not fd:return -MATE+pl
   return a
  if d>=3 and not kc and PH>0:
   s0=D()
   if s0>=b:
    oE,oH,oZ,oS=E,H,Z,S
    if E>=0:Z^=ZE[E&7]
    E=-1;H+=1;Z^=ZS;S^=1
    s=-T(d-4,-b,-b+1,pl+1)
    E,H,Z,S=oE,oH,oZ,oS
    if AB:return 0
    if s>=b:return s
  ms=G()
  ms.sort(key=lambda m:(m==tm)*10000000+O(m,pl),reverse=True)
  best=-MATE*2;bf=2;bm=0
  for i,m in enumerate(ms):
   t=(m>>7)&127;cp=B[t];pq=(m>>14);ep=(t==E)
   u=M(m)
   if AT(KS[S^1],S):U(u);continue
   ck=AT(KS[S],S^1)
   ex=1 if ck else 0
   if i==0:
    s=-T(d-1+ex,-b,-a,pl+1)
   else:
    rd=1 if d>=3 and i>=4 and not kc and not cp and not pq and not ep and not ck else 0
    s=-T(d-1+ex-rd,-a-1,-a,pl+1)
    if rd and s>a:s=-T(d-1+ex,-a-1,-a,pl+1)
    if s>a and s<b:s=-T(d-1+ex,-b,-a,pl+1)
   U(u)
   if AB:return 0
   if s>best:best=s;bm=m
   if s>=b:
    if not cp and not pq and not ep:
     if m!=K1[pl]:K2[pl]=K1[pl];K1[pl]=m
     HS[B[m&127]+6][t]+=d*d
    TT[Z]=(d,1,sg(s,pl),m);return s
   if s>a:a=s;bf=0
  if best==-MATE*2:return -MATE+pl if kc else 0
  TT[Z]=(d,bf,sg(best,pl),bm)
  return best
 finally:
  RP.discard(Z)
def sq(s):return chr(97+(s&7))+str((s>>4)+1)
def uc(m):
 f=m&127;t=(m>>7)&127;pr=m>>14
 return sq(f)+sq(t)+("nbrq"[pr-2] if pr else "")
def R(lm):
 global ND,AB
 ND=0;AB=0
 ms=[]
 for m in G():
  u=M(m)
  if AT(KS[S^1],S):U(u);continue
  U(u)
  if uc(m) in lm:ms.append(m)
 if not ms:return None
 if len(ms)==1:return ms[0]
 sc={m:0 for m in ms}
 best=ms[0];d=1
 while ND<BUD and d<65:
  ms.sort(key=lambda m:-sc[m])
  a=-MATE*2;bb=None
  for i,m in enumerate(ms):
   u=M(m)
   if i==0:s=-T(d-1,-MATE,MATE,1)
   else:
    s=-T(d-1,-a-1,-a,1)
    if s>a:s=-T(d-1,-MATE,MATE,1)
   U(u)
   if AB:break
   sc[m]=s
   if s>a:a=s;bb=m
  if AB:break
  if bb:best=bb
  if abs(sc[best])>=MATE-1000:break
  d+=1
 return best
def po(p,b):
 r=urlopen(Request(EU+p,data=json.dumps(b).encode()),timeout=30)
 return json.loads(r.read())
def go():
 global EU
 EU=os.getenv("MAKEFUN_ENV_URL","")
 for _ in range(6):
  if EU:break
  time.sleep(5);EU=os.getenv("MAKEFUN_ENV_URL","")
 if not EU:1/0
 pg=None
 while True:
  try:g=po("/game",{})
  except Exception:
   time.sleep(3);continue
  if g.get("status")=="done":return
  gn=g["game"]
  if gn!=pg:
   TT.clear();pg=gn
   for i in range(256):K1[i]=0;K2[i]=0
   for r in HS:
    for i in range(128):r[i]=0
  F(g["start_fen"]);GS.clear();GS.add(Z)
  for u in g["moves"]:
   f=(ord(u[0])-97)+((int(u[1])-1)<<4)
   t=(ord(u[2])-97)+((int(u[3])-1)<<4)
   pr=("nbrq".index(u[4])+2) if len(u)>4 else 0
   M(f|(t<<7)|(pr<<14));GS.add(Z)
  lm=set(g.get("legal_moves",[]))
  m=R(lm)
  if m is None:
   try:po("/resign",{"game":gn})
   except Exception:pass
   continue
  for _ in range(2):
   try:po("/move",{"game":gn,"move":uc(m)});break
   except Exception:
    lm.discard(uc(m));m=R(lm)
    if m is None:break
if __name__=="__main__":go()
