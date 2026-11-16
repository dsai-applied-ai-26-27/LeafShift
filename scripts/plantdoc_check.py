"""Audit PlantDoc shared tomato/potato classes: counts, readability, sizes, duplicates."""
import hashlib, os, sys, collections
from PIL import Image
import imagehash

ROOT = sys.argv[1]  # path to a clone of PlantDoc-Dataset
SHARED = ["Tomato leaf", "Tomato leaf bacterial spot", "Tomato Early blight leaf", "Tomato leaf late blight",
          "Tomato mold leaf", "Tomato Septoria leaf spot", "Tomato leaf mosaic virus", "Tomato leaf yellow virus",
          "Potato leaf early blight", "Potato leaf late blight"]

rows, bad, md5s, phashes = [], [], collections.defaultdict(list), []
counts = collections.Counter()
for split in ("train", "test"):
    for cls in sorted(os.listdir(f"{ROOT}/{split}")):
        for f in os.listdir(f"{ROOT}/{split}/{cls}"):
            p = f"{ROOT}/{split}/{cls}/{f}"
            counts[(split, cls)] += 1
            if cls not in SHARED:
                continue
            try:
                with Image.open(p) as im:
                    im.load()
                    w, h = im.size
                    ph = imagehash.phash(im.convert("RGB"))
            except Exception as e:
                bad.append((p, repr(e)[:60]))
                continue
            md5s[hashlib.md5(open(p, "rb").read()).hexdigest()].append((split, cls, f))
            phashes.append((ph, split, cls, f))
            rows.append((split, cls, w, h))

print("all classes in repo:", len({c for _, c in counts}), "| total files:", sum(counts.values()))
tot = sum(counts[(s, c)] for s in ("train", "test") for c in SHARED)
tst = sum(counts[("test", c)] for c in SHARED)
print("shared-class files:", tot, "| shared test files:", tst,
      "| per-class test min/max:", min(counts[("test", c)] for c in SHARED), max(counts[("test", c)] for c in SHARED))
print("unreadable:", len(bad), bad[:5])
ws = sorted(r[2] for r in rows); hs = sorted(r[3] for r in rows)
med = lambda a: a[len(a) // 2]
print(f"width min/median/max {ws[0]}/{med(ws)}/{ws[-1]} | height min/median/max {hs[0]}/{med(hs)}/{hs[-1]}")
print("images smaller than 224 on either side:", sum(1 for r in rows if min(r[2], r[3]) < 224))

dups = [v for v in md5s.values() if len(v) > 1]
print("exact-duplicate groups:", len(dups), "| conflicting labels:",
      sum(1 for v in dups if len({c for _, c, _ in v}) > 1), "| crossing train/test:",
      sum(1 for v in dups if len({s for s, _, _ in v}) > 1))
for v in dups:
    print("   ", v)

near = []
for i in range(len(phashes)):
    for j in range(i + 1, len(phashes)):
        if phashes[i][0] - phashes[j][0] <= 4:
            near.append((phashes[i][1:], phashes[j][1:]))
print("near-duplicate pairs (pHash dist<=4):", len(near),
      "| with different labels:", sum(1 for a, b in near if a[1] != b[1]),
      "| crossing train/test:", sum(1 for a, b in near if a[0] != b[0]))
for a, b in near:
    print("   ", a, "<->", b)
