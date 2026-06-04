import os
from pathlib import Path
from tqdm import tqdm

# 图像目录
path = r'./rec/'

# 支持的图像后缀
IMG_SUFFIXES = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.webp'}

# 用 pathlib 递归遍历，避免含中文路径时 imutils 读取失败
imgpaths = [
    str(p) for p in Path(path).rglob('*')
    if p.suffix.lower() in IMG_SUFFIXES
]

# 载入词典，显式指定 UTF-8 编码，兼容中文字符
dict_path = r'./ppocr_keys_v1.txt'
with open(dict_path, 'r', encoding='utf-8') as f:
    valid_chars = {line.strip() for line in f if line.strip()}

flag = 0
for imgpath in tqdm(imgpaths, desc='验证中'):
    basename = os.path.basename(imgpath)
    parts = basename.split('_')

    # 文件名格式不符合 label_xxx 规范，报错
    if len(parts) != 2:
        print(f'{basename} ----------> Error!!!! 文件名格式异常')
        flag = 1
        continue

    label = parts[0]
    for ch in label:
        if ch not in valid_chars:
            print(f'{basename} ----------> Error!!!! 字符 [{ch}] 不在词典中')
            flag = 1
            break

if flag == 0:
    print('符号没问题！！！！')
