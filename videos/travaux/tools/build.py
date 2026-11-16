"""Builds index.html and compositions/mots.html for the before/after works video.
Run from the project root: python3 tools/build.py, then re-apply the grade (see README note at the end)."""
from PIL import Image

# Documentary cut: only clean, well-framed shots. (id, seconds, kind, file, media-start)
SEQ = [
 ("avant",1.7,"img","avant-facade",0), ("apres",1.7,"img","apres-facade",0),
 ("mur",1.3,"img","mur-abime",0), ("salle",1.2,"img","salle-vide",0),
 ("rouleau",2.0,"vid","peinture-rouleau",0.1), ("plafond",1.6,"vid","peinture-plafond",0.2), ("murpeint",1.8,"vid","peinture-mur",0.2),
 ("moteur",1.3,"img","moteur-gras",0), ("extracteur",1.3,"img","extracteur-neuf",0), ("cuisine",1.5,"img","cuisine",0), ("sauces",1.3,"img","sauces",0),
 ("menu",1.3,"img","menu-imprime",0), ("comptoir1",1.6,"img","comptoir-menu",0), ("mugs",1.1,"img","mugs",0),
 ("tampon",1.1,"img","tampon",0), ("stickers",1.2,"vid","stickers",0.2), ("tonneau",1.3,"img","tonneau",0),
 ("echelle",1.7,"img","echelle",0),
 ("duo",1.8,"img","duo",0), ("comptoir2",2.0,"vid","entree-comptoir",0.1), ("story",1.7,"vid","story-file",0.15),
]
# Narration lines: shot id -> (kicker, sentence with <br> for line breaks)
CH = {
 "avant":("LES LILAS","Avant,<br>c'était ça"),
 "apres":("AUJOURD'HUI","Smash<br>by Bubble Sü"),
 "mur":("LE CHANTIER","On a tout<br>repris à zéro"),
 "rouleau":("À LA MAIN","Chaque mur,<br>repeint par nous"),
 "moteur":("LA CUISINE","Remise<br>à neuf"),
 "menu":("L'IDENTITÉ","Jusqu'au<br>moindre détail"),
 "echelle":("L'ENSEIGNE","Posée<br>par nos soins"),
 "duo":("LE JOUR J","Et vous<br>étiez là"),
}
LOW = set()
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
for j,(sid,st,(kick,txt)) in enumerate(marks):
    nxt = marks[j+1][1] if j+1<len(marks) else END
    words.append((f"m{j}",sid,st,round(min(2.6,nxt-st),2),kick,txt))
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

def lines(txt): return "".join(f'<div class="l"><span>{x}</span></div>' for x in txt.split("<br>"))
wh="\n".join(
    f'    <div class="mot clip" id="{i}" data-start="{s}" data-duration="{d}" data-track-index="1">\n'
    f'      <div class="k" id="{i}-k"><i class="bar"></i>{k}</div>\n'
    f'      <div class="t" id="{i}-t">{lines(t)}</div>\n'
    f'    </div>' for i,sid,s,d,k,t in words)
timing=", ".join(f'["{i}", {s}, {round(s+d,2)}]' for i,sid,s,d,k,t in words)
tpl=open("tools/mots.template.html").read()
open("compositions/mots.html","w").write(tpl.replace("__WORDS__",wh).replace("__TIMING__",timing).replace("__END__",str(END)))
print("END", END, "TOTAL", TOTAL)
# Then: npx hyperframes media-treatment --selector "video, img.clip" --grading '<grade>' --apply
