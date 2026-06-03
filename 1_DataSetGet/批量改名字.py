import os
from imutils import paths
from tqdm import tqdm

path=r'./imgs'
name='C0-00009'
today='20240410'
imgpaths=list(paths.list_images(path))
n=0
for imgpath in tqdm(imgpaths):
    dirname=os.path.dirname(imgpath)
    outpath=os.path.join(dirname,name+'_'+today+'{}'.format(n)+'.png')
    os.rename(imgpath,outpath)
    n+=1
