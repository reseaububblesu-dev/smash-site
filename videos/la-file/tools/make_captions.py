"""Builds compositions/captions.html from assets/transcript.json.
Display words are written by hand (correct spelling) and take their timing
from the transcript word at the same position."""
import json, html
words = json.load(open("assets/transcript.json"))
words = words if isinstance(words, list) else words["words"]
# (display text, transcript index) per group
GROUPS = [
    [("PREMIER", 8), ("INDICE :", 9)],
    [("DES", 10), ("SMASH", 11), ("BURGERS,", 12)],
    [("ÉCRASÉS", 13), ("MINUTE", 14)],
    [("SUR", 15), ("LA", 16), ("PLANCHA.", 17)],
    [("LE", 18), ("FROMAGE", 19), ("QUI", 20), ("COULE…", 21)],
    [("ET", 22), ("LES", 23), ("FRITES", 24)],
    [("QUI", 25), ("VONT", 26), ("AVEC.", 27)],
    [("DEUXIÈME", 28), ("INDICE :", 29)],
    [("LE", 30), ("POULET", 31), ("FRIT,", 32)],
    [("BIEN", 33), ("CROUSTILLANT.", 34)],
    [("ET", 35), ("POUR", 36), ("FINIR…", 37)],
    [("LES", 38), ("MILKSHAKES.", 39)],
    [("SMASH", 40), ("BY", 41), ("BUBBLE", 42), ("SÜ.", 43)],
    [("AVENUE", 44), ("PASTEUR,", 45)],
    [("AUX", 46), ("LILAS.", 47)],
]
FIX = {44: 16.5}  # whisper put "Avenue" too early
def ws(i): return FIX.get(i, words[i]["start"])
groups_html, js = [], []
for g, grp in enumerate(GROUPS):
    start = round(ws(grp[0][1]) - 0.05, 2)
    nxt = GROUPS[g + 1] if g + 1 < len(GROUPS) else None
    end = round(ws(nxt[0][1]) - 0.05, 2) if nxt else 17.7
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
