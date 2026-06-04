from imutils import paths
import os
from tqdm import  tqdm
import shutil
import random


n=250
inpath='./out'
outpath_train='./rec/train'
outpath_val='./rec/test'

if not os.path.exists(outpath_train):
    os.makedirs(outpath_train)

if not os.path.exists(outpath_val):
    os.makedirs(outpath_val)

impaths=list(paths.list_images(inpath))
total_num=len(impaths)
random.shuffle(impaths)

for i in tqdm(range(n)):
    impath=impaths[i]
    basename=os.path.basename(impath)
    outpathval=os.path.join(outpath_val,basename)
    shutil.copy(impath,outpathval)

for i in tqdm(range(n,total_num)):
    impath = impaths[i]
    basename = os.path.basename(impath)
    outpathtrain = os.path.join(outpath_train, basename)
    shutil.copy(impath, outpathtrain)
