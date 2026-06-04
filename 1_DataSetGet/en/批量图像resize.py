from imutils import paths
import os
import cv2
from tqdm import  tqdm


inpath=r'./imgs'
outpath=r'./out'

if not os.path.exists(outpath):
    os.makedirs(outpath)

imgpaths=list(paths.list_images(inpath))

for impath in tqdm(imgpaths):
    basename=os.path.basename(impath)
    name=basename.split('.')[0]
    img=cv2.imread(impath)
    img=cv2.resize(img,(320,48))
    outfilename=os.path.join(outpath,name+'resize.png')
    cv2.imwrite(outfilename,img)