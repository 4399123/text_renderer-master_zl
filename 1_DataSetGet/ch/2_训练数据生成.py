import os
import random
from pathlib import Path
from tqdm import tqdm

# 支持的图像后缀
IMG_SUFFIXES = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}

for model in ('train', 'test'):

    inputpath = f'./rec/{model}'
    outputpath = r'./rec'
    outputtxtpath = f'rec/{model}/'

    # 用 pathlib 递归遍历，避免含中文路径时 imutils 读取失败
    imgpaths = [
        str(p) for p in Path(inputpath).rglob('*')
        if p.suffix.lower() in IMG_SUFFIXES
    ]
    random.shuffle(imgpaths)

    lines = []
    for imgpath in tqdm(imgpaths, desc=f'处理 {model}'):
        basename = os.path.basename(imgpath)
        parts = basename.split('_')
        if len(parts) == 1:
            continue
        name = parts[0]

        # 针对 ':' 的特殊处理（存储时用 @@@ 替代）
        if '@@@' in name:
            name = name.replace('@@@', ':')
            if '---' in name:
                name = name.replace('---', '/')
        # 针对 '/' 的特殊处理（存储时用 --- 替代）
        elif '---' in name:
            name = name.replace('---', '/')
            if '@@@' in name:
                name = name.replace('@@@', '：')

        f_outpath = os.path.join(outputtxtpath, basename)
        lines.append(f'{f_outpath}\t{name}')

    # 显式指定 UTF-8，确保中文标签正确写入
    out_file = os.path.join(outputpath, f'rec_gt_{model}.txt')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'[{model}] 共处理 {len(lines)} 条，已写入 {out_file}')
