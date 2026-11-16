"""Builds index.html and compositions/mots.html for the before/after works video.
Run from the project root: python3 tools/build.py, then re-apply the grade (see README note at the end)."""
from PIL import Image

# (id, seconds, kind, file, media-start)   kind: img | vid
SEQ = [
 ("avant",1.5,"img","avant-facade",0), ("apres",1.5,"img","apres-facade",0),
 ("mur",1.5,"img","mur-abime",0), ("salle",1.0,"img","salle-vide",0), ("nettoyage",2.0,"vid","nettoyage",0.1),
 ("hottesale",1.0,"img","hotte-sale",0), ("moteur",1.0,"img","moteur-gras",0), ("extracteur",1.5,"img","extracteur-neuf",0),
 ("cuisine",1.5,"img","cuisine",0), ("hotte",1.0,"img","hotte",0), ("sauces",1.0,"img","sauces",0), ("courses",1.0,"img","courses",0),
 ("ens1",2.0,"vid","enseigne-porte",0.2), ("echelle",1.5,"img","echelle",0), ("ens2",1.5,"vid","enseigne-posee",0.3),
 ("menu",1.0,"img","menu-imprime",0), ("comptoir1",1.5,"img","comptoir-menu",0), ("stickers",1.0,"vid","stickers",0.2),
 ("mugs",1.0,"img","mugs",0), ("tampon",1.0,"img","tampon",0), ("borne",1.0,"vid","borne",0.3), ("bornes",1.0,"img","bornes",0),
 ("tonneau",1.0,"img","tonneau",0),
 ("entree",2.0,"vid","entree",0.4), ("duo",1.5,"img","duo",0), ("ecran",1.5,"vid","ecran-vitrine",1.2),
 ("nuit",1.5,"img","nuit-file",0), ("story",1.5,"vid","story-file",0.2), ("comptoir2",2.0,"vid","entree-comptoir",0.1),
]
# Chapter words: shot id -> text (HTML allowed for a line break)
CH = {"avant":"AVANT","apres":"APRÈS","mur":"ON REPART<br>DE ZÉRO","hottesale":"LA CUISINE",
      "extracteur":"TOUT NEUF","ens1":"L'ENSEIGNE","menu":"LES DÉTAILS","entree":"LE JOUR J"}
LOW = {"avant","apres"}   # words placed low so the shop signs stay visible

t=0; html=[]; js=[]; marks=[]
for i,(sid,d,k,f,ms) in enumerate(SEQ):
    st=round(t,2); t+=d
    if k=="vid":
        html.append(f'      <div class="shot" id="w-{sid}"><video id="v-{sid}" class="clip" src="assets/footage/{f}.mp4" data-start="{st}" data-duration="{d}" data-media-start="{ms}" data-track-index="2" muted playsinline></video></div>')
        js.append(f'tl.fromTo("#w-{sid}", {{ scale: 1.14 }}, {{ scale: 1, duration: 0.3, ease: "power3.out" }}, {st});')
    else:
        w,h=Image.open(f"assets/img/{f}.jpg").size
        if w>h:  # landscape photo: full height, slow pan across it
            iw=round(1920*w/h)
            html.append(f'      <div class="shot" id="w-{sid}"><img id="v-{sid}" class="clip pan" src="assets/img/{f}.jpg" style="width:{iw}px;height:1920px;left:0;top:0" data-start="{st}" data-duration="{d}" data-track-index="2" alt=""></div>')
            dx=iw-1080; a,b=(-dx*0.15,-dx*0.85) if i%2==0 else (-dx*0.85,-dx*0.15)
            js.append(f'tl.fromTo("#w-{sid}", {{ x: {a:.0f}, scale: 1.06 }}, {{ x: {b:.0f}, scale: 1, duration: {d}, ease: "power1.inOut" }}, {st});')
        else:
            html.append(f'      <div class="shot" id="w-{sid}"><img id="v-{sid}" class="clip" src="assets/img/{f}.jpg" data-start="{st}" data-duration="{d}" data-track-index="2" alt=""></div>')
            js.append(f'tl.fromTo("#w-{sid}", {{ scale: 1.14 }}, {{ scale: 1, duration: 0.3, ease: "power3.out" }}, {st});')
            js.append(f'tl.to("#w-{sid}", {{ scale: 1.06, duration: {d-0.3:.2f}, ease: "none" }}, {st+0.3:.2f});')
    if sid in CH: marks.append((sid,st,CH[sid]))
