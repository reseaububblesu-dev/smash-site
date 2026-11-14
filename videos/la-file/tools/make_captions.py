"""Builds compositions/captions.html from assets/transcript.json.
Display words are written by hand (correct spelling) and take their timing
from the transcript word at the same position."""
import json, html
OFFSET = 0.1  # the voice starts 0.1 s into the film
words = json.load(open("assets/voice-perso/mots.json"))
# (display text, transcript index) per group
GROUPS = [
    [("DES", 9), ("SMASH", 10), ("BURGERS", 11)],
    [("DE", 12), ("QUALITÉ,", 13)],
    [("ÉCRASÉS", 14), ("À", 15), ("LA", 16), ("MINUTE", 17)],
    [("SUR", 18), ("LA", 19), ("PLANCHA.", 20)],
    [("UN", 21), ("FROMAGE", 22), ("QUI", 23), ("COULE,", 24)],
    [("DES", 25), ("FRITES", 26), ("MAISON", 27)],
    [("QUI", 28), ("VONT", 29), ("AVEC.", 30)],
    [("LE", 31), ("POULET", 32), ("FRIT,", 33)],
    [("BIEN", 34), ("CROUSTILLANT.", 35)],
    [("ET", 36), ("POUR", 37), ("FINIR,", 38)],
    [("DES", 39), ("MILKSHAKES,", 40)],
    [("DES", 41), ("TIRAMISUS,", 42)],
    [("TOUT", 43), ("CE", 44), ("QU'IL", 45), ("FAUT.", 47)],
    [("SMASH", 48), ("BY", 49), ("BUBBLE", 50), ("SÜ,", 50.5)],
    [("81", 51), ("AVENUE", 52), ("PASTEUR,", 53)],
    [("AUX", 54), ("LILAS.", 55)],
]
END = 21.45  # the end card takes over
def ws(i):
    if i == 50.5:  # "Bubblesu" is one word for whisper: split it in two
        w = words[50]; return round((w["start"] + w["end"]) / 2 + OFFSET, 2)
    return round(words[i]["start"] + OFFSET, 2)
groups_html, js = [], []
for g, grp in enumerate(GROUPS):
    start = round(ws(grp[0][1]) - 0.05, 2)
    nxt = GROUPS[g + 1] if g + 1 < len(GROUPS) else None
    end = round(ws(nxt[0][1]) - 0.05, 2) if nxt else END
    spans = []
    for j, (txt, i) in enumerate(grp):
        spans.append(f'<span class="cw" id="cw{g}_{j}">{html.escape(txt)}</span>')
        js.append(f'  tl.set("#cw{g}_{j}", {{ backgroundColor: "#A80F57" }}, {ws(i):.2f});')
        wend = ws(grp[j + 1][1]) if j + 1 < len(grp) else end
        js.append(f'  tl.set("#cw{g}_{j}", {{ backgroundColor: "rgba(168,15,87,0)" }}, {wend:.2f});')
    groups_html.append(f'      <div class="cg" id="cg{g}"><span class="cbox">{" ".join(spans)}</span></div>')
    js.append(f'  tl.fromTo("#cg{g}", {{ opacity: 0, scale: 0.86 }}, {{ opacity: 1, scale: 1, duration: 0.12, ease: "back.out(2)" }}, {start});')
    js.append(f'  tl.to("#cg{g}", {{ opacity: 0, duration: 0.08, ease: "power2.in" }}, {end - 0.08:.2f});')
    js.append(f'  tl.set("#cg{g}", {{ visibility: "hidden" }}, {end:.2f});')
out = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cg {{
      position: absolute; left: 160px; width: 760px; top: 1040px; text-align: center;
      opacity: 0; transform-origin: 50% 50%;
    }}
    .cw {{ padding: 0 6px; border-radius: 4px; background-color: rgba(168,15,87,0); }}
    .cbox {{
      display: inline; background: #F82D8C; color: #fff; padding: 2px 16px 6px;
      font-family: "Archivo Black", sans-serif; font-size: 56px; line-height: 1.38;
      box-decoration-break: clone; -webkit-box-decoration-break: clone;
    }}
    .cg {{ padding: 0; box-sizing: border-box; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-layout-allow-overflow>
{chr(10).join(groups_html)}
  </div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
  window.__timelines["captions"] = tl;
  </script>
</template>
"""
open("compositions/captions.html", "w").write(out)
print("groups", len(GROUPS), "words", len(words))
