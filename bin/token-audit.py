#!/usr/bin/env python3
"""Where do my Claude Code tokens go? Read-only replay of ~/.claude/projects transcripts, last 14 days.

Prices are API-equivalent $/MTok from platform.claude.com/docs/en/about-claude/pricing (checked 2026-10-15)
and WILL go stale: re-check the PR table below before trusting the dollar figures. Subscription usage caps
are not published as a formula, so $ is a proxy. The policy replays (fresh start after idle, earlier
compaction, Opus->Sonnet) are what-ifs on past calls: they ignore quality and any extra turns they cause.
Run: python3 -I bin/token-audit.py
"""
import json,glob,os,collections,datetime as dt
R=os.path.expanduser("~/.claude/projects")
cut=dt.datetime.now(dt.timezone.utc)-dt.timedelta(days=14)
P=lambda s: dt.datetime.fromisoformat(s.replace("Z","+00:00"))
# $/MTok from platform.claude.com pricing page (fetched 2026-10-15): input, write5m, write1h, read, output
PR={"claude-opus-5-5":(4,5,8,.20,20),"claude-opus-5":(5,6.25,10,.5,25),"claude-sonnet-5-5":(2,2.5,4,.10,10),
    "claude-sonnet-5":(2,2.5,4,.20,10),"claude-haiku-4-5-20251001":(1,1.25,2,.1,5)}
def price(model): return PR.get(model,PR["claude-sonnet-5"])
def parts(u):
    cc=u.get("cache_creation") or {}
    w1=cc.get("ephemeral_1h_input_tokens",0); w5=cc.get("ephemeral_5m_input_tokens",0)
    if not cc: w5=u.get("cache_creation_input_tokens",0)
    return u.get("input_tokens",0),u.get("cache_read_input_tokens",0),w5,w1,u.get("output_tokens",0)
def dollars(u,model,rd=None,w1=None,w5=None):
    i,r,a,b,o=parts(u); p=price(model)
    r=r if rd is None else rd; a=a if w5 is None else w5; b=b if w1 is None else w1
    return (i*p[0]+a*p[1]+b*p[2]+r*p[3]+o*p[4])/1e6
S=[]
for path in glob.glob(R+"/*/*.jsonl"):
    msgs={}
    for l in open(path):
        try:o=json.loads(l)
        except:continue
        m=o.get("message") or {}
        if o.get("type")!="assistant" or not m.get("usage") or not o.get("timestamp"):continue
        t=P(o["timestamp"])
        if t<cut: continue
        k=m.get("id") or o.get("uuid"); u=m["usage"]
        if k not in msgs or u.get("output_tokens",0)>=msgs[k][1].get("output_tokens",0): msgs[k]=(t,u,m.get("model","?"))
    if msgs: S.append(sorted(msgs.values(),key=lambda x:x[0]))
tot=sum(dollars(u,m) for r in S for t,u,m in r)
comp=collections.Counter(); bym=collections.Counter()
for r in S:
    for t,u,m in r:
        i,rd,a,b,o=parts(u); p=price(m)
        comp["cache read"]+=rd*p[3]/1e6; comp["cache write"]+=(a*p[1]+b*p[2])/1e6; comp["output"]+=o*p[4]/1e6; comp["input"]+=i*p[0]/1e6
        bym[m]+=dollars(u,m)
print(f"LAST 14 DAYS  API-equivalent ${tot:,.0f}  ({sum(len(r) for r in S):,} calls, {len(S)} sessions)")
print("by token type:", {k:f"{100*v/tot:.0f}%" for k,v in comp.most_common()})
print("by model:", {k:f"{100*v/tot:.0f}%" for k,v in bym.most_common() if v/tot>.001})

def run(idle_reset=False,compact_at=None,reorient=0,sonnet_share=0.0):
    BASE,SUM=40000,4000; T=0; resets=0
    for r in S:
        off=0; pt=None; pr=None
        for (t,u,m) in r:
            i,rd,a,b,o=parts(u); real=i+rd+a+b; gap=(t-pt).total_seconds() if pt else 0
            p=price(m); extra=0
            if pr and real<0.7*pr: off=0
            if idle_reset and gap>3600 and real>BASE+SUM: off=max(off,real-(BASE+SUM)); extra+=2*reorient*p[2]/1e6*1e0; resets+=1
            sim=real-off
            if compact_at and sim>compact_at:
                extra+=(sim*p[3]+SUM*p[4]+(BASE+SUM)*p[2]+reorient*p[2])/1e6; off=real-(BASE+SUM); resets+=1
            off=max(0,min(off,real)); red=off
            r2=min(red,rd); red-=r2; w1r=min(red,b); red-=w1r; w5r=min(red,a)
            d=dollars(u,m,rd=rd-r2,w1=b-w1r,w5=a-w5r)+extra
            if m=="claude-opus-5-5": d*= (1-sonnet_share*0.5)     # Sonnet 5.5 is exactly half Opus 5.5 in every price column
            T+=d; pt=t; pr=real
    return T,resets
base,_=run()
print(f"\nbaseline from replay: ${base:,.0f} (matches actual: {abs(base-tot)<1})\n")
print("SAVINGS vs now  (re-orient = tokens re-read after each fresh start/compaction)")
for R_ in (0,50000,100000):
    row=[]
    for name,kw in [("fresh after >1h idle",dict(idle_reset=True)),("compact at 150k",dict(compact_at=150000)),("compact at 100k",dict(compact_at=100000)),("both (150k)",dict(idle_reset=True,compact_at=150000))]:
        v,n=run(reorient=R_,**kw); row.append(f"{name} {100*(1-v/base):4.1f}%")
    print(f"  re-orient {R_//1000:>3}k | "+" | ".join(row))
print("\nMODEL SWITCH  (Opus 5.5 -> Sonnet 5.5 for a share of Opus work)")
for sh in (.25,.5):
    v,_=run(sonnet_share=sh); print(f"  move {int(sh*100)}% of Opus work to Sonnet: {100*(1-v/base):4.1f}% less")
v,_=run(idle_reset=True,compact_at=150000,reorient=50000,sonnet_share=.25); print(f"\ncombined (fresh after idle + compact 150k + 25% to Sonnet, 50k re-orient): {100*(1-v/base):.1f}% less")
