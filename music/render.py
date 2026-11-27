# Original folk tune "Senior Year Stomp" — composed for this project.
import numpy as np, wave
SR=44100
rng=np.random.default_rng(7)
mf=lambda m:440*2**((m-69)/12)

# ---- song layout (bars of 4 beats) ----
CH={'Am':[45,52,57,60,64],'G':[43,50,55,59,62],'F':[41,48,53,57,60],'E':[40,47,52,56,59],'Dm':[50,57,62,65],'C':[48,52,55,60,64]}
ROOT={'Am':(45,52),'G':(43,50),'F':(41,48),'E':(40,47),'Dm':(38,45),'C':(36,43)}
A1=[[(76,1),(69,.5),(71,.5),(72,.5),(71,.5),(69,1)],[(74,1),(71,.5),(67,.5),(71,1),(74,1)],
    [(72,.5),(69,.5),(65,.5),(69,.5),(72,.5),(74,.5),(72,1)],[(71,.5),(68,.5),(64,.5),(68,.5),(71,1),(74,.5),(72,.5)]]
A2=A1[:3]+[[(71,1),(68,1),(64,2)]]
B1=[[(77,.5),(77,.5),(76,.5),(74,.5),(81,2)],[(76,.5),(74,.5),(72,.5),(71,.5),(72,1),(69,1)],
    [(68,.5),(71,.5),(76,.5),(77,.5),(76,.5),(74,.5),(72,.5),(71,.5)],[(69,1),(76,1),(81,2)]]
B2=B1[:3]+[[(81,.5),(80,.5),(81,.5),(76,.5),(69,2)]]
BUILD=[[(64,.5),(65,.5),(68,.5),(69,.5),(71,.5),(72,.5),(74,.5),(76,.5)],[(65,.5),(68,.5),(69,.5),(71,.5),(72,.5),(74,.5),(76,.5),(77,.5)],
       [(68,.5),(69,.5),(71,.5),(72,.5),(74,.5),(76,.5),(77,.5),(80,.5)],[(76,1),(80,1),(83,2)]]
secs=[('intro',['Am','G','F','E'],None,'light'),
 ('A',['Am','G','F','E']*2,A1+A2,'stomp'),
 ('B',['Dm','Am','E','Am']*2,B1+B2,'stomp'),
 ('A',['Am','G','F','E']*2,A1+A2,'drive'),
 ('build',['E']*4,BUILD,'build'),
 ('B',['Dm','Am','E','Am']*2,B1+B2,'double'),
 ('A',['Am','G','F','E']*2,A1+A2,'double'),
 ('end',['Am'],[[(81,4)]],'end')]
bars=[];[bars.extend([(c,(mel[i] if mel else None),feel) for i,c in enumerate(chs)]) for _,chs,mel,feel in secs]
NB=len(bars)
# tempo rises from 112 to 160 bpm over the song (the "speeds up" build)
beat_t=[0.0]
for b in range(NB*4+8):
    bpm=112+48*min(1,(b/(NB*4))**1.4)
    beat_t.append(beat_t[-1]+60/bpm)
bt=lambda x:np.interp(x,np.arange(len(beat_t)),beat_t)
total=bt(NB*4)+4
out=np.zeros((int(total*SR)+SR,2))

def add(sig,t0,pan=0,gain=1):
    i=int(t0*SR);n=min(len(sig),len(out)-i)
    if n<=0:return
    l=np.cos((pan+1)*np.pi/4);r=np.sin((pan+1)*np.pi/4)
    out[i:i+n,0]+=sig[:n]*l*gain;out[i:i+n,1]+=sig[:n]*r*gain

def pluck(f,dur=1.6,bright=.5,K=12):
    N=int(dur*SR);t=np.arange(N)/SR;k=np.arange(1,K+1)[:,None]
    pick=.13+bright*.05
    amps=np.abs(np.sin(np.pi*k*pick))/k**(1.4-bright*.5)
    dec=1.2+k*(1.6-bright*.9)
    inh=k*np.sqrt(1+.0004*k**2)
    s=(amps*np.exp(-dec*t)*np.sin(2*np.pi*f*inh*t+rng.uniform(0,6.28,(K,1)))).sum(0)
    att=np.minimum(1,t/.002);s*=att
    s+=rng.normal(0,1,N)*np.exp(-t*300)*.15*bright
    return s

