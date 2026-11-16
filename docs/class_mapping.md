# LeafShift class mapping and post-cleaning counts

| Shared class | PlantVillage folder | PlantDoc folder | PlantVillage raw | PlantVillage retained | PlantDoc raw | PlantDoc retained |
|---|---|---|---:|---:|---:|---:|
| Tomato healthy | `Tomato___healthy` | `Tomato leaf` | 1,591 | 1,585 | 63 | 63 |
| Tomato bacterial spot | `Tomato___Bacterial_spot` | `Tomato leaf bacterial spot` | 2,127 | 2,127 | 110 | 105 |
| Tomato early blight | `Tomato___Early_blight` | `Tomato Early blight leaf` | 1,000 | 1,000 | 88 | 76 |
| Tomato late blight | `Tomato___Late_blight` | `Tomato leaf late blight` | 1,909 | 1,901 | 111 | 100 |
| Tomato leaf mold | `Tomato___Leaf_Mold` | `Tomato mold leaf` | 952 | 952 | 91 | 90 |
| Tomato Septoria leaf spot | `Tomato___Septoria_leaf_spot` | `Tomato Septoria leaf spot` | 1,771 | 1,771 | 151 | 139 |
| Tomato mosaic virus | `Tomato___Tomato_mosaic_virus` | `Tomato leaf mosaic virus` | 373 | 373 | 54 | 53 |
| Tomato yellow leaf curl virus | `Tomato___Tomato_Yellow_Leaf_Curl_Virus` | `Tomato leaf yellow virus` | 5,357 | 5,357 | 76 | 72 |
| Potato early blight | `Potato___Early_blight` | `Potato leaf early blight` | 1,000 | 1,000 | 117 | 102 |
| Potato late blight | `Potato___Late_blight` | `Potato leaf late blight` | 1,000 | 1,000 | 105 | 93 |
| **Total** | | | **17,080** | **17,066** | **966** | **893** |

PlantVillage counts exclude 14 extra copies of byte-identical images. Grouping affects future splits and does not remove additional images from the table.
PlantDoc counts pool the original train and test folders for the external dataset. We excluded 73 files after reviewing 8 byte-identical groups and 49 perceptual-hash pairs; the 49 pairs included all 8 byte-identical pairs. Visual review identified 45 groups of repeated source photos. All copies were excluded from the 26 groups with conflicting labels. For the 19 same-label groups, the highest-resolution copy was retained, preferring the official test copy on ties.

The cleaned PlantDoc manifest retains 893 images, 77 of them from the original test folder. Original labels were kept for all retained photos; the duplicate review does not confirm their diagnoses.

**Next step (not yet applied).** While inspecting the retained images we found 25 that appear not to be plant photographs: presentation slides, title cards, covers with title text, one labelled figure grid and one drawing. They are listed in `plantdoc_nonphoto_candidates.csv`, are still included in the counts above, and will be reviewed and excluded in the next cleaning step. A label review (possible wrong crop, several diseases in one image, for example `train/Tomato leaf/Fig-2.jpg`) follows after that.

## Files and how to apply them

| File | Use |
|---|---|
| `class_mapping.csv` | Exact folder mapping, pre- and post-cleaning counts, and PlantVillage group coverage by class. |
| `plantdoc_clean_manifest.csv` | The retained PlantDoc images and their source labels. Use `windows_path` for the numbered extraction from `fix_plantdoc.py` and `original_path` for the upstream Linux checkout. Paths are relative to `data/PlantDoc-Dataset`. |
| `plantdoc_cleaning_log.csv` | One row per reviewed image with the decision, reason, and reviewer. The source dataset is kept intact and the manifest controls inclusion. |
| `plantdoc_nonphoto_candidates.csv` | 25 retained images that appear not to be plant photographs, proposed for exclusion in the next cleaning step. |
| `plantdoc_duplicate_pairs.csv` | The 49 candidate pairs, distances, and visual decisions. The same group ID can appear in several pairs. |
| `plantvillage_duplicate_review.csv` | All 61 candidate pairs and review results. The one cross-class hit was visually distinct. |
| `plantvillage_leaf_groups.csv` | One row per PlantVillage image relative to `raw/color`. Filter to `action=retain` and use `split_group_id` to keep all related rows together when making splits. |
| `week7_section4_status.md` | Wording to paste into Section 4 of the handout. |

## PlantVillage grouping and remaining limitation

Published maps identify 11,735 rows directly. One additional image matched a published map entry after removing a conflicted-copy suffix. Another 1,038 images have greenhouse leaf-series IDs inferred from their filenames. The greenhouse rule groups angle suffixes and repeated observation days with the same base leaf number. The longer GHLB2 camera sequence is kept with its greenhouse series because overlap with numbered leaves cannot be ruled out. Visually confirmed and uncertain same-leaf candidates were also joined into the same split group.

The remaining 4,306 images have no verified individual leaf ID. Of those, 4,304 have a capture-series prefix and two have unresolved provenance. The manifest assigns conservative split groups to them and leaves `leaf_id` blank. For the two unresolved files, a shared placeholder group preserves their unresolved status. The grouping cannot establish whether they overlap with other groups.

All 373 PlantVillage tomato mosaic virus images belong to one capture series. Keeping it intact prevents placing that class in both the training and test sets. A 10-class split with every class on both sides needs verified mosaic leaf IDs or an instructor-approved change to the split. No train/test split is included.

## Source revisions

- PlantVillage color images: https://github.com/spMohanty/PlantVillage-Dataset/tree/7f7ecc7e1eaca78107e3affe7cb5abd9427e139a
- PlantDoc: https://github.com/pratikkayal/PlantDoc-Dataset/tree/5467f6012d78d1c446145d5f582da6096f852ae8
- Published PlantVillage leaf maps: https://github.com/salathegroup/plantvillage_deeplearning_paper_dataset/tree/97664b03183427f3190489764e5f1c2929cd25ac/leaf_grouping/filtered_leafmaps

## Backup dataset verification

The version 1 download of [Tomato leaf diseases](https://data.mendeley.com/datasets/93h9p62kg4/1)
contains 2,627 JPEG files in 10 folders. All decoded successfully. The publisher's
description also lists 32 uncategorized images that are absent from the downloaded
archive. `backup_dataset_counts.csv` records the verified per-folder counts.
The five matching classes total 915 images. The 394 images labelled Tomato Leaf
Curl Virus are outside the fallback because the label does not establish a match
with Tomato Yellow Leaf Curl Virus.

Version 1 archive SHA-256
`9d45c4063f796ce85afe312028c40ea9f2f5efc5f14fd33c52d5bbaee430c2cf`
