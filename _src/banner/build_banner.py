# 納品済みLP バナー修正 急ぎ2点（SWO 40venue・YXP yclass）
# 公開中ページを土台に、件数を数えた置換でバナーを重ねる。
# 使い方: python3 build_banner.py <live40.html> <liveyc.html> <出力フォルダ>
import sys, re, base64, pathlib
from PIL import Image, ImageDraw, ImageFont

src40, srcyc, out = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
(out / "swo" / "images").mkdir(parents=True, exist_ok=True)
(out / "yxp" / "images").mkdir(parents=True, exist_ok=True)
DATE = "2026-11-21"

def rep(s, a, b, n):
    c = s.count(a)
    if c != n:
        raise SystemExit(f"置換件数が違う: 期待{n} 実際{c} :: {a[:60]}")
    return s.replace(a, b)

# ---------- メールアドレス画像（透明背景・表示の2倍） ----------
def mail_png(text, color, path):
    f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 56)
    bb = f.getbbox(text)
    w, h = bb[2] - bb[0] + 8, 82
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - bb[0], (h - (bb[3] - bb[1])) // 2 - bb[1]), text, font=f, fill=color)
    im.save(path)
    return w, h

# ================= SWO 40venue =================
s = open(src40, encoding="utf8").read()
s = rep(s, "<!-- BUILD_TAG: swo2026_40venue_ver5.5wB / 2026-08-18 -->",
        f"<!-- BUILD_TAG: swo2026_40venue_banner_ver1.0 / {DATE} -->", 1)
MAIL = "web-team@science-web.online"
mw, mh = mail_png(MAIL, (15, 98, 180, 255), out / "swo" / "images" / "mail-web-team.png")
b64 = base64.b64encode((out / "swo" / "images" / "mail-web-team.png").read_bytes()).decode()

CSS40 = """
/* ===== 11月バナー修正：ここから ===== */
.cbanner{margin:28px auto 0;max-width:760px;border:2px solid var(--navy);border-radius:8px;background:var(--navy-l);padding:18px 22px;color:#000;}
.cbanner-ttl{font-size:clamp(17px,2.2vw,21px);font-weight:900;color:var(--navy);margin:0 0 10px;text-align:center;letter-spacing:.06em;}
.cbanner-grid{display:grid;grid-template-columns:auto auto auto;justify-content:center;align-items:center;column-gap:20px;row-gap:10px;}
.cb-label{font-size:clamp(15px,2vw,18px);font-weight:800;white-space:nowrap;}
.cb-tel{font-size:clamp(22px,4.6vw,32px);font-weight:900;line-height:1.3;color:#000;text-decoration:none;white-space:nowrap;letter-spacing:.03em;}
.cb-hours{font-size:clamp(13.5px,1.6vw,16px);white-space:nowrap;}
.cb-mail{display:block;line-height:0;grid-column:2 / span 2;}
.cb-mail img{height:clamp(20px,2.6vw,26px);width:auto;max-width:100%;}
@media(max-width:640px){
  .cbanner{padding:16px 16px;}
  .cbanner-grid{grid-template-columns:auto minmax(0,1fr);justify-content:start;column-gap:14px;row-gap:2px;}
  .cb-label{grid-row:span 2;align-self:start;padding-top:4px;}
  .cb-hours{grid-column:2;margin-bottom:10px;}
  .cb-mail{grid-column:2;padding-top:6px;}
}
.cbanner-note{margin:10px 0 0;text-align:center;font-size:clamp(13.5px,1.6vw,15px);font-weight:700;}
@media print{.cbanner{break-inside:avoid;}}
/* ===== 11月バナー修正：ここまで ===== */
</style>"""
s = rep(s, "</style>", CSS40, 1)

def banner40():
    return f"""
    <!-- 11月バナー修正：お問合せのバナー（メールアドレスは画像。押すとメールソフトが起動） -->
    <div class="cbanner" role="group" aria-label="お問合せ">
      <p class="cbanner-ttl">お問合せは</p>
      <div class="cbanner-grid">
        <span class="cb-label">電話</span><a class="cb-tel" href="tel:050-3538-7006">050-3538-7006</a><span class="cb-hours">平日10時から16時まで</span>
        <span class="cb-label">メール</span><a class="cb-mail" href="mailto:{MAIL}"><img src="data:image/png;base64,{b64}" width="{mw//2}" height="{mh//2}" alt="{MAIL}"></a>
      </div>
      <p class="cbanner-note">開封後6時間以内に返信いたします</p>
    </div>"""

# トップ：画像（スライドショー）の直下
a = '      <img src="images/lecture.png" alt="公演の様子">\n    </div>    \n  </div>\n</div>'
s = rep(s, a, a.replace("    </div>    \n  </div>\n</div>", "    </div>    " + banner40() + "\n  </div>\n</div>"), 1)
# 料金表（40万円の画面）：書類ボタンの直前
i0 = s.index('<section id="price40"'); i1 = s.index('<section id="faq"')
seg = s[i0:i1]
b = '    <div class="btns" style="margin-top:26px;">\n      <button class="btn btn-quote"'
if seg.count(b) != 1: raise SystemExit("料金表の書類ボタンが1か所でない")
seg = seg.replace(b, banner40().lstrip("\n") + "\n\n" + b)
s = s[:i0] + seg + s[i1:]
(out / "swo" / "index.html").write_text(s, encoding="utf8")

# ================= YXP yclass =================
y = open(srcyc, encoding="utf8").read()
y = rep(y, "<!-- BUILD_TAG: yxp2026_yclass_oct_ver1.0 / 2026-11-10 -->",
        f"<!-- BUILD_TAG: yxp2026_yclass_banner_ver1.0 / {DATE} -->", 1)
# 連絡先の枠（ページ内4か所・同じ部品）を罫線で囲んだバナーにする
y = rep(y, ".yx-contact{margin-top:44px;border-top:3px solid #0070C0;padding-top:22px;}",
        ".yx-contact{margin-top:44px;border:2px solid #0070C0;border-radius:8px;background:#EEF6FC;padding:20px 22px;}", 1)
y = rep(y, '<span class="yx-c-hours">月曜〜金曜／10時〜15時</span>',
        '<span class="yx-c-hours">平日10時から16時まで</span>', 4)
y = rep(y, '<a class="yx-c-tel" href="tel:05035386117">０５０　３５３８　６１１７</a>',
        '<a class="yx-c-tel" href="tel:05035386117">050-3538-6117</a>', 4)
y = rep(y, '<span class="yx-c-hours">24時間365日</span>\n      </div>\n    </div>',
        '<span class="yx-c-hours">24時間365日</span>\n      </div>\n      <p class="yx-c-note">開封後6時間以内に返信いたします</p>\n    </div>', 4)
y = rep(y, "/* ===== 10月修正：ここまで ===== */\n</style>",
        "/* ===== 10月修正：ここまで ===== */\n/* ===== 11月バナー修正：ここから ===== */\n.yx-c-note{margin:12px 0 0;text-align:center;font-size:clamp(13.5px,1.6vw,16px);font-weight:700;}\n@media(max-width:640px){.yx-contact{padding:16px 14px;}.yx-contact-ttl{font-size:clamp(12.5px,4vw,15px);}}\n/* ===== 11月バナー修正：ここまで ===== */\n</style>", 1)
(out / "yxp" / "index.html").write_text(y, encoding="utf8")
print("ok", mw, mh)
