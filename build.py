import os
import fontforge
import time
from concurrent.futures import ProcessPoolExecutor

SRC = "simsun.ttf"
OUT_DIR = "dist"
BASE_FAMILY = "SimSunDerived"

WEIGHTS = [
    ("Regular", 400, 0),
    ("Medium", 500, 8),
    ("SemiBold", 600, 14),
    ("Bold", 700, 22),
]

def build_one(args):
    style, weight_num, embolden = args
    print(f"[{style}] 正在加载字体...")
    font = fontforge.open(SRC)

    if embolden > 0:
        print(f"[{style}] 正在加粗 ({embolden})...")
        font.selection.all()
        font.correctDirection()
        font.changeWeight(embolden, "LCG", 0, 0, "auto")
        
        print(f"[{style}] 正在去除路径重叠 (最耗时)...")
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
    print(f"[{style}] 正在导出...")
    font.generate(out_path)
    font.close()
    print(f"[{style}] ✅ 生成完毕: {out_path}")

def main():
    if not os.path.exists(SRC):
        raise FileNotFoundError(f"当前目录下没有 {SRC}")
    os.makedirs(OUT_DIR, exist_ok=True)
    
    start_time = time.time()
    print("开始并行构建字体...")
    with ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(build_one, WEIGHTS)
        
    end_time = time.time()
    print(f"🎉 全部任务完成！总耗时: {end_time - start_time:.2f} 秒")

if __name__ == "__main__":
    main()