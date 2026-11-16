import csv, os, collections, sys
PV = sys.argv[1]  # path to PlantVillage-Dataset/raw/color
CL = ["Tomato___healthy","Tomato___Bacterial_spot","Tomato___Early_blight","Tomato___Late_blight","Tomato___Leaf_Mold",
      "Tomato___Septoria_leaf_spot","Tomato___Tomato_mosaic_virus","Tomato___Tomato_Yellow_Leaf_Curl_Virus",
      "Potato___Early_blight","Potato___Late_blight"]
tot = cov = 0
for c in CL:
    files = os.listdir(f"{PV}/{c}")
    m = {}
    p = f"{sys.argv[2]}/{c}.csv"
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding="utf-8", errors="replace")):
            m[".".join(r["File Name"].split(".")[:-1]).lower().strip()] = r["Leaf #"]
    ids = [m.get(".".join(f.split("___", 1)[-1].split(".")[:-1]).lower().strip()) for f in files]
    hit = [i for i in ids if i]
    leaves = collections.Counter(hit)
    tot += len(files); cov += len(hit)
    mx = max(leaves.values()) if leaves else 0
    print(f"{c:42s} imgs={len(files):5d} mapped={len(hit):5d} leaves={len(leaves):5d} "
          f"imgs/leaf={len(hit)/max(len(leaves),1):.2f} max={mx}")
print("total", tot, "mapped", cov, f"{cov/tot:.1%}")
