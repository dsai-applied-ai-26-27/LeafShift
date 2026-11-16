# Section 4: Required change from Week 3

## Required change

Commit the final class-mapping table between PlantVillage and PlantDoc for your 10 classes, with the number of images per class after cleaning, and report the result of a duplicate check on PlantVillage.

## Status

**Done.** The table in `docs/class_mapping.md` (machine-readable: `docs/class_mapping.csv`) gives the folder names in both datasets and the counts per class before and after cleaning. After cleaning we keep 17,066 of 17,080 PlantVillage images and 893 of 966 PlantDoc images.

**PlantVillage duplicate check.**

- Byte-identical files: 14 pairs (8 in tomato late blight, 6 in tomato healthy), all with matching labels. One copy of each pair is excluded.
- Perceptual hash (distance 4 or less): 61 pairs, including the 14 identical pairs. All 47 other pairs were reviewed by eye:
  - 30 show the same leaf;
  - 9 possibly show the same leaf;
  - 8 show different leaves, including the one pair across classes.
- Same-leaf and possible same-leaf pairs are kept but placed in the same split group, so they cannot end up on both sides of a split.

**PlantDoc cleaning (73 images excluded).**

- Duplicates: 8 byte-identical groups and 49 perceptual-hash pairs gave 45 groups of repeated photos.
  - In the 26 groups whose copies carry different labels, every copy is excluded.
  - In the 19 same-label groups, one copy is kept.
- Every decision is listed in `docs/plantdoc_cleaning_log.csv` with its reason and reviewer.
- Next step: 25 retained images appear not to be plant photographs (slides, title cards, covers with title text, one figure grid, one drawing). They are listed in `docs/plantdoc_nonphoto_candidates.csv` and will be reviewed and excluded next.

**Leaf grouping in PlantVillage.**

- 11,735 images have a leaf ID from the published leaf maps, and 1 more was matched to a renamed map entry.
- 1,038 images have a leaf-series ID taken from the file name.
- The remaining 4,306 images have no verified leaf ID and are kept in conservative capture-series groups.

**Open issue: tomato mosaic virus.** All 373 tomato mosaic virus images form one capture group, so the class cannot be placed in both training and test data without risking leakage. This needs verified leaf IDs or an agreed change to the split.
