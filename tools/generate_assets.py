"""Generate Bitcrest's repository-local profile graphics. Requires Pillow."""
from pathlib import Path
import math
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
W = 1200
BG = (10, 17, 27)
FG = (233, 243, 246)
MUTED = (134, 155, 173)
MINT = (104, 239, 198)
BLUE = (108, 155, 251)


def font(size, kind='regular'):
    names = {'regular': 'DejaVuSans.ttf', 'bold': 'DejaVuSans-Bold.ttf', 'mono': 'DejaVuSansMono.ttf'}
    windows = {'regular': 'arial.ttf', 'bold': 'arialbd.ttf', 'mono': 'consola.ttf'}
    candidates = [Path(os.environ.get('BITCREST_FONT_DIR', '/usr/share/fonts/truetype/dejavu')) / names[kind],
                  Path('C:/Windows/Fonts') / windows[kind]]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    raise FileNotFoundError('Set BITCREST_FONT_DIR to a directory containing DejaVu Sans fonts.')


def base(height):
    im = Image.new('RGB', (W, height), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((1, 1, W-2, height-2), radius=20, outline=(36, 52, 66), width=2)
    return im


def save_loop(frames, name, duration):
    # One shared palette prevents text and background colors from flickering.
    sample = Image.new('RGB', (W, frames[0].height * 3))
    for i, idx in enumerate([0, len(frames)//2, len(frames)-1]):
        sample.paste(frames[idx], (0, i*frames[0].height))
    pal = sample.quantize(colors=128)
    indexed = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(OUT / f'{name}.gif', save_all=True, append_images=indexed[1:],
                    duration=duration, loop=0, optimize=True, disposal=1)


def banner():
    frames = []
    n = 72
    for frame in range(n):
        t = frame / n
        im = base(380)
        d = ImageDraw.Draw(im)
        # Quiet grid beneath the animated network crest.
        for x in range(738, 1172, 28):
            for y in range(30, 353, 28):
                d.ellipse((x, y, x+1, y+1), fill=(36, 52, 66))
        d.text((44, 34), 'B / C', font=font(20, 'mono'), fill=MINT)
        d.text((44, 102), 'BITCREST', font=font(76, 'bold'), fill=FG)
        d.text((48, 206), 'ENGINEERING MEETS IMAGINATION', font=font(18, 'mono'), fill=MINT)
        d.text((48, 248), 'Full-stack developer & creative technologist', font=font(21), fill=MUTED)
        d.line((48, 305, 690, 305), fill=(38, 56, 69))
        d.text((48, 328), 'CODE  /  SECURITY  /  MOTION', font=font(15, 'mono'), fill=MUTED)
        cx, cy = 954, 190
        points = []
        for ring, radius in enumerate([66, 131]):
            for i in range(6):
                a = math.pi/3*i-math.pi/2 + ring*0.20
                points.append((cx+math.cos(a)*radius, cy+math.sin(a)*radius))
        edges = []
        for i in range(6):
            edges.extend([(i,(i+1)%6), (6+i,6+(i+1)%6), (i,6+i), (i,6+(i+1)%6)])
        for j, (a,b) in enumerate(edges):
            pa,pb = points[a],points[b]
            d.line((pa,pb), fill=(40, 87, 92) if j%3 else (52, 64, 105), width=1)
            s = (t + j/len(edges)) % 1
            x,y = pa[0]+(pb[0]-pa[0])*s, pa[1]+(pb[1]-pa[1])*s
            d.ellipse((x-2,y-2,x+2,y+2), fill=MINT if j%3 else BLUE)
        for i,(x,y) in enumerate(points):
            strength = (math.sin(2*math.pi*t+i)+1)/2
            color = tuple(int(v*(0.55+0.45*strength)) for v in MINT)
            d.ellipse((x-4,y-4,x+4,y+4), fill=color)
        d.rounded_rectangle((919,154,989,226), radius=15, fill=(14,31,39), outline=MINT, width=2)
        d.text((938,166), 'B', font=font(35,'bold'), fill=FG)
        frames.append(im)
    frames[0].save(OUT/'bitcrest-banner.png')
    save_loop(frames,'bitcrest-banner',80)


def workbench():
    lines = [('$ cat focus.txt', FG),
             ('security  > MeshTrace AI', MINT),
             ('platforms > ZellZap / NexusFlow', BLUE),
             ('creative  > Blender / motion design / AI workflows', MUTED)]
    frames = []
    for f in range(116):
        im = base(250)
        d = ImageDraw.Draw(im)
        for x, color in [(28,(238,121,120)), (50,(232,190,94)), (72,MINT)]:
            d.ellipse((x,20,x+10,30),fill=color)
        d.text((106,15),'bitcrest / workbench',font=font(14,'mono'),fill=MUTED)
        d.text((924,15),'BUILD. LEARN. REFINE.',font=font(12,'mono'),fill=MUTED)
        d.line((20,46,1180,46),fill=(36,52,66))
        for i,(line,color) in enumerate(lines):
            count = max(0, min(len(line), (f-i*16)*2))
            y = 68+i*39
            d.text((30,y),line[:count],font=font(20,'mono'),fill=color)
            if (0 < count < len(line)) or (i==3 and count==len(line) and f%14<7):
                x = 30+d.textlength(line[:count],font=font(20,'mono'))+4
                d.rectangle((x,y+3,x+10,y+23),fill=MINT)
        frames.append(im)
    frames[95].save(OUT/'workbench.png')
    durations = [70]*len(frames)
    durations[-1] = 1300
    save_loop(frames,'workbench',durations)


if __name__ == '__main__':
    banner()
    workbench()
    print('Generated 2 animated GIFs and 2 static alternatives in assets/.')
