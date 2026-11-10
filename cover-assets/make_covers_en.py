"""はてなブログ用の表紙のうち、メインワードが日本語だったものを、英語のロゴにして作り直す(黒地×ネオン)。
使い方: python3 make_covers_en.py <character_head.png> <public-files のフォルダ>   (同じファイル名で上書きする)"""
from pathlib import Path
import io, math, random
import cairosvg
import numpy as np
from PIL import Image, ImageFilter, ImageColor
F="Noto Sans CJK JP"
BG="#07080A"; LN="#23272D"; LS="#3A4048"; INK="#ECEEF0"; MUTE="#8B929B"
LINE1,LINE2="Think","Work"       # メインワード(1行目=白、2行目=ネオン色)
BADGE="WORK × THINK"; SUB="仕事で「考える」ということ"
MODE="char"                       # "char"(既定。セキュリティ以外) / "ring"(サイバーセキュリティ関係) / "robot"(ロボットを頼まれたとき)
import sys
CHAR=sys.argv[1] if len(sys.argv)>1 else "character_head.png"   # キャラの頭部の切り抜きPNG
OUT=sys.argv[2] if len(sys.argv)>2 else "covers"
ACCENT="#2BB4F0"                  # char の強調色(記事ごとに COVERS で変える)
N="#D2FF3A"                       # ネオン色(robot)。ring のときは下の AC2 を使う
AC="#2D7BFF"; AC2="#2BB4F0"; AC3="#12C98A"   # ring: 青・シアン・緑
W,H=1200,630
CX,CY=905,315
def t(x,y,s,sz,w=700,c=INK,a="start",ex=""):
    return f'<text x="{x}" y="{y}" font-family="{F}" font-size="{sz}" font-weight="{w}" fill="{c}" text-anchor="{a}" {ex}>{s}</text>'
def pts(p): return " ".join(f"{x:.1f},{y:.1f}" for x,y in p)
def pol(r,a):
    q=math.radians(a); return CX+r*math.cos(q), CY+r*math.sin(q)
def robot(cx,cy,s=1.0):
    P='#0D0F12'
    g=f'<g transform="translate({cx} {cy}) scale({s})" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round">'
    g+=f'<circle r="250" stroke="{LN}" stroke-width="2"/><circle r="200" stroke="{LN}" stroke-width="2" stroke-dasharray="3 10"/>'
    body="M-150 250 L-150 150 C-150 98 -96 76 -40 70 L40 70 C96 76 150 98 150 150 L150 250"
    g+=f'<path d="{body} Z" fill="{P}" stroke="none"/><path d="{body}"/>'
    g+=f'<path d="M-96 100 C-120 120 -126 150 -126 250 M96 100 C120 120 126 150 126 250" stroke="{LS}"/>'
    g+=f'<circle cx="-118" cy="112" r="14" fill="{P}"/><circle cx="118" cy="112" r="14" fill="{P}"/>'
    g+=f'<path d="M-52 150 H52 L40 220 H-40 Z" stroke="{LS}"/>'
    g+=f'<circle cy="182" r="20" stroke="{N}"/><circle cy="182" r="6" fill="{N}" stroke="{N}"/><path d="M-20 182 H-52 M20 182 H52" stroke="{N}" stroke-width="1.5" opacity="0.6"/>'
    g+=f'<rect x="-30" y="12" width="60" height="68" rx="8" fill="{P}"/><path d="M-30 34 H30 M-30 52 H30" stroke="{LS}"/>'
    g+=f'<path d="M0 -196 V-158"/><circle cy="-204" r="10" stroke="{N}"/>'
    g+=f'<rect x="-112" y="-158" width="224" height="176" rx="48" fill="{P}"/>'
    g+=f'<rect x="-84" y="-126" width="168" height="84" rx="34" stroke="{LS}"/>'
    g+=f'<circle cx="-36" cy="-84" r="18" fill="{N}" stroke="{N}"/><circle cx="36" cy="-84" r="18" fill="{N}" stroke="{N}"/><path d="M-30 -10 H30" stroke="{LS}"/>'
    g+=f'<rect x="-136" y="-110" width="24" height="60" rx="10" fill="{P}"/><rect x="112" y="-110" width="24" height="60" rx="10" fill="{P}"/>'
    g+=f'<circle cx="-124" cy="-80" r="3" fill="{N}" stroke="{N}"/><circle cx="124" cy="-80" r="3" fill="{N}" stroke="{N}"/></g>'
    return g
