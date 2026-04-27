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
    if embolden > 0:
        try:
            font.changeWeight(embolden)
        except AttributeError:
            font.changeWeight(embolden)

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

def main():
    if not os.path.exists(SRC):
        raise FileNotFoundError("当前目录下没有 simsun.ttf")

    os.makedirs(OUT_DIR, exist_ok=True)

    for style, weight_num, embolden in WEIGHTS:
        build_one(style, weight_num, embolden)

if __name__ == "__main__":
    main()