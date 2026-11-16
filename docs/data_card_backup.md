# Data card - Tomato leaf diseases (backup dataset)

| Field | Value |
|---|---|
| Name | Tomato leaf diseases (Mendeley Data, version 1) |
| Link | https://data.mendeley.com/datasets/93h9p62kg4/1 (DOI 10.17632/93h9p62kg4.1) |
| License | CC BY 4.0; course use is allowed with attribution |
| Size | The version 1 archive holds 2,627 JPEG files in 10 labelled folders, and all of them open. The dataset page lists 2,659 images, including 32 uncategorized images that are not in the archive |
| Target | The class, given by the folder name |
| Role in LeafShift | Fallback field test set if PlantDoc proves unusable |

## Folders

| Folder | Images | Matches our class |
|---|---:|---|
| Bacterial Spot | 376 | Tomato bacterial spot |
| Early Blight | 204 | Tomato early blight |
| Healthy | 103 | Tomato healthy |
| Late Blight | 166 | Tomato late blight |
| Leaf Mold | 66 | Tomato leaf mold |
| Tomato Leaf Curl Virus | 394 | Not used: the label does not establish that it is the same virus as tomato yellow leaf curl virus |
| Cercospora leaf mold | 156 | No |
| Insect Damage | 336 | No |
| Leaf Miner | 519 | No |
| Spider Mites | 307 | No |

The five matching classes hold 915 images. There is no Septoria leaf spot, mosaic virus or potato class. Per-folder counts are in `backup_dataset_counts.csv`.

## Why it is a viable fallback

The photos were taken in the field with a smartphone, separately from PlantVillage, and the licence allows course use. If PlantDoc is judged unusable, the field evaluation would shrink to these five tomato classes.
