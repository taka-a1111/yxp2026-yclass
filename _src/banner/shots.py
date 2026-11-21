import asyncio,sys
from playwright.async_api import async_playwright
# 使い方: python3 shots.py <名前> <URL> <幅,…>
name,url=sys.argv[1],sys.argv[2]; widths=[int(w) for w in sys.argv[3].split(',')]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for w in widths:
      pg=await b.new_page(viewport={"width":w,"height":900})
      errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
      await pg.goto(url,wait_until="networkidle",timeout=60000); await pg.wait_for_timeout(800)
      info=await pg.evaluate("""()=>{const sel=document.querySelectorAll('.cbanner,.yx-contact');return {sw:document.documentElement.scrollWidth-document.documentElement.clientWidth,
        boxes:[...sel].map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.top+scrollY),Math.round(r.left),Math.round(r.width),Math.round(r.height)]}),
        imgs:[...document.querySelectorAll('.cb-mail img,.yx-c-mail img')].map(i=>[i.alt,i.naturalWidth,Math.round(i.getBoundingClientRect().width)]).slice(0,3)}}""")
      print(name,w,info,errs[:2])
      els=await pg.query_selector_all('.cbanner,.yx-contact')
      for k,e in enumerate(els[:2]):
        await e.scroll_into_view_if_needed(); await e.screenshot(path=f"shot_{name}_{w}_{k}.png")
      await pg.close()
    await b.close()
asyncio.run(main())
