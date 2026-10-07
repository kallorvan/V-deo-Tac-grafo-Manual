# -*- coding: utf-8 -*-
import json, os, subprocess, sys, html, math
from scenes import SCENES, MODULES, beat_duration
from playwright.sync_api import sync_playwright

FPS = 30
W, H = 1920, 1080
ROOT = os.path.dirname(os.path.abspath(__file__))
from pathlib import Path
ASSETS = Path(ROOT, "assets").as_uri() + "/"
AUDIO_DIR = os.path.join(ROOT, "audio")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "out.mp4")
PREVIEW = "--preview" in sys.argv
ANIM = 0.65

NAVY = "#0B2350"; CORAL = "#E9516B"; LILAC = "#AB85B6"; YEL = "#F9D590"


def audio_len(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


# ---------- timing ----------
import re, glob
PRE, POST = 0.4, 0.6


def silences(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "silencedetect=noise=-35dB:d=0.22", "-f", "null", "-"],
                       capture_output=True, text=True)
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return list(zip(st, en))


def sentences(t):
    return [x for x in re.split(r"(?<=[.!?:])\s+", t.strip()) if x]


def timeline():
    out = []
    for s in SCENES:
        n = len(s["beats"])
        durs = [beat_duration(b["narr"], i == 0, i == n - 1) for i, b in enumerate(s["beats"])]
        cand = glob.glob(os.path.join(AUDIO_DIR, "*" + s["id"] + ".mp3"))
        audio, times = None, {}
        if cand:
            audio = cand[0]
            L = audio_len(audio)
            sil = silences(audio)
            # início/fim da fala
            s0 = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
            s1 = sil[-1][0] if sil and sil[-1][1] > L - 0.05 else L
            sil = [x for x in sil if x[0] > s0 + 0.1 and x[1] < s1 - 0.1]
            # sentenças de todos os beats, com posição esperada proporcional aos caracteres
            sents = [(bi, j, t) for bi, b in enumerate(s["beats"]) for j, t in enumerate(sentences(b["narr"]))]
            tot = sum(len(t) for _, _, t in sents)
            exp, acc = [], 0
            for (bi, j, t) in sents:
                exp.append(s0 + (s1 - s0) * acc / tot); acc += len(t)
            m, S = len(sents), len(sil)
            if m - 1 <= S and m > 1:
                INF = 1e18
                cost = lambda k, i: abs(sil[i][1] - exp[k]) - 3.0 * (sil[i][1] - sil[i][0])
                dp = [[INF] * S for _ in range(m)]; bk = [[-1] * S for _ in range(m)]
                for i in range(S):
                    dp[1][i] = cost(1, i)
                for k in range(2, m):
                    best, bi_ = INF, -1
                    for i in range(S):
                        if i - 1 >= 0 and dp[k - 1][i - 1] < best:
                            best, bi_ = dp[k - 1][i - 1], i - 1
                        if best < INF:
                            dp[k][i] = best + cost(k, i); bk[k][i] = bi_
                i = min(range(S), key=lambda i: dp[m - 1][i]); sel = [0] * m
                for k in range(m - 1, 0, -1):
                    sel[k] = i; i = bk[k][i]
                starts = [s0] + [sil[sel[k]][1] - 0.05 for k in range(1, m)]
            else:
                starts = exp
            bstart = {}
            for (bi, j, t), st in zip(sents, starts):
                bstart.setdefault(bi, st)
                times.setdefault(bi, []).append(PRE + st)
            total = PRE + L + POST
            bs = [0.0] + [PRE + bstart[i] for i in range(1, n)] + [total]
            durs = [bs[i + 1] - bs[i] for i in range(n)]
        out.append(dict(scene=s, durs=durs, total=sum(durs), audio=audio, times=times))
    return out


# ---------- html ----------
ICON_CHECK = '<svg viewBox="0 0 24 24" width="30" height="30"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_WARN = '<svg viewBox="0 0 24 24" width="34" height="34"><path d="M12 3L2 21h20L12 3z" fill="#fff"/><path d="M12 10v5" stroke="#E9516B" stroke-width="2.6" stroke-linecap="round"/><circle cx="12" cy="18" r="1.4" fill="#E9516B"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" width="34" height="34"><path d="M4 12h14M13 6l6 6-6 6" fill="none" stroke="#E9516B" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'

