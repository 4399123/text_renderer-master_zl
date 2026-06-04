import numpy as np
import os
from imutils import paths
import random
from tqdm import  tqdm


for model in ('train', 'test'):

    inputpath = f'./rec/{model}'
    outputpath = r'./rec'

    outputtxtpath = f'rec/{model}/'

    imgpaths = list(paths.list_images(inputpath))
    random.shuffle(imgpaths)

    lines = []
    for imgpath in tqdm(imgpaths):
        basename = os.path.basename(imgpath)
        name = basename.split('_')
        if (len(name) == 1): continue
        name = name[0]

        if ('@@@' in name):                   #针对':'进行特殊处理
            name = name.replace('@@@', ':')
            if ('---' in name):
                name = name.replace('---', '/')
        if ('---' in name):                   #针对'/'进行特殊处理
            name = name.replace('---', '/')
            if ('@@@' in name):
                name = name.replace('@@@', '：')

        f_outpath = os.path.join(outputtxtpath, basename)

        line = '{}\t{}'.format(f_outpath, str(name))

        lines.append(line)

    with open(os.path.join(outputpath, f'rec_gt_{model}.txt'), 'w') as f:
        f.write('\n'.join(lines))

