"""Builds compositions/captions.html from assets/transcript.json.
Display words are written by hand (correct spelling) and take their timing
from the transcript word at the same position."""
import json, html
OFFSET = 0.1  # the voice starts 0.1 s into the film
words = json.load(open("assets/voice-perso/mots.json"))
# (display text, transcript index) per group
GROUPS = [
    [("Des", 9), ("smash", 10), ("burgers", 11)],
    [("de", 12), ("qualité", 13)],
    [("écrasés", 14), ("à", 15), ("la", 16), ("minute", 17)],
    [("sur", 18), ("la", 19), ("plancha", 20)],
    [("Un", 21), ("fromage", 22), ("qui", 23), ("coule", 24)],
    [("des", 25), ("frites", 26), ("maison", 27)],
    [("qui", 28), ("vont", 29), ("avec", 30)],
    [("Le", 31), ("poulet", 32), ("frit", 33)],
    [("bien", 34), ("croustillant", 35)],
    [("Et", 36), ("pour", 37), ("finir", 38)],
    [("des", 39), ("milkshakes", 40)],
    [("des", 41), ("tiramisus", 42)],
    [("tout", 43), ("ce", 44), ("qu'il", 45), ("faut", 47)],
    [("Smash", 48), ("by", 49), ("Bubble", 50), ("Sü", 50.5)],
    [("81", 51), ("avenue", 52), ("Pasteur", 53)],
    [("aux", 54), ("Lilas", 55)],
]
END = 21.45  # the end card takes over
def ws(i):
    if i == 50.5:  # "Bubblesu" is one word for whisper: split it in two
        w = words[50]; return round((w["start"] + w["end"]) / 2 + OFFSET, 2)
    return round(words[i]["start"] + OFFSET, 2)
groups_html, js = [], []
for g, grp in enumerate(GROUPS):
    start = round(ws(grp[0][1]) - 0.06, 2)
    nxt = GROUPS[g + 1] if g + 1 < len(GROUPS) else None
    end = round(ws(nxt[0][1]) - 0.06, 2) if nxt else END
    text = html.escape(" ".join(t for t, _ in grp))
    groups_html.append(f'    <div class="cg" id="cg{g}"><span class="ct">{text}</span></div>')
    js.append(f'  tl.fromTo("#cg{g} .ct", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.18, ease: "power3.out" }}, {start});')
    js.append(f'  tl.to("#cg{g} .ct", {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, {end - 0.1:.2f});')
    js.append(f'  tl.set("#cg{g}", {{ visibility: "hidden" }}, {end:.2f});')
out = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    #cap-scrim {{
      position: absolute; left: 0; top: 860px; width: 1080px; height: 560px; opacity: 0;
      background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.42) 50%, rgba(0,0,0,0) 100%);
    }}
    .cg {{ position: absolute; left: 140px; width: 800px; top: 1112px; text-align: center; }}
    .ct {{
      display: inline-block; color: #fff; font-family: "Inter", sans-serif; font-weight: 700;
      font-size: 58px; line-height: 1.15; letter-spacing: -0.02em; opacity: 0;
      text-shadow: 0 2px 18px rgba(0,0,0,0.55);
    }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-layout-allow-overflow>
    <div id="cap-scrim"></div>
{chr(10).join(groups_html)}
  </div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  // A soft band behind the captions while they run (from the first caption to the end card).
  tl.fromTo("#cap-scrim", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {round(ws(GROUPS[0][0][1]) - 0.2, 2)});
  tl.to("#cap-scrim", {{ opacity: 0, duration: 0.2 }}, {END - 0.2});
{chr(10).join(js)}
  window.__timelines["captions"] = tl;
  </script>
</template>
"""
open("compositions/captions.html", "w").write(out)
print("groups", len(GROUPS), "words", len(words))
