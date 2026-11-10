# メールアドレス画像（透明背景・表示の2倍）
from PIL import Image, ImageDraw, ImageFont
F='/usr/share/fonts/opentype/inter/Inter-Bold.otf'
def mk(addr,out):
    f=ImageFont.truetype(F,60)
    l,t,r,b=f.getbbox(addr)
    asc,desc=f.getmetrics()
    W=r-l+16; H=asc+desc+8
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    ImageDraw.Draw(im).text((8-l,4),addr,font=f,fill=(0,112,192,255))
    im.save(out,optimize=True); print(out,im.size)
mk('y-class@yobiyose-express.com','images/mail-y-class.png')
mk('c-class@yobiyose-express.com','images/mail-c-class.png')
