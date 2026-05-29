import os
import json
from datetime import datetime
from glob import glob
from tqdm import tqdm
import shutil

inputpath=r'./rand_data'
outpath=r'./rand_data/renamefiles_rand_data'

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
    current_date = datetime.now().strftime("%Y%m%d")  # 获取当前日期，格式：20260529
    for imgname in tqdm(img_lbls.keys()):
        imgpath=os.path.join(dirname,imgname+'.png')
        label=img_lbls[imgname]
        outname=os.path.join(outpath,str(label)+'_{}{}.png'.format(current_date, n))
        n+=1
        shutil.copy(imgpath,outname)