DEFS=f'''<linearGradient id="hud" x1="{CX-340}" y1="{CY-340}" x2="{CX+340}" y2="{CY+340}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{AC3}"/><stop offset="0.3" stop-color="{AC3}"/><stop offset="0.56" stop-color="{AC2}"/><stop offset="0.82" stop-color="{AC}"/><stop offset="1" stop-color="{AC}"/></linearGradient>
<clipPath id="fr"><rect x="34" y="34" width="1132" height="562"/></clipPath>'''
def svg(body): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs>{DEFS}</defs>{body}</svg>'
def hud(k=1.0,core=False):
    R=random.Random(11); g=""
    def pl(P,w): return f'<polyline points="{pts(P)}" fill="none" stroke="url(#hud)" stroke-width="{w*k:.2f}" stroke-linejoin="miter"/>'
    g+=f'<polygon points="{pts([pol(146,i*30+15) for i in range(12)])}" fill="none" stroke="url(#hud)" stroke-width="{2.4*k:.2f}" stroke-linejoin="round"/>'
    g+=f'<polygon points="{pts([pol(138,i*30+15) for i in range(12)])}" fill="none" stroke="url(#hud)" stroke-width="{0.9*k:.2f}" stroke-linejoin="round"/>'
    for r,w in [(172,3.6),(204,1.4),(236,2.4),(266,1.4),(298,1.2)]:
        a=R.uniform(0,360); tot=0
        while tot<340:
            span=min(R.uniform(20,100),345-tot); gap=R.uniform(8,30)
            if span<8: break
            x0,y0=pol(r,a); x1,y1=pol(r,a+span)
            d_=f"M{x0:.1f} {y0:.1f} A{r} {r} 0 {1 if span>180 else 0} 1 {x1:.1f} {y1:.1f}"
            g+=f'<path d="{d_}" fill="none" stroke="url(#hud)" stroke-width="{w*k:.2f}"/>'
            if core and w>=2.2: g+=f'<path d="{d_}" fill="none" stroke="#fff" stroke-opacity="0.8" stroke-width="{w*0.32:.2f}"/>'
            if span>40 and R.random()<0.45:
                m=a+span*R.uniform(.3,.7); d=R.choice([-1,1])*R.choice([9,12])
                g+=pl([pol(r,m-2.6),pol(r+d,m-2.6),pol(r+d,m+2.6),pol(r,m+2.6)],1.2)
            if R.random()<0.5:
                x,y=pol(r+R.choice([-8,8]),a+span*R.random())
                g+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.3*k:.1f}" fill="{AC3}"/>'
            a+=span+gap; tot+=span+gap
    for i in range(0,360,4):
        if R.random()<0.55: g+=pl([pol(244,i),pol(244+R.choice([6,10,14]),i)],0.9)
    for i in range(0,360,9):
        if R.random()<0.6: g+=pl([pol(180,i),pol(180+R.choice([8,14,20]),i)],1.0)
    for _ in range(16):
        a=R.uniform(-100,100); r0=R.choice([304,312,324]); r1=r0+R.uniform(30,110)
        g+=pl([pol(r0,a),pol(r1,a)],0.9)+f'<circle cx="{pol(r1,a)[0]:.1f}" cy="{pol(r1,a)[1]:.1f}" r="{2*k:.1f}" fill="{AC}"/>'
    for _ in range(18):
        a=R.uniform(0,360); r=R.choice([186,220,252,282]); d=R.choice([8,12,16]); da=R.choice([3,4.5,6])
        P=[pol(r,a),pol(r+d,a),pol(r+d,a+da),pol(r+2*d,a+da),pol(r+2*d,a+2*da)]
        g+=pl(P,1.3)+f'<circle cx="{P[-1][0]:.1f}" cy="{P[-1][1]:.1f}" r="{2.4*k:.1f}" fill="{AC}"/>'
    for _ in range(12):
        r=R.choice([188,222,254,284]); a=R.uniform(0,360)
        g+=pl([pol(r-6,a-3),pol(r+6,a-3),pol(r+6,a+3),pol(r-6,a+3),pol(r-6,a-3)],1.1)
    for i in range(0,360,3):
        if (i//30)%3!=0:
            x,y=pol(224,i); g+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{1.2*k:.1f}" fill="{AC}" opacity="0.8"/>'
    # 中心の立方体(線だけ)
    s=61; k3=0.866
    V=[(CX,CY-s),(CX+k3*s,CY-s/2),(CX+k3*s,CY+s/2),(CX,CY+s),(CX-k3*s,CY+s/2),(CX-k3*s,CY-s/2),(CX,CY)]
    for a_,b_ in [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(5,6),(1,6),(2,6),(4,6),(3,6),(0,6)]:
        g+=f'<line x1="{V[a_][0]:.1f}" y1="{V[a_][1]:.1f}" x2="{V[b_][0]:.1f}" y2="{V[b_][1]:.1f}" stroke="url(#hud)" stroke-width="{1.4*k:.2f}"/>'
    g+=f'<circle cx="{CX}" cy="{CY}" r="{4*k:.1f}" fill="{AC}"/>'
    return f'<g clip-path="url(#fr)">{g}</g>'
def png(s): return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(),output_width=W))).convert("RGBA")
def ring_layer():
    base=Image.new("RGBA",(W,H),BG)
    a=png(svg(hud(1.5))).getchannel("A"); rgb=ImageColor.getrgb(AC2)
    for r,k,cap in [(3,1.4,110),(9,2.2,70),(20,3.2,48)]:   # 黒地では、にじみを重ねて光らせる
        ba=a.filter(ImageFilter.GaussianBlur(r)).point(lambda v,k=k,cap=cap:min(cap,int(v*k)))
        l=Image.new("RGBA",(W,H),rgb+(0,)); l.putalpha(ba); base=Image.alpha_composite(base,l)
    return Image.alpha_composite(base,png(svg(hud(1.0,True))))
