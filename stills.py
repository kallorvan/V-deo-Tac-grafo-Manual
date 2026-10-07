import os
from pathlib import Path
from build import timeline, scene_html, ROOT, W, H
from playwright.sync_api import sync_playwright
from PIL import Image
os.makedirs("build",exist_ok=True)
tls=timeline()
ims=[]
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport=dict(width=W,height=H))
    for tl in tls:
        doc,_=scene_html(tl); path=os.path.abspath(f"build/{tl['scene']['id']}.html"); open(path,"w").write(doc)
        pg.goto(Path(path).as_uri()); pg.evaluate("document.fonts.ready"); pg.evaluate(f"render({tl['total']})")
        f=f"build/still_{tl['scene']['id']}.png"; pg.screenshot(path=f); ims.append(f)
    br.close()
g=Image.new("RGB",(960*2,540*7),"white")
for i,f in enumerate(ims):
    im=Image.open(f).resize((960,540)); g.paste(im,((i%2)*960,(i//2)*540))
g.save("build/contact.png")
