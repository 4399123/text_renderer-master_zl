import os
import json
from glob import glob
from tqdm import tqdm
import shutil

inputpath=r'./eng_word_data'
outpath=r'./eng_word_data/renamefiles_eng_word_data'

if not os.path.exists(outpath):
    os.makedirs(outpath)

jsonpath=os.path.join(inputpath,'labels.json')
n=0
with open(jsonpath, 'r', encoding='utf8') as f:
    json_data = json.load(f)
    num_samples = int(json_data.get("num-samples"))
    img_lbls=dict(json_data.get("labels"))
    # print(num_samples)
    # print(img_lbls)
    dirname=os.path.join(inputpath,'images')
    for imgname in tqdm(img_lbls.keys()):
        imgpath=os.path.join(dirname,imgname+'.png')
        label=img_lbls[imgname]
        outname=os.path.join(outpath,str(label)+'_202406012{}.png'.format(n))
        n+=1
        shutil.copy(imgpath,outname)




