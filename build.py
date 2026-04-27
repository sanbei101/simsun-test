import os
import fontforge

SRC = "simsun.ttf"
OUT_DIR = "dist"
BASE_FAMILY = "SimSunDerived"

WEIGHTS = [
    ("Regular", 400, 0),
    ("Medium", 500, 8),
    ("SemiBold", 600, 14),
    ("Bold", 700, 22),
]

def build_one(style, weight_num, embolden):
    font = fontforge.open(SRC)

    font.selection.all()
    
    font.removeOverlap()
    font.correctDirection()

    if embolden > 0:
        font.selection.all()
        font.changeWeight(embolden)

    font.selection.all()
    font.removeOverlap()

    font.familyname = BASE_FAMILY
    font.fontname = f"{BASE_FAMILY.replace(' ', '')}-{style}"
    font.fullname = f"{BASE_FAMILY} {style}"
    font.weight = style
    try:
        font.os2_weight = weight_num
    except:
        pass

    out_path = os.path.join(OUT_DIR, f"{BASE_FAMILY.replace(' ', '')}-{style}.ttf")
    font.generate(out_path)
    font.close()
    print(f"Generated: {out_path}")

def main():
    if not os.path.exists(SRC):
        raise FileNotFoundError(f"当前目录下没有 {SRC}")
    os.makedirs(OUT_DIR, exist_ok=True)
    for style, weight_num, embolden in WEIGHTS:
        print(f"Building {style}...")
        build_one(style, weight_num, embolden)

if __name__ == "__main__":
    main()