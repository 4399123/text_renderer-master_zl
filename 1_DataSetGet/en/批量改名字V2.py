import os
from imutils import paths
from tqdm import tqdm
import shutil

path=r'./o_imgs'
out_path=r'./imgs'
name='0050011000100B5126244324M071'
today='20240522'

if not os.path.exists(out_path):
    os.makedirs(out_path)

imgpaths=list(paths.list_images(path))
n=80
for imgpath in tqdm(imgpaths):
    outpath=os.path.join(out_path,name+'_'+today+'{}'.format(n)+'.png')
    shutil.move(imgpath,outpath)
    n+=1
