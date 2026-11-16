import os, numpy as np, collections
from concurrent.futures import ProcessPoolExecutor
from PIL import Image; import imagehash
import sys
CL=["Tomato___healthy","Tomato___Bacterial_spot","Tomato___Early_blight","Tomato___Late_blight","Tomato___Leaf_Mold","Tomato___Septoria_leaf_spot","Tomato___Tomato_mosaic_virus","Tomato___Tomato_Yellow_Leaf_Curl_Virus","Potato___Early_blight","Potato___Late_blight"]
def h(p):
    return int(str(imagehash.phash(Image.open(p).convert("RGB"))),16)

def main():
    PV = sys.argv[1]  # path to PlantVillage-Dataset/raw/color
    paths=[f"{PV}/{c}/{f}" for c in CL for f in sorted(os.listdir(f"{PV}/{c}"))]
    with ProcessPoolExecutor() as ex: H=np.array(list(ex.map(h,paths,chunksize=200)),dtype=np.uint64)
    lab=np.array([p.split("/")[-2] for p in paths])
    tbl=np.array([bin(i).count("1") for i in range(256)],dtype=np.uint8)
    def pop(x):
        b=x.view(np.uint8).reshape(*x.shape,8); return tbl[b].sum(-1)
    res=collections.Counter(); pairs=[]
    for i in range(0,len(H),500):
        d=pop(H[i:i+500,None]^H[None,:])
        for a,b in zip(*np.nonzero(d<=4)):
            a+=i
            if a<b: pairs.append((a,b,int(d[a-i,b])))
    print("pairs dist<=4:",len(pairs))
    for k in (0,2,4):
        s=[p for p in pairs if p[2]<=k]; print(f" dist<={k}: {len(s)} pairs, cross-class {sum(lab[a]!=lab[b] for a,b,_ in s)}")
    print(collections.Counter(lab[a] for a,b,_ in pairs).most_common())
    import random; random.seed(0)
    sm=[p for p in pairs if p[2]>0]; print("examples dist>0:",[(paths[a].split('/')[-1][-25:],paths[b].split('/')[-1][-25:],d) for a,b,d in sm[:6]])
    open("pv_nearpairs.txt","w").write("\n".join(f"{paths[a]}\t{paths[b]}\t{d}" for a,b,d in pairs))


if __name__ == "__main__":
    main()