CSS = f"""
@font-face{{font-family:Poppins;font-weight:400;src:url({ASSETS}fonts/Poppins-Regular.ttf)}}
@font-face{{font-family:Poppins;font-weight:500;src:url({ASSETS}fonts/Poppins-Medium.ttf)}}
@font-face{{font-family:Poppins;font-weight:600 700;src:url({ASSETS}fonts/Poppins-Bold.ttf)}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;font-family:Poppins,sans-serif;color:{NAVY}}}
body{{background:#F4F6FB}}
.a{{opacity:0;will-change:transform,opacity}}
/* content */
.top{{position:absolute;left:120px;top:70px;right:120px}}
.chip{{display:inline-flex;align-items:center;gap:12px;font-weight:600;font-size:24px;letter-spacing:3px;text-transform:uppercase;color:{CORAL}}}
.chip:before{{content:"";width:46px;height:6px;border-radius:3px;background:{CORAL}}}
h1{{font-weight:700;font-size:66px;line-height:1.1;margin-top:10px;letter-spacing:-0.5px}}
.media{{position:absolute;left:120px;top:270px;width:700px;height:660px;border-radius:32px;background:#fff;
  box-shadow:0 30px 60px -20px rgba(11,35,80,.25);display:flex;align-items:center;justify-content:center;overflow:hidden}}
.media img{{width:86%;height:80%;object-fit:contain}}
.media .cap{{position:absolute;bottom:26px;left:0;right:0;text-align:center;font-size:22px;font-weight:500;color:#5a6682}}
.panel{{background:{NAVY};color:#fff;flex-direction:column;overflow:hidden}}
.panel .big{{font-weight:700;font-size:170px;line-height:1;color:#fff;position:relative;z-index:2;text-align:center}}
.panel .lbl{{font-size:34px;font-weight:500;text-align:center;max-width:560px;margin-top:24px;color:{YEL};position:relative;z-index:2;line-height:1.3}}
.panel .shp{{position:absolute;right:-420px;bottom:-240px;width:1100px;opacity:.9}}
.items{{position:absolute;left:900px;top:270px;width:900px;height:660px;display:flex;flex-direction:column;justify-content:center;gap:22px}}
.items.grid{{display:grid;grid-template-columns:1fr 1fr;align-content:center;gap:18px 22px}}
.it{{display:flex;align-items:center;gap:24px;background:#fff;border-radius:22px;padding:22px 30px;
  box-shadow:0 14px 30px -18px rgba(11,35,80,.35);font-size:33px;font-weight:500;line-height:1.28}}
.it .ic{{flex:none;width:58px;height:58px;border-radius:50%;background:{CORAL};display:flex;align-items:center;justify-content:center;
  color:#fff;font-weight:700;font-size:30px}}
.it.num .ic{{background:{NAVY}}}
.it .sub{{display:block;font-size:26px;color:#5a6682;margin-top:6px}}
.it.warn{{background:{CORAL};color:#fff;font-weight:600}}
.it.warn .ic{{background:rgba(255,255,255,.18)}}
.it.field{{font-size:28px;padding:18px 22px;gap:18px}}
.it.field .ic{{width:48px;height:48px;font-size:26px;background:{NAVY}}}
.head{{grid-column:1/-1;font-size:36px;font-weight:700;color:{NAVY};padding:0 4px 10px;border-bottom:4px solid {YEL};margin-bottom:8px}}
.flow{{display:flex;align-items:center;gap:14px;flex-wrap:wrap;background:transparent;box-shadow:none;padding:6px 0}}
.flow .lab{{font-weight:600;font-size:30px;width:100%;margin-bottom:4px}}
.flow .st{{background:{NAVY};color:#fff;border-radius:18px;padding:18px 26px;font-weight:600;font-size:30px}}
.flow.nums .st{{min-width:96px;text-align:center;font-size:44px;padding:14px 18px}}
.foot{{position:absolute;left:0;right:0;bottom:0;height:86px;background:{NAVY};display:flex;align-items:center;padding:0 60px;gap:40px}}
.foot img.l{{height:52px}}
.foot img.r{{height:36px;filter:brightness(0) invert(1);margin-left:auto}}
.prog{{display:flex;gap:10px;flex:1;justify-content:center}}
.seg{{display:flex;flex-direction:column;gap:8px;width:230px;font-size:17px;font-weight:500;color:rgba(255,255,255,.45)}}
.seg i{{display:block;height:6px;border-radius:3px;background:rgba(255,255,255,.2)}}
.seg.done i{{background:rgba(249,213,144,.6)}}
.seg.on{{color:#fff}} .seg.on i{{background:{CORAL}}}
/* cover */
.cover{{position:absolute;inset:0;background:url({ASSETS}bg_navy.png) center/cover;color:#fff;overflow:hidden}}
.cover .shp{{position:absolute;inset:0;width:100%;height:100%}}
.cover .logo{{position:absolute;left:140px;top:140px;height:150px}}
.cover .t{{position:absolute;left:140px;top:420px;font-size:92px;font-weight:700;line-height:1.08;max-width:1150px}}
.cover .s{{position:absolute;left:140px;top:660px;font-size:44px;font-weight:500;color:{YEL}}}
.cover .bar{{position:absolute;left:140px;top:395px;width:120px;height:10px;border-radius:5px;background:{CORAL}}}
.cover .din{{position:absolute;left:140px;bottom:110px;height:52px;filter:brightness(0) invert(1)}}
"""


