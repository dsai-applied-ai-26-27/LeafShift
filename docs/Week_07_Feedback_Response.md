# Week 7 response to the Week 3 feedback

| Field | Value |
|---|---|
| Project | LeafShift: lab-to-field gap in tomato and potato leaf disease recognition |
| Team | Muhammed Pašić, Emin Hadžiabdić, Armin Memišević |
| Main submission | `docs/Applied_AI_Week_06_Handout_LeafShift.docx` |

The accepted parts of the proposal are unchanged: the research question, the two baselines (B0 majority class, B1 HOG + HSV histogram + linear SVM), macro-F1 on PlantDoc with bootstrap confidence intervals, the scope, the "uncertain - consult an agronomist" fallback and the 10 shared classes. No model has been trained yet.

## The five points that needed attention

1. **Background bias in PlantVillage.**
   - We will show it with Grad-CAM on lab and field images (Selvaraju et al.).
   - We will also train the same model on colour and on background-removed (segmented) PlantVillage images and compare both on PlantDoc.
   - Noyan (2022) shows that capture bias also affects the leaf itself, so the segmented comparison measures only the background part.
   - Details: `background_vs_label_noise.md`.
2. **Leakage inside PlantVillage.** We used the original release instead of a redistributed copy.
   - Byte-identical files: 14 pairs, all with matching labels. One copy of each is excluded.
   - Perceptual hashing: 61 pairs, and every non-identical pair was reviewed by eye.
   - Every image has a split group, built from the published leaf maps (11,735 images), file-name leaf series and capture-series groups. A random split would leak: in the leaf maps, almost every leaf appears in 4 images.
   - Details: `class_mapping.md`, `plantvillage_leaf_groups.csv`.
3. **PlantDoc label noise.** The cleaning rule is in `data_card_plantdoc.md`, and every decision, with its reason and reviewer, is in `plantdoc_cleaning_log.csv`.
   - Duplicate photos: if the copies carry conflicting labels, all are excluded; if the labels match, one copy is kept.
   - 73 of 966 images are excluded.
   - Next step: 25 retained images appear not to be plant photographs (slides, title cards, a figure grid, a drawing). They are listed in `plantdoc_nonphoto_candidates.csv` and will be reviewed and excluded. A review of the remaining labels follows.
4. **License.** We switched to the original sources:
   - PlantVillage: https://github.com/spMohanty/PlantVillage-Dataset, CC BY-SA 3.0 as declared in its `README_HF.md`;
   - PlantDoc: https://github.com/pratikkayal/PlantDoc-Dataset, CC BY 4.0.

   No images are stored in our repository.
5. **README typo.** Fixed.

## Required change

The class-mapping table for the 10 classes, with counts after cleaning, is in `class_mapping.md` and `class_mapping.csv`:

- PlantVillage: 17,080 → 17,066 images;
- PlantDoc: 966 → 893 images.

The PlantVillage duplicate check is reported in section 4 of the handout and in `week7_section4_status.md`.

## Also due in Week 7

| Item | File |
|---|---|
| Literature matrix (5 sources) | `literature_matrix.md` |
| Data cards for PlantVillage, PlantDoc and the backup dataset | `data_card_plantvillage.md`, `data_card_plantdoc.md`, `data_card_backup.md` |
| Data-loading notebook with class counts for both datasets and one data-quality observation | `notebooks/LeafShift_Week7_Data.ipynb` |
| First idea for separating a background-caused drop from a label-noise-caused drop | `background_vs_label_noise.md` |

## Open issue for the instructor

All 373 PlantVillage tomato mosaic virus images form one capture group, without leaf IDs. Putting the class in both training and test data risks leakage. We would like to agree on how to handle it before building the split.
