import os, hashlib, collections
from concurrent.futures import ProcessPoolExecutor
from PIL import Image
import sys
CL=["Tomato___healthy","Tomato___Bacterial_spot","Tomato___Early_blight","Tomato___Late_blight","Tomato___Leaf_Mold","Tomato___Septoria_leaf_spot","Tomato___Tomato_mosaic_virus","Tomato___Tomato_Yellow_Leaf_Curl_Virus","Potato___Early_blight","Potato___Late_blight"]
def info(p):
    try:
        with Image.open(p) as im: im.load(); s=im.size
    except Exception: s=None
    return p.split("/")[-2], s, hashlib.md5(open(p,"rb").read()).hexdigest()

def main():
    PV = sys.argv[1]  # path to PlantVillage-Dataset/raw/color
    paths=[f"{PV}/{c}/{f}" for c in CL for f in os.listdir(f"{PV}/{c}")]
    with ProcessPoolExecutor() as ex: r=list(ex.map(info,paths,chunksize=200))
    print("images",len(r),"unreadable",sum(s is None for _,s,_ in r),"sizes",collections.Counter(s for _,s,_ in r))
    g=collections.defaultdict(list)
    for c,_,m in r: g[m].append(c)
    d=[v for v in g.values() if len(v)>1]
    print("exact dup groups",len(d),"images in them",sum(len(v) for v in d),"conflicting",sum(len(set(v))>1 for v in d), collections.Counter(v[0] for v in d))
    cnt=collections.Counter(c for c,_,_ in r); print(cnt.most_common()); print("ratio",max(cnt.values())/min(cnt.values()))


if __name__ == "__main__":
    main()