def item_html(it):
    t = it["t"]
    if t == "head":
        return f'<div class="head">{html.escape(it["text"])}</div>'
    if t == "flow":
        parts = []
        if it.get("label"):
            parts.append(f'<div class="lab">{html.escape(it["label"])}</div>')
        for i, s in enumerate(it["steps"]):
            if i:
                parts.append(ARROW)
            parts.append(f'<div class="st">{html.escape(s)}</div>')
        nums = " nums" if all(len(s) <= 2 for s in it["steps"]) else ""
        return f'<div class="flow{nums}">{"".join(parts)}</div>'
    ic = {"check": ICON_CHECK, "warn": ICON_WARN}.get(t, html.escape(it.get("n", "")))
    sub = f'<span class="sub">{html.escape(it["sub"])}</span>' if it.get("sub") else ""
    return f'<div class="it {t}"><div class="ic">{ic}</div><div>{html.escape(it["text"])}{sub}</div></div>'


def wrap(el, kind, t0, d=ANIM):
    # insere atributos de animação no primeiro elemento
    i = el.index(">")
    tag_open = el[:i]
    if 'class="' in tag_open:
        tag_open = tag_open.replace('class="', 'class="a ', 1)
    else:
        tag_open += ' class="a"'
    return f'{tag_open} data-k="{kind}" data-t0="{t0:.3f}" data-d="{d:.3f}"' + el[i:]


def scene_html(tl):
    s, durs = tl["scene"], tl["durs"]
    starts = [sum(durs[:i]) for i in range(len(durs))]
    anims = []  # (t0,d)

    def A(el, kind, t0, d=ANIM):
        anims.append((t0, d))
        return wrap(el, kind, t0, d)

    if s["layout"] in ("cover", "end"):
        body = '<div class="cover">'
        body += A(f'<img class="shp" src="{ASSETS}shapes.png">', "fade", 0.0, 1.4)
        body += A(f'<img class="logo" src="{ASSETS}toliman_white.png">', "up", 0.2)
        body += A('<div class="bar"></div>', "left", 0.45)
        body += A(f'<div class="t">{html.escape(s["title"])}</div>', "up", 0.5)
        body += A(f'<div class="s">{html.escape(s["sub"])}</div>', "up", 0.8)
        body += A(f'<img class="din" src="{ASSETS}dinamo.png">', "fade", 1.1)
        body += "</div>"
    else:
        chip = s.get("chip") or f'Módulo {s["module"] + 1} de {len(MODULES)}'
        body = '<div class="top">' + A(f'<div class="chip">{html.escape(chip)}</div>', "left", 0.05) + \
               A(f'<h1>{html.escape(s["title"])}</h1>', "up", 0.15) + '</div>'
        if s.get("img"):
            cap = f'<div class="cap">{html.escape(s["caption"])}</div>' if s.get("caption") else ""
            body += A(f'<div class="media"><img src="{ASSETS}{s["img"]}">{cap}</div>', "scale", 0.25, 0.8)
        else:
            big, lbl = s["panel"]
            body += A(f'<div class="media panel"><img class="shp" src="{ASSETS}shapes.png"><div class="big">{html.escape(big)}</div><div class="lbl">{html.escape(lbl)}</div></div>', "scale", 0.25, 0.8)
        items = [item_html(it) for it in s["items"]]
        for bi, b in enumerate(s["beats"]):
            show = b.get("show", [])
            if not show:
                continue
            base = starts[bi] + (0.55 if bi == 0 else 0.15)
            st_list = tl.get("times", {}).get(bi)
            if b.get("spread") and st_list and len(st_list) >= len(show):
                off = len(st_list) - len(show)
                for j, idx in enumerate(show):
                    items[idx] = A(items[idx], "up", st_list[off + j] + 0.05)
                continue
            if b.get("spread"):
                step = (durs[bi] * 0.85) / len(show)
            else:
                step = 0.2
            for j, idx in enumerate(show):
                items[idx] = A(items[idx], "up", base + j * step)
        cls = "items grid" if s.get("grid") else "items"
        body += f'<div class="{cls}">' + "".join(items) + "</div>"
        # rodapé com progresso
        segs = ""
        m = s.get("module")
        cur = m if m is not None else (-1 if s["id"] == "agenda" else len(MODULES))
        for i, name in enumerate(MODULES):
            c = "on" if i == cur else ("done" if i < cur else "")
            segs += f'<div class="seg {c}"><i></i>{html.escape(name)}</div>'
        body += f'<div class="foot"><img class="l" src="{ASSETS}toliman_white.png"><div class="prog">{segs}</div><img class="r" src="{ASSETS}dinamo.png"></div>'

    js = """
    function ease(p){return 1-Math.pow(1-p,3)}
    window.render=function(t){
      document.querySelectorAll('.a').forEach(e=>{
        const t0=+e.dataset.t0, d=+e.dataset.d; let p=(t-t0)/d; p=Math.max(0,Math.min(1,p)); const q=ease(p);
        e.style.opacity=q; const k=e.dataset.k;
        if(k==='up') e.style.transform=`translateY(${(1-q)*34}px)`;
        else if(k==='left') e.style.transform=`translateX(${-(1-q)*50}px)`;
        else if(k==='scale') e.style.transform=`scale(${0.93+0.07*q})`;
      });
    }
    """
    doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}<script>{js}</script></body></html>'
    return doc, anims