def strum(notes,t0,up=False,vel=1,dur=1.2):
    ns=notes[::-1] if up else notes
    for i,m in enumerate(ns):
        add(pluck(mf(m),dur,.35)*vel*.22,t0+i*(.011 if not up else .008),pan=-.35+.12*i)

def kick(t0,g=1):
    N=int(.35*SR);t=np.arange(N)/SR;f=50+90*np.exp(-t*30)
    add(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*.9*g,t0)
def stomp(t0,g=1): # foot stomp + hand clap
    N=int(.25*SR);t=np.arange(N)/SR;n=rng.normal(0,1,N)
    lp=np.convolve(n,np.ones(18)/18,'same')
    add((lp*np.exp(-t*28)*1.4+n*np.exp(-t*60)*.25)*g*.5,t0,pan=.15)
def shaker(t0,g=1):
    N=int(.08*SR);t=np.arange(N)/SR;n=rng.normal(0,1,N);n=n-np.convolve(n,np.ones(4)/4,'same')
    add(n*np.exp(-t*50)*.08*g,t0,pan=.4)

for bi,(ch,mel,feel) in enumerate(bars):
    b0=bi*4;notes=CH[ch];r,fifth=ROOT[ch]
    if feel=='end':
        strum(notes,bt(b0),vel=1.3,dur=3.5);add(pluck(mf(r-12+12),3.5,.2)*.5,bt(b0));kick(bt(b0),1.2)
    else:
        for beat in range(4):
            tb=bt(b0+beat)
            if feel=='light':
                strum(notes,tb,vel=.7);strum(notes,bt(b0+beat+.5),up=True,vel=.4)
                continue
            # oom-pah: bass on 1 & 3, strums on 2 & 4, light up-strums on the offbeats
            if beat%2==0:add(pluck(mf((r if beat==0 else fifth)),1.0,.15,8)*.55,tb,pan=0);kick(tb,.8 if feel!='light' else .5)
            else:strum(notes[1:],tb,vel=1.0);stomp(tb,1 if feel!='build' else .7)
            strum(notes[1:],bt(b0+beat+.5),up=True,vel=.5)
            if feel in('drive','double','build'):
                for q in(.25,.75):shaker(bt(b0+beat+q),1.2 if feel=='double' else .8)
            if feel=='double':strum(notes[1:],bt(b0+beat+.75),up=True,vel=.35)
            if feel=='build':kick(bt(b0+beat+.5),.5)
    # lead: balalaika-ish bright pluck, tremolo on long notes
    if mel:
        pos=b0
        for m,d in mel:
            if d>=1:
                step=.25 if feel not in('double',) else .125
                x=0
                while x<d-1e-6:
                    add(pluck(mf(m),.5,.95,14)*.16*(1-.15*(x>0)),bt(pos+x),pan=.3);x+=step
            else:add(pluck(mf(m),.9,.95,14)*.2,bt(pos),pan=.3)
            pos+=d

# reverb via FFT convolution
ir_n=int(1.6*SR);ir=rng.normal(0,1,(ir_n,2))*np.exp(-np.arange(ir_n)/SR*3.2)[:,None];ir[:int(.012*SR)]=0
L=len(out)+ir_n;nf=1<<int(np.ceil(np.log2(L)))
wet=np.stack([np.fft.irfft(np.fft.rfft(out[:,c],nf)*np.fft.rfft(ir[:,c],nf),nf)[:len(out)] for c in range(2)],1)
mix=out+wet*(np.abs(out).max()/np.abs(wet).max())*.22
mix=np.tanh(mix/np.abs(mix).max()*1.3)*.89
end=int((bt(NB*4)+3.6)*SR);mix=mix[:end];fade=int(.4*SR);mix[-fade:]*=np.linspace(1,0,fade)[:,None]
pcm=(mix*32767).astype('<i2')
with wave.open('/home/claude/music/song.wav','wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes())
print('bars',NB,'seconds',round(len(mix)/SR,1))
