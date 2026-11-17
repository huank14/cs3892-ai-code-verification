"""Merge Bingsong's changes into the team's Google-Slides export (unpacked in team_unpacked/):
slide 5 -> new demo (slide1 of two.pptx), new slide after slide 9 -> poster layout (slide2),
backup page numbers 10/11 -> 11/12, repo link on the title slide."""
import re
import shutil
import zipfile
from pathlib import Path

S = Path(__file__).parent
T = S / 'team_unpacked'
two = zipfile.ZipFile(S / 'deck' / 'two.pptx')


def rd(p):
    return (T / p).read_text(encoding='utf-8')


def wr(p, s):
    (T / p).parent.mkdir(parents=True, exist_ok=True)
    (T / p).write_text(s, encoding='utf-8')


# 1. demo replaces slide 5 (keep the team's rels: layout1 + notesSlide5)
demo = two.read('ppt/slides/slide1.xml').decode('utf-8')
assert 'r:embed' not in demo and 'r:id=' not in demo
wr('ppt/slides/slide5.xml', demo)
wr('ppt/notesSlides/notesSlide5.xml', two.read('ppt/notesSlides/notesSlide1.xml').decode('utf-8'))

# 2. poster slide as slide12 (inserted after slide 9 in the show order)
poster = two.read('ppt/slides/slide2.xml').decode('utf-8')
(T / 'ppt/media/poster_draft.png').write_bytes(two.read('ppt/media/image-2-1.png'))
wr('ppt/slides/slide12.xml', poster)
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
wr('ppt/slides/_rels/slide12.xml.rels',
   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
   f'<Relationship Id="rId1" Type="{R}/image" Target="../media/poster_draft.png"/>'
   f'<Relationship Id="rId2" Type="{R}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
   f'<Relationship Id="rId3" Type="{R}/notesSlide" Target="../notesSlides/notesSlide12.xml"/>'
   '</Relationships>')
wr('ppt/notesSlides/notesSlide12.xml', two.read('ppt/notesSlides/notesSlide2.xml').decode('utf-8'))
wr('ppt/notesSlides/_rels/notesSlide12.xml.rels',
   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
   f'<Relationship Id="rId1" Type="{R}/notesMaster" Target="../notesMasters/notesMaster1.xml"/>'
   f'<Relationship Id="rId2" Type="{R}/slide" Target="../slides/slide12.xml"/>'
   '</Relationships>')
ct = rd('[Content_Types].xml')
for part, typ in (('/ppt/slides/slide12.xml', 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml'),
                  ('/ppt/notesSlides/notesSlide12.xml', 'application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml')):
    if part not in ct:
        ct = ct.replace('</Types>', f'<Override PartName="{part}" ContentType="{typ}"/></Types>')
wr('[Content_Types].xml', ct)
rels = rd('ppt/_rels/presentation.xml.rels')
if 'slides/slide12.xml' not in rels:
    rels = rels.replace('</Relationships>',
                        f'<Relationship Id="rId900" Type="{R}/slide" Target="slides/slide12.xml"/></Relationships>')
wr('ppt/_rels/presentation.xml.rels', rels)
pres = rd('ppt/presentation.xml')
if 'r:id="rId900"' not in pres:
    pres = pres.replace('<p:sldId id="264" r:id="rId14"/>', '<p:sldId id="264" r:id="rId14"/><p:sldId id="267" r:id="rId900"/>')
    assert 'rId900' in pres
wr('ppt/presentation.xml', pres)

# 3. backup page numbers
for n, new in ((10, '11'), (11, '12')):
    x = rd(f'ppt/slides/slide{n}.xml')
    assert x.count(f'<a:t>{n}</a:t>') == 1
    wr(f'ppt/slides/slide{n}.xml', x.replace(f'<a:t>{n}</a:t>', f'<a:t>{new}</a:t>'))

# 4. repo link on the title slide
x = rd('ppt/slides/slide1.xml')
if 'cs3892-ai-code-verification' not in x:
    sp = ('<p:sp><p:nvSpPr><p:cNvPr id="901" name="Repo link"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
          '<p:spPr><a:xfrm><a:off x="457200" y="4389120"/><a:ext cx="5669280" cy="274320"/></a:xfrm>'
          '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
          '<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"><a:noAutofit/></a:bodyPr>'
          '<a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="1200" u="sng"><a:solidFill><a:srgbClr val="E6EBEF"/></a:solidFill>'
          '<a:latin typeface="Arial"/></a:rPr><a:t>github.com/huank14/cs3892-ai-code-verification</a:t></a:r></a:p>'
          '</p:txBody></p:sp>')
    i = x.rfind('</p:spTree>')
    x = x[:i] + sp + x[i:]
    wr('ppt/slides/slide1.xml', x)

out = S / 'Verifying-AI-Generated-Code-Milestone1-merged.pptx'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    ctp = T / '[Content_Types].xml'
    z.write(ctp, '[Content_Types].xml')
    for p in sorted(T.rglob('*')):
        if p.is_file() and p != ctp:
            z.write(p, p.relative_to(T).as_posix())
print('wrote', out)
