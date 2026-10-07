import os
import requests
from PIL import Image, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
RAW_DIR = os.path.join(ASSETS_DIR, 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

IMAGES = {
    "census_clerks.jpg": "https://upload.wikimedia.org/wikipedia/commons/1/17/Clerks_working_a_census_tabulator_LCCN2012645285.jpg",
    "vasa_ship.jpg": "https://upload.wikimedia.org/wikipedia/commons/1/15/The_Vasa_from_the_Bow.jpg",
    "aberdeen_computers.jpg": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Two_women_operating_ENIAC_%28full_resolution%29.jpg"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def download_and_process():
    for name, url in IMAGES.items():
        raw_path = os.path.join(RAW_DIR, name)
        print(f"Fetching {name}...")
        r = requests.get(url, headers=headers, timeout=25)
        if r.status_code == 200:
            with open(raw_path, 'wb') as f:
                f.write(r.content)
        else:
            raise RuntimeError(f"Failed to download {name}: status {r.status_code}")
        
        # Process with Pillow: 8px solid white border + drop shadow
        with Image.open(raw_path) as im:
            im = im.convert("RGBA")
            im.thumbnail((800, 600), Image.Resampling.LANCZOS)
            w, h = im.size
            border = 8
            
            # White bordered image
            bw, bh = w + border * 2, h + border * 2
            bordered = Image.new("RGBA", (bw, bh), (255, 255, 255, 255))
            bordered.paste(im, (border, border))
            
            # Canvas with soft drop shadow (rgba(0, 0, 0, 0.12) -> alpha ~ 31)
            pad = 12
            cw, ch = bw + pad * 2, bh + pad * 2
            canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
            
            shadow = Image.new("RGBA", (bw, bh), (0, 0, 0, 31))
            canvas.paste(shadow, (pad + 2, pad + 4))
            canvas = canvas.filter(ImageFilter.GaussianBlur(radius=4))
            
            # Paste bordered image on top
            canvas.paste(bordered, (pad, pad), bordered)
            
            out_name = f"cutout_{os.path.splitext(name)[0]}.png"
            out_path = os.path.join(ASSETS_DIR, out_name)
            canvas.save(out_path, "PNG")
            print(f"Saved cutout: {out_path} ({cw}x{ch})")

if __name__ == '__main__':
    download_and_process()
    print("All assets prepared successfully!")
