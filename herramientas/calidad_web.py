"""Metadatos únicos y recursos adaptados; conserva originales y textos editoriales."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib, json, os, re
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
BASE='https://lineadepase.com/'
RESPONSIVE_IMAGE_MIN_BYTES=300_000
PAGE_IMAGE_MIN_BYTES={
    'index.html':40_000,
    'proyectos/real-zaragoza/goles-en-video.html':40_000,
    'proyectos/real-zaragoza/grupo-2.html':40_000,
    'proyectos/liga-f-xt/index.html':40_000,
    'proyectos/real-zaragoza/informe-completo.html':40_000,
    'proyectos/index.html':40_000,
    'proyectos/real-zaragoza/simulacion.html':40_000,
    'proyectos/futbol-femenino/index.html':40_000,
    'proyectos/real-zaragoza/previa-jornada-10.html':40_000,
    'proyectos/real-zaragoza/previa.html':40_000,
    'comparador/index.html':40_000,
    'galeria-visual/index.html':20_000,
}
PAGE_IMAGE_SIZES={
    'proyectos/index.html':'(max-width: 600px) 112px, 480px',
    'galeria-visual/index.html':'(max-width: 640px) calc(100vw - 32px), 360px',
    'index.html':{
        'proyectos/real-zaragoza/graficos/previa/real-zaragoza-villarreal-b-j10-v2.webp':'(max-width: 640px) calc(100vw - 32px), (max-width: 1200px) calc((100vw - 80px)/2), 560px',
        'proyectos/real-zaragoza/graficos/previa/noche-copa-tudela-20261027.webp':'(max-width: 640px) calc(100vw - 32px), (max-width: 1200px) calc((100vw - 80px)/2), 560px',
        'assets/ilustraciones/comparador-grupo2.webp':'(max-width: 760px) calc(100vw - 32px), 400px',
        'proyectos/liga-f-xt/graficos/foto.jpg':'(max-width: 416px) calc(100vw - 32px), 384px',
        'assets/fotos/seleccion-espanola-riazor-2024.jpg':'(max-width: 366px) calc(100vw - 32px), 334px',
        'assets/fvs-portada.jpg':'(max-width: 380px) 192px, 384px',
    },
    'proyectos/futbol-femenino/index.html':{
        'proyectos/futbol-femenino/mapa.png':'(max-width: 640px) calc(100vw - 32px), 1120px',
    },
}


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
    relative_page=page.resolve().relative_to(root.resolve()).as_posix()
    minimum_bytes=PAGE_IMAGE_MIN_BYTES.get(relative_page,RESPONSIVE_IMAGE_MIN_BYTES)
    def adapt(match):
        tag=match[0]; a=attrs(tag); src=a.get('src',''); url=urlsplit(src)
        if url.scheme or url.netloc or not url.path:return tag
        source=(root/unquote(url.path).lstrip('/')) if src.startswith('/') else page.parent/unquote(url.path)
        source=source.resolve()
        if not source.is_relative_to(root.resolve()) or not source.is_file() or source.suffix.lower() not in ('.png','.jpg','.jpeg','.webp'):return tag
        page_sizes=PAGE_IMAGE_SIZES.get(relative_page)
        sizes=page_sizes.get(source.relative_to(root).as_posix()) if isinstance(page_sizes,dict) else page_sizes
        with Image.open(source) as im:
            width,height=im.size
            add=''
            if not a.get('width'):add+=f' width="{width}"'
            if not a.get('height'):
                declared=int(a.get('width',width)) if str(a.get('width',width)).isdigit() else width
                add+=f' height="{round(height*declared/width)}"'
            if source.stat().st_size>minimum_bytes and width>800:
                digest=hashlib.sha256(source.read_bytes()).hexdigest()[:10]
                folder=root/'assets/adaptadas';folder.mkdir(exist_ok=True)
                existing=a.get('srcset','')
                existing_widths={int(item.strip().rsplit(' ',1)[1][:-1])
                                 for item in existing.split(',') if item.strip().rsplit(' ',1)[-1].endswith('w')
                                 and item.strip().rsplit(' ',1)[-1][:-1].isdigit()}
                def variant(size):
                    target=folder/f'{source.stem}-{digest}-{size}.webp'
                    if not target.exists():
                        copy=im.copy();copy.thumbnail((size,round(height*size/width)))
                        if source.suffix.lower()=='.png':
                            copy.save(target,'WEBP',lossless=True,method=6)
                        else:
                            copy.save(target,'WEBP',quality=82,method=6)
                    relative=os.path.relpath(target,page.parent).replace('\\','/')
                    return f'{relative} {size}w'
                if existing:
                    existing_parts=[item.strip() for item in existing.split(',') if item.strip()]
                    versions=[]
                    optimized_full=False
                    for item in existing_parts:
                        candidate=item.rsplit(' ',1)
                        if len(candidate)==2 and candidate[1]==f'{width}w' and candidate[0]==src:
                            versions.append(variant(width));optimized_full=True
                        elif len(candidate)==2 and candidate[1]==f'{width}w':
                            versions.append(item);optimized_full=True
                        else:
                            versions.append(item)
                    for size in (480,800,1200,1600):
                        if size<width and size not in existing_widths:
                            versions.append(variant(size))
                    if not optimized_full:
                        versions.append(variant(width))
                    new_srcset=escape(', '.join(versions),quote=True)
                    tag=re.sub(r'\bsrcset=("[^"]*"|\'[^\']*\')',lambda _:f'srcset="{new_srcset}"',tag,count=1)
                    if sizes:
                        if re.search(r'\bsizes=("[^"]*"|\'[^\']*\')',tag):
                            tag=re.sub(r'\bsizes=("[^"]*"|\'[^\']*\')',lambda _:f'sizes="{escape(sizes,quote=True)}"',tag,count=1)
                        else:
                            tag=tag[:-1]+' sizes="'+escape(sizes,quote=True)+'"'
                else:
                    versions=[variant(size) for size in (480,800,1200,1600) if size<width]
                    versions.append(variant(width))
                    sizes=sizes or '(max-width: 640px) calc(100vw - 48px), 800px'
                    add+=' srcset="'+escape(', '.join(versions),quote=True)+'" sizes="'+escape(sizes,quote=True)+'"'
            return tag[:-1]+add+'>'
    return re.sub(r'<img\b[^>]*>',adapt,raw)


def build(root=ROOT):
    changed=0
    for page in root.rglob('*.html'):
        if any(x in ('.git','analisis') for x in page.relative_to(root).parts):continue
        original=page.read_bytes()
        newline='\r\n' if b'\r\n' in original else '\n'
        raw=original.decode('utf-8')
        if newline=='\r\n':raw=raw.replace('\r\n','\n')
        if '</head>' not in raw or '<main' not in raw:continue
        new=imagenes(metadata(raw,root),page,root)
        if new!=raw:
            page.write_text(new,encoding='utf-8',newline=newline);changed+=1
    return changed


if __name__=='__main__':print('Páginas mejoradas:',build())
