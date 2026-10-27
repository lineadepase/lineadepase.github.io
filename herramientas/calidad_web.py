"""Metadatos únicos y recursos adaptados; conserva originales y textos editoriales."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib, json, os, re
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
BASE='https://lineadepase.com/'


def attrs(tag):
    class Tag(HTMLParser):
        def handle_starttag(self, _, values): self.values=dict(values)
    parser=Tag(); parser.feed(tag)
    return parser.values


def metadata(raw, root=ROOT):
    head, tail=raw.split('</head>',1)
    seen=set(); chosen={}
    def unique(match):
        a=attrs(match[0]); key=a.get('property',a.get('name',''))
        if not (key.startswith('og:') or key.startswith('twitter:')):return match[0]
        if key in seen:return ''
        seen.add(key); chosen[key]=a.get('content','')
        return match[0]
    head=re.sub(r'<meta\b[^>]*>',unique,head)
    image=chosen.get('og:image','')
    if image.startswith(BASE):
        path=image.removeprefix(BASE)
        resource=root/path
        if resource.is_file() and resource.suffix.lower() in ('.png','.jpg','.jpeg','.webp'):
            with Image.open(resource) as im: width,height=im.size; kind=im.format.lower().replace('jpg','jpeg')
            for key,value in [('og:image:width',width),('og:image:height',height),('og:image:type','image/'+kind),('twitter:image',image)]:
                tag=f'<meta {"name" if key.startswith("twitter:") else "property"}="{key}" content="{value}">'
                if key in seen:head=re.sub(r'<meta\b[^>]*(?:name|property)="'+re.escape(key)+r'"[^>]*>',lambda _:tag,head)
                else:head+='\n'+tag
            if '/assets/compartir/' not in image and 'name="imagen-editorial"' not in head:
                head+=f'\n<meta name="imagen-editorial" content="{path}">'
            def schema(m):
                value=json.loads(m[1])
                for item in value.get('@graph',[value]):
                    if item.get('@type')=='Article':item['image']=[image]
                return '<script type="application/ld+json">'+json.dumps(value,ensure_ascii=False)+'</script>'
            head=re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,head,flags=re.S)
    return head+'</head>'+tail


def imagenes(raw, page, root=ROOT):
    def adapt(match):
        tag=match[0]; a=attrs(tag); src=a.get('src',''); url=urlsplit(src)
        if url.scheme or url.netloc or not url.path:return tag
        source=(root/unquote(url.path).lstrip('/')) if src.startswith('/') else page.parent/unquote(url.path)
        source=source.resolve()
        if not source.is_relative_to(root.resolve()) or not source.is_file() or source.suffix.lower() not in ('.png','.jpg','.jpeg','.webp'):return tag
        with Image.open(source) as im:
            width,height=im.size
            add=''
            if not a.get('width'):add+=f' width="{width}"'
            if not a.get('height'):
                declared=int(a.get('width',width)) if str(a.get('width',width)).isdigit() else width
                add+=f' height="{round(height*declared/width)}"'
            if source.stat().st_size>300000 and width>800 and 'srcset' not in a:
                digest=hashlib.sha256(source.read_bytes()).hexdigest()[:10]
                folder=root/'assets/adaptadas';folder.mkdir(exist_ok=True)
                versions=[]
                for size in (480,800,1200):
                    if size>=width:continue
                    target=folder/f'{source.stem}-{digest}-{size}.webp'
                    if not target.exists():
                        copy=im.copy();copy.thumbnail((size,round(height*size/width)))
                        copy.save(target,'WEBP',quality=82,method=6)
                    relative=os.path.relpath(target,page.parent).replace('\\','/')
                    versions.append(f'{relative} {size}w')
                versions.append(f'{src} {width}w')
                add+=' srcset="'+escape(', '.join(versions),quote=True)+'" sizes="(max-width: 640px) calc(100vw - 48px), 800px"'
            return tag[:-1]+add+'>'
    return re.sub(r'<img\b[^>]*>',adapt,raw)


def build(root=ROOT):
    changed=0
    for page in root.rglob('*.html'):
        if any(x in ('.git','analisis') for x in page.relative_to(root).parts):continue
        raw=page.read_text(encoding='utf-8')
        if '</head>' not in raw or '<main' not in raw:continue
        new=imagenes(metadata(raw,root),page,root)
        if new!=raw:
            page.write_text(new,encoding='utf-8',newline='\n');changed+=1
    return changed


if __name__=='__main__':print('Páginas mejoradas:',build())
