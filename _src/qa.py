import sys,asyncio
from playwright.async_api import async_playwright
url=sys.argv[1]; outdir=sys.argv[2]
W=[320,375,414,768,900,1024,1280,1440]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w in W:
            pg=await b.new_page(viewport={'width':w,'height':900})
            errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            bad=[]; pg.on('response',lambda r: bad.append((r.status,r.url)) if r.status>=400 else None)
            await pg.goto(url,wait_until='load'); await pg.wait_for_timeout(400)
            r=await pg.evaluate('''()=>{const d=document.documentElement;
              const sp=[...document.querySelectorAll('.yx-h1 span')].map(s=>{const cs=getComputedStyle(s);return [parseFloat(cs.fontSize).toFixed(1),Math.round(s.getBoundingClientRect().height/parseFloat(cs.lineHeight)),Math.round(s.scrollWidth),Math.round(s.clientWidth)]});
              const cols=[...document.querySelectorAll('.yx-col')].map(c=>Math.round(c.getBoundingClientRect().left)+','+Math.round(c.getBoundingClientRect().top));
              const m=[...document.querySelectorAll('.yx-c-mail img')].slice(0,2).map(i=>Math.round(i.getBoundingClientRect().width)+'x'+Math.round(i.getBoundingClientRect().height)+(i.naturalWidth?'':'!BROKEN'));
              const hd=getComputedStyle(document.querySelector('.nav-btn')).display;
              return {over:d.scrollWidth-d.clientWidth,h1:sp,cols,mail:m,navbtn:hd,h:d.scrollHeight}}''')
            print(w,r,errs,bad)
            await pg.screenshot(path=f'{outdir}/w{w}.png',full_page=True)
            await pg.close()
        await b.close()
asyncio.run(main())