def main():
    tls = timeline()
    total = sum(t["total"] for t in tls)
    print(f"Duração total: {total:.1f}s ({total/60:.1f} min)")
    os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
    json.dump([dict(id=t["scene"]["id"], durs=t["durs"], total=t["total"]) for t in tls],
              open(os.path.join(ROOT, "build", "timeline.json"), "w"), indent=1)

    silent = os.path.join(ROOT, "build", "video_silent.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), silent],
                          stdin=subprocess.PIPE)
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport=dict(width=W, height=H))
        scenes = tls if not PREVIEW else tls[:3]
        prev_last = None
        for tl in scenes:
            doc, anims = scene_html(tl)
            path = os.path.join(ROOT, "build", tl["scene"]["id"] + ".html")
            open(path, "w").write(doc)
            pg.goto(Path(path).as_uri()); pg.wait_for_load_state("load")
            pg.evaluate("document.fonts.ready")
            nframes = int(round(tl["total"] * FPS))
            last = None
            XF = 10  # crossfade entre cenas (frames)
            for f in range(nframes):
                t = f / FPS
                active = last is None or any(t0 - 1 / FPS <= t <= t0 + d + 1 / FPS for t0, d in anims)
                if active:
                    pg.evaluate(f"render({t})")
                    last = pg.screenshot(type="png")
                    if f < XF and prev_last is not None:
                        # dissolve suave a partir do último frame da cena anterior
                        from PIL import Image
                        import io
                        a = Image.open(io.BytesIO(prev_last)).convert("RGB")
                        b = Image.open(io.BytesIO(last)).convert("RGB")
                        m = Image.blend(a, b, (f + 1) / XF)
                        buf = io.BytesIO(); m.save(buf, "PNG", compress_level=1)
                        ff.stdin.write(buf.getvalue())
                        continue
                ff.stdin.write(last)
            pg.evaluate(f"render({tl['total']})")
            prev_last = pg.screenshot(type="png")
            print("ok", tl["scene"]["id"], f"{tl['total']:.1f}s", flush=True)
        br.close()
    ff.stdin.close(); ff.wait()

    # áudio: narração por cena (se existir) ou faixa silenciosa
    have_audio = any(t["audio"] for t in tls)
    if have_audio:
        inputs, filt, t0 = [], [], 0.0
        for i, t in enumerate(tls):
            if t["audio"]:
                inputs += ["-i", t["audio"]]
                k = len(inputs) // 2
                ms = int((t0 + 0.4) * 1000)
                filt.append(f"[{k}:a]adelay={ms}|{ms}[a{k}]")
            t0 += t["total"]
        n = len(filt)
        mix = ";".join(filt) + ";" + "".join(f"[a{i+1}]" for i in range(n)) + f"amix=inputs={n}:normalize=0[aout]"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", silent] + inputs + ["-filter_complex", mix, "-map", "0:v", "-map", "[aout]",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", OUT]
    else:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
               "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest", OUT]
    subprocess.run(cmd, check=True)
    print("gerado:", OUT)


if __name__ == "__main__":
    main()