def texts(label,head,neon):
    b=f'<circle cx="72" cy="78" r="6" fill="{neon}"/>'+t(92,85,BADGE,20,700,INK,ex='letter-spacing="6"')
    b+=t(72,160,label,26,700,neon)
    b+=t(72,330,LINE1,(150 if len(LINE1)<7 else 132),900,INK,ex='letter-spacing="-5"')+t(72,470,LINE2,150,900,neon,ex='letter-spacing="-5"')
    b+=f'<rect x="72" y="505" width="40" height="3" fill="{neon}"/>'+t(72,560,head,(38 if len(head)<=14 else 33),800,INK)
    b+=t(1130,86,SUB,20,500,MUTE,"end")
    return b
def frame(): return f'<rect x="32.5" y="32.5" width="1135" height="565" fill="none" stroke="{LN}" stroke-width="1.5"/>'
def cover(label,head):
    neon=ACCENT if MODE=="char" else (AC2 if MODE=="ring" else N)
    if MODE=="char":
        base=Image.new("RGBA",(W,H),BG)
        ov=png(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><circle cx="{CX}" cy="{CY}" r="250" fill="none" stroke="{LN}" stroke-width="2"/><circle cx="{CX}" cy="{CY}" r="200" fill="none" stroke="{LN}" stroke-width="2" stroke-dasharray="3 10"/></svg>')
        base=Image.alpha_composite(base,ov)
        ch=Image.open(CHAR).convert("RGBA"); sc=465/ch.height; ch=ch.resize((int(ch.width*sc),465),Image.LANCZOS)
        a=np.array(ch.getchannel("A")).astype(float); yy=np.linspace(0,1,ch.height)[:,None]
        xx=np.linspace(0,1,ch.width)[None,:]; a*=np.clip((1-yy)/0.3,0,1)*np.clip(np.minimum(xx,1-xx)/0.14,0,1)   # 下端と左右を黒へなじませる
        ch.putalpha(Image.fromarray(a.astype("uint8")))
        gl=ch.getchannel("A").filter(ImageFilter.GaussianBlur(18)).point(lambda v:int(v*0.35))   # 青いにじみ
        glow=Image.new("RGBA",ch.size,ImageColor.getrgb(AC2)+(0,)); glow.putalpha(gl)
        x=CX-ch.width//2; y=CY-250+46
        base.alpha_composite(glow,(x,y)); base.alpha_composite(ch,(x,y))
        top=png(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{frame()}{texts(label,head,neon)}</svg>')
        return Image.alpha_composite(base,top).convert("RGB")
    if MODE=="ring":
        base=ring_layer()
        top=png(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{frame()}{texts(label,head,neon)}</svg>')
        return Image.alpha_composite(base,top).convert("RGB")
    s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{BG}"/>{frame()}{texts(label,head,neon)}{robot(905,315)}</svg>'
    return png(s).convert("RGB")
# (保存先, 回ラベル, 見出し, メインワード1行目, 2行目, 強調色, 絵, 左上の小ラベル, 右上のひとこと)
GREEN="#12C98A"; BLUE="#5B8CFF"; AQUA="#3DE0E0"; CYAN="#2BB4F0"
ELD=("WISDOM × AI","長老からAIへ 知恵の旅"); SD=("IT × 30 YEARS","ITは30年同じ夢を見る")
NV=("SYSTEM × VISION","思想のないシステム"); AT=("AUTO TRADE","自動で株の売買を行う夢見る人")
PHP=("SECURITY","PHPの安全性")
COVERS=[
 ("elder-to-ai/01_cover_neon.png","連載 第1回","知恵は5万年、誰が運んだのか","Wisdom","Journey",GREEN,"char",*ELD),
 ("elder-to-ai/02_cover_neon.png","連載 第2回","長老は「歩く図書館」だった","Wisdom","Journey",GREEN,"char",*ELD),
 ("elder-to-ai/03_cover_neon.png","連載 第3回","文字は「帳簿」から生まれた","Wisdom","Journey",GREEN,"char",*ELD),
 ("elder-to-ai/04_cover_neon.png","連載 第4回","AIで、また「聞く人」に戻った","Wisdom","Journey",GREEN,"char",*ELD),
 ("elder-to-ai/05_cover_neon.png","連載 第5回","津波石と子守唄が命を救った","Wisdom","Journey",GREEN,"char",*ELD),
 ("elder-to-ai/06_cover_neon.png","最終回","検索の次は「聞く前に届く」","Wisdom","Journey",GREEN,"char",*ELD),
 ("same-dream/07_cover_neon.png","連載 第1回","流行語は変わる、夢は変わらない","Same","Dream",BLUE,"char",*SD),
 ("same-dream/08_cover_neon.png","連載 第2回","1988年、「消えるコンピュータ」の夢","Same","Dream",BLUE,"char",*SD),
 ("same-dream/09_cover_neon.png","連載 第3回","先を行った日本は、なぜ止まったか","Same","Dream",BLUE,"char",*SD),
 ("same-dream/10_cover_neon.png","連載 第4回","スマホは、名前を言わずに夢を叶えた","Same","Dream",BLUE,"char",*SD),
 ("same-dream/11_cover_neon.png","連載 第5回","データは溜まった、でも誰も読めない","Same","Dream",BLUE,"char",*SD),
 ("same-dream/12_cover_neon.png","最終回","AIは30年目の「最後の部品」","Same","Dream",BLUE,"char",*SD),
 ("no-vision/21_cover_neon.png","連載 第1回","便利だったはずのシステムが重荷に","No","Vision",AQUA,"char",*NV),
 ("no-vision/22_cover_neon.png","連載 第2回","つながらない事務系、その正体は","No","Vision",AQUA,"char",*NV),
 ("no-vision/23_cover_neon.png","最終回","1つずつ直しても、綺麗にならない","No","Vision",AQUA,"char",*NV),
 ("no-vision/24_cover_neon.png","有料編 第3回","見積とヒアリングの裏側","No","Vision",AQUA,"char",*NV),
 ("no-vision/25_cover_neon.png","有料編 第1回","最初の2週間の仕事と、記入用の表","No","Vision",AQUA,"char",*NV),
 ("no-vision/26_cover_neon.png","有料編 第2回","記入済みの見本で、合意まで進める","No","Vision",AQUA,"char",*NV),
 ("auto-trading/40_cover_neon.png","連載 1回目","口座の開設と、設計から始めた","Auto","Dream",GREEN,"char",*AT),
 ("auto-trading/41_cover_neon.png","連載 2回目","バックテストの限界を見つめる","Auto","Dream",GREEN,"char",*AT),
 ("auto-trading/42_cover_neon.png","連載 3回目","注文が出ない原因を追う","Auto","Dream",GREEN,"char",*AT),
 ("php/19_cover_neon.png","緊急","PHPを使っている方は早急に対応して","PHP","Urgent",CYAN,"ring",*PHP),
 ("php/20_cover_neon.png","番外","あなたの会社にも、PHPは隠れている","PHP","Hidden",CYAN,"ring",*PHP),
 ("book/33_cover_neon.png","書評","良書は、読み直すと再発見がある","The","Goal",BLUE,"char","BOOK × THINKING","良書は再発見できる"),
 ("exec-security/39_cover_neon.png","経営者向け","今日できる、会社のセキュリティ点検","Security","Check",CYAN,"ring","SECURITY","経営者向け"),
]
if __name__=="__main__":
    out=Path(OUT)
    for n,l,h,a,b,ac,mode,badge,sub in COVERS:
        LINE1,LINE2,ACCENT,MODE,BADGE,SUB=a,b,ac,mode,badge,sub
        p=out/n; p.parent.mkdir(parents=True,exist_ok=True)
        cover(l,h).save(p); print("wrote",p)