END=round(t,2); TOTAL=round(END+3.5,2)

words=[]
for j,(sid,st,txt) in enumerate(marks):
    nxt = marks[j+1][1] if j+1<len(marks) else END
    words.append((f"m{j}",sid,st,round(nxt-st if sid in LOW else min(1.5,nxt-st),2),txt))

open("index.html","w").write(f'''<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #111; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; }}
      .shot {{ position: absolute; inset: 0; z-index: 1; }}
      .shot video, .shot img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .shot img.pan {{ object-fit: fill; }}
      .scene-host {{ position: absolute; inset: 0; }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 8; pointer-events: none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920" data-layout-allow-overflow>
      <!-- Montage sur une grille de 0,5 s (120 BPM) : un son TikTok à ce tempo tombera sur les coupes. -->
{chr(10).join(html)}
      <div id="fin" class="scene-host" style="z-index:2" data-composition-id="fin" data-composition-src="compositions/fin.html"
           data-start="{END}" data-duration="{round(TOTAL-END,2)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="mots" class="scene-host" style="z-index:5" data-composition-id="mots" data-composition-src="compositions/mots.html"
           data-start="0" data-duration="{END}" data-track-index="3" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="flash"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10)+"      ").join(js)}
      tl.set("#flash", {{ opacity: 0 }}, 0);
      [1.5, {END}].forEach((t) => {{
        tl.set("#flash", {{ opacity: 0.9 }}, t);
        tl.to("#flash", {{ opacity: 0, duration: 0.22, ease: "power2.out" }}, t);
      }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')

low_ids=", ".join(f"#{i}" for i,sid,*_ in words if sid in LOW)
low_w=", ".join(f"#{i} .mw" for i,sid,*_ in words if sid in LOW)
wh="\n".join(f'    <div class="mot clip" id="{i}" data-start="{s}" data-duration="{d}" data-track-index="1"><span class="mw" id="{i}-w">{t}<span class="pt">.</span></span></div>' for i,sid,s,d,t in words)
open("compositions/mots.html","w").write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .mot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 980px; text-align: center;
      background: linear-gradient(180deg, rgba(0,0,0,0.66) 0%, rgba(0,0,0,0.42) 50%, rgba(0,0,0,0) 100%); }}
    .mw {{ display: inline-block; margin-top: 380px; max-width: 820px; color: #fff; font-family: "Inter", sans-serif; font-weight: 900;
      font-size: 112px; line-height: 0.98; letter-spacing: -0.05em; text-shadow: 0 6px 30px rgba(0,0,0,0.35); }}
    {low_ids} {{ top: 940px; background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.5) 50%, rgba(0,0,0,0) 100%); }}
    {low_w} {{ font-size: 150px; margin-top: 360px; }}
    .pt {{ color: #FF5CAA; }}
  </style>
  <div id="root" data-composition-id="mots" data-width="1080" data-height="1920" data-layout-allow-overflow>
{wh}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    // Frame 0 is the thumbnail: "AVANT." is already there.
    tl.fromTo("#m0-w", {{ scale: 1.06 }}, {{ scale: 1, duration: 0.6, ease: "power3.out" }}, 0);
    [{", ".join(f'["#{i}-w", {s}]' for i,sid,s,d,t in words[1:])}].forEach(([sel, t]) => {{
      tl.fromTo(sel, {{ scale: 1.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.22, ease: "power4.out" }}, t);
    }});
    window.__timelines["mots"] = tl;
  </script>
</template>
''')
print("END", END, "TOTAL", TOTAL)
# Then: npx hyperframes media-treatment --selector "video, img.clip" --grading '<grade>' --apply
