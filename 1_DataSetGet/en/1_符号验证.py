import  numpy
import os
from imutils import paths
from tqdm import tqdm


path=r'./rec/test'
# path=r'imgs'

imgpaths=list(paths.list_images(path))


#载入词典
dict_path = r'./en_dict.txt'
new_lines = []
with open(dict_path, 'r') as f:
    lines = f.readlines()
    for line in lines:
        line1 = line.strip()
        new_lines.append(line1)

flag=0
for imgpath in imgpaths:
    basename = os.path.basename(imgpath)

    name=basename.split('_')

    if(len(name)==1):
        print(imgpath)
        continue
    name = name[0]
    for aphs in name:
        if(aphs not in new_lines):
            print('{} ---------->Error!!!!'.format(basename))
            flag=1
            break

if(flag==0):print('符号没问题！！！！')