# YXP 商品LP10月修正 初校：公開中ページ（2026-11-10 取得、ver1.4w）を土台に、原稿 26.11.09YXP入稿.docx どおりに直す
# 使い方: python3 -I build_yxp_oct.py <このフォルダ> <出力 index.html>
import sys,re,os
src=sys.argv[1]; out=sys.argv[2]
h=open(os.path.join(src,'live_index_261110.html'),encoding='utf8').read()
main=open(os.path.join(src,'main_oct.html'),encoding='utf8').read()
css=open(os.path.join(src,'add_oct.css'),encoding='utf8').read()
def rep(s,a,b,n=1):
    c=s.count(a)
    assert c==n,(a[:50],c,n)
    return s.replace(a,b)
CONTACT='''    <div class="yx-contact">
      <p class="yx-contact-ttl"><span>招へいに必要な実務をまとめてサポート。</span><span>呼び寄せエクスプレスです。</span></p>
      <div class="yx-contact-grid">
        <span class="yx-c-label">電話</span><a class="yx-c-tel" href="tel:05035386117">０５０　３５３８　６１１７</a><span class="yx-c-hours">月曜〜金曜／10時〜15時</span>
        <span class="yx-c-label">メール</span><a class="yx-c-mail" href="mailto:y-class@yobiyose-express.com"><img src="./images/mail-y-class.png" width="{w1}" height="{h1}" alt="y-class@yobiyose-express.com"></a><span class="yx-c-hours">24時間365日</span>
        <span class="yx-c-label yx-c-empty" aria-hidden="true"></span><a class="yx-c-mail" href="mailto:c-class@yobiyose-express.com"><img src="./images/mail-c-class.png" width="{w2}" height="{h2}" alt="c-class@yobiyose-express.com"></a><span class="yx-c-hours">24時間365日</span>
      </div>
    </div>'''
from PIL import Image
a=Image.open(os.path.join(src,'images/mail-y-class.png')).size; b=Image.open(os.path.join(src,'images/mail-c-class.png')).size
CONTACT=CONTACT.format(w1=a[0]//2,h1=a[1]//2,w2=b[0]//2,h2=b[1]//2)
assert main.count('{{CONTACT}}')==4
main=main.replace('{{CONTACT}}',CONTACT)
# 1 BUILD_TAG
h=rep(h,'<!-- BUILD_TAG: yxp2026_yclass_ver1.4w / 2026-08-18 -->','<!-- BUILD_TAG: yxp2026_yclass_oct_ver1.0 / 2026-11-10 -->')
# 2 title・meta（「11月」を原稿の大見出しに合わせる）
h=rep(h,'<title>11月の学会招へい まだ間に合います｜国際線航空券・海外研究者招へい｜株式会社呼び寄せエクスプレス</title>','<title>３月の学会講演者 予約・発券・お渡し、未だ間に合います｜国際線航空券・海外研究者招へい｜株式会社呼び寄せエクスプレス</title>')
h=rep(h,'招へいに必要な実務をまとめてサポート。11月開催の学会は早めのご相談を。">','招へいに必要な実務をまとめてサポート。早めのご相談・お見積りが、お得な航空券の確保につながります。">')
h=rep(h,'<meta property="og:title" content="11月の学会招へい まだ間に合います｜株式会社呼び寄せエクスプレス">','<meta property="og:title" content="３月の学会講演者 予約・発券・お渡し、未だ間に合います｜株式会社呼び寄せエクスプレス">')
# 3 CSS 追記
h=rep(h,'</style>',css+'</style>')
# 4 本文（main）を原稿どおりに差し替え
i=h.index('<main>'); j=h.index('</main>')+len('</main>')
assert h.count('<main>')==1 and h.count('</main>')==1
h=h[:i]+main.rstrip('\n')+h[j:]
# 5 追従バー（原稿に無い「メールにて ご相談／Zoomにて ご相談」）はコメントアウト
old='''<div class="sticky-cta">
  <a class="s-mail" href="mailto:yxp-mail@yobiyose-express.jp">メールにて ご相談</a>
  <a class="s-zoom" href="mailto:yxp-zoom@yobiyose-express.jp">Zoomにて ご相談</a>
</div>'''
h=rep(h,old,'<!-- 10月修正：原稿に無いため追従バーを非表示（戻す場合はこのコメントを外す）\n'+old+'\n-->')
# 6 公開中ページで <body> が2つ重なっているのを1つに
h=rep(h,'<body>\n<body>','<body>')
assert '11月' not in h, '11月が残っている'
for w in ['yxp-mail@','yxp-sign@','passenger_','平日10時～16時']:
    assert w not in h.replace(old,''),w
open(out,'w',encoding='utf8').write(h); print('ok',len(h))
