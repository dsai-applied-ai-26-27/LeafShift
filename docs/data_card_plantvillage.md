# Data card - PlantVillage (primary dataset)

| Field | Value |
|---|---|
| Name | PlantVillage, colour images (`raw/color`); we use 10 tomato and potato classes |
| Link | https://github.com/spMohanty/PlantVillage-Dataset (original release), audited at commit `7f7ecc7e1eaca78107e3affe7cb5abd9427e139a` |
| Creator and purpose | David P. Hughes and Marcel Salathé (PlantVillage). An open-access set of expert-curated images of healthy and infected leaves, released to enable the development of mobile disease diagnostics. Dataset paper: https://arxiv.org/abs/1511.08060. Benchmark paper: Mohanty, Hughes & Salathé (2016), https://doi.org/10.3389/fpls.2016.01419 |
| Size | Colour folder: 54,305 images in 38 classes (the paper reports 54,306). Our 10 classes: 17,080 images, all 256x256 px; 17,066 after cleaning |
| Target | The class (crop and disease, or healthy), given by the folder name |
| License | CC BY-SA 3.0, declared in the repository's `README_HF.md` (the dataset card of the official Hugging Face mirror `mohanty/PlantVillage`). The repository itself has no LICENSE file. Course use is allowed with attribution. ShareAlike applies to any image set we derive and publish. We do not store images in our repository |
| Role in LeafShift | Training data and in-domain test set |

## Our 10 classes

| Class | Folder | Images | After cleaning |
|---|---|---:|---:|
| Tomato healthy | `Tomato___healthy` | 1,591 | 1,585 |
| Tomato bacterial spot | `Tomato___Bacterial_spot` | 2,127 | 2,127 |
| Tomato early blight | `Tomato___Early_blight` | 1,000 | 1,000 |
| Tomato late blight | `Tomato___Late_blight` | 1,909 | 1,901 |
| Tomato leaf mold | `Tomato___Leaf_Mold` | 952 | 952 |
| Tomato Septoria leaf spot | `Tomato___Septoria_leaf_spot` | 1,771 | 1,771 |
| Tomato mosaic virus | `Tomato___Tomato_mosaic_virus` | 373 | 373 |
| Tomato yellow leaf curl virus | `Tomato___Tomato_Yellow_Leaf_Curl_Virus` | 5,357 | 5,357 |
| Potato early blight | `Potato___Early_blight` | 1,000 | 1,000 |
| Potato late blight | `Potato___Late_blight` | 1,000 | 1,000 |
| **Total** | | **17,080** | **17,066** |

Potato healthy (152 images) is not used, because PlantDoc has no healthy potato class.

## Quality issues

- **Missing or unreadable files:** none; all 17,080 files open.
- **Imbalance:** 5,357 images (tomato yellow leaf curl virus) vs. 373 (tomato mosaic virus), about 14.4x.
- **Duplicates:** 14 pairs of byte-identical files (8 in tomato late blight, 6 in tomato healthy), none with conflicting labels. One copy of each is excluded. Perceptual hashing found 61 pairs in total; the 47 non-identical pairs were reviewed by eye (`plantvillage_duplicate_review.csv`).
- **Same leaf in several images:** the published leaf maps assign 11,735 of our images to 2,935 leaves, so a random split would leak. `plantvillage_leaf_groups.csv` gives every image a split group. Tomato mosaic virus has no leaf map, and its 373 images form one capture group.
- **Bias:** uniform lab backgrounds and capture conditions per class (Noyan, 2022).
- **Labels:** assigned by the dataset creators; not independently checked by us.

## Sensitive content

Photos of single leaves; no personal, confidential or restricted data.

## Why it fits

It contains all 10 of our classes, with 373 to 5,357 images each, which is enough to train a CNN. It is also the lab dataset whose transfer to field photos our project measures (Mohanty et al., 2016).
