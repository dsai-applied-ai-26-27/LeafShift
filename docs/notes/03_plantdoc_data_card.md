# Data card - PlantDoc

## Summary

| Field | Description |
|---|---|
| Dataset name | PlantDoc |
| Intended use in LeafShift | Web-sourced, uncontrolled-condition image dataset for the cross-dataset evaluation against PlantVillage. |
| Task | Image classification, one target class per image. |
| Source used by this project | Kaggle dataset `nirmalsankalana/plantdoc-dataset`, https://www.kaggle.com/datasets/nirmalsankalana/plantdoc-dataset, downloaded with `kagglehub` into `data/raw/plantdoc`. Provenance marker present: `.complete/datasets/nirmalsankalana/plantdoc-dataset/7/bundle.complete`. |
| Version / release | Version 7. |
| Download date | Container created 2026-11-11. |
| License of exact copy | Kaggle page shows Creative Commons Attribution 4.0 International. The original repository `pratikkayal/PlantDoc-Dataset` is CC-BY-4.0. One field on the Kaggle page also displays a CC0 label, so quote the page as seen and keep a screenshot with the access date. |
| Citation | Singh et al. (2020), DOI: https://doi.org/10.1145/3371158.3371196 |

## Description

The PlantDoc paper presents a dataset for visual plant-disease detection built from images collected from online sources. The paper reports 2,598 data points across 13 plant species and up to 17 disease classes, with roughly 300 human hours of annotation. It is the field-side dataset for this project because its images are not collected under controlled laboratory conditions.

This copy is a `train` / `test` redistribution. It differs from the paper's numbers, which is expected for a redistributed copy and is why the counts below are measured, not quoted.

## Actual counts in this copy

| Measure | Value | Source file |
|---|---:|---|
| Images found | 2,922 | `raw_class_counts.csv` |
| train images | 2,670 | filesystem count |
| test images | 252 | filesystem count |
| train class folders | 28 | filesystem count |
| test class folders | 27 | filesystem count |
| Unreadable images | 0 | `image_quality_report.csv` |
| Images in the 9 mapped classes | 990 | `week7_class_mapping_counts.csv` |
| Review decisions recorded in scope | 990 of 990 | `plantdoc_review.csv` |
| Kept after review, 9 classes | 986 | `week7_class_mapping_counts.csv` |
| Kept after review, 8 evaluable classes | 984 | derived |
| Removed by review | 4 | `plantdoc_review.csv` |

`Tomato_two_spotted_spider_mites_leaf` exists in `train` (2 images) and is absent from `test`.

## Mapping limitations that affect the evaluation

- **Healthy potato is absent.** The copy contains only `Potato_leaf_early_blight` and `Potato_leaf_late_blight`. This is why the shared task moved from 10 classes to 9; see `03_class_mapping.md`.
- **Spider mites has 2 images.** `Tomato_two_spotted_spider_mites_leaf` holds 2 train images and 0 test images, so a per-class F1 for it is not meaningful. It is declared unevaluable on PlantDoc.
- **`Tomato_leaf` is treated as healthy tomato.** The folder name does not state "healthy". All 52 images were inspected during the review of 2026-11-15 and kept under this label (reviewer Emin Hadziabdic), which is the confirmation recorded here. The label rests on the folder name and visual inspection, not on an agronomist's diagnosis.
- **Small official test split.** Only 74 of the kept images belong to our evaluable classes (252 images exist in the test split overall). Macro-F1 on 74 images needs a bootstrap interval, never a bare point estimate.

## Known risks and limitations

- **Web-sourced images:** quality, framing, lighting, resolution and background vary widely, which is the point of the dataset but also a source of noise.
- **Label uncertainty:** an image may show several leaves, several symptoms, or a disease that is hard to identify from a single photograph.
- **Class imbalance:** counts range from 2 to 223 images per folder in this copy.
- **Version differences:** folder names and counts vary between redistributions. Do not copy a class list or count from another mirror.
- **Underlying image rights:** the repository license may not resolve copyright in every third-party photograph.
- **Stock-photo watermarks:** web-scraped images can carry a visible stock-agency watermark (for example Alamy). A watermark does not by itself make a readable leaf unusable, so it is not a removal reason. The review recorded no image removed for a watermark, and the number of watermarked images was not counted separately.
- **Not locally collected:** this is not a Bosnia and Herzegovina field dataset.

## Cleaning rules (as defined in `data_cleaning_protocol.md`)

- **keep:** readable image, target crop identifiable, one target class clear enough for a single-label task.
- **uncertain:** several diseases may be present, symptoms unclear, or the class cannot be confirmed. Excluded from the clean evaluation until resolved.
- **remove:** unreadable, unrelated, wrong crop, no usable leaf or symptom evidence, or clear mismatch with the folder label.

Several leaves are not automatically a reason to remove an image. Every `uncertain` and `remove` decision needs a short reason and a named reviewer.

## Status of the review

**Complete for the declared scope.** `data/processed/plantdoc_review.csv` holds 2,922 rows; the 990 inside the mapped classes are all decided:

| Decision | Count |
|---|---:|
| keep | 986 |
| uncertain | 0 |
| remove | 4 |
| pending in scope | 0 |

The 4 removals sit in `Tomato_leaf_bacterial_spot` (3) and `Tomato_mold_leaf` (1), and each carries a written reason. Every decided row carries `reviewer = Emin Hadziabdic` and `review_date = 2026-11-15`.

The 1,932 rows outside the mapped classes are left undecided on purpose. They are never scored, so they cannot influence a reported metric. `week7_audit_summary.json` records them separately as `plantdoc_rows_outside_scope` and `plantdoc_out_of_scope_pending`, and the notebook gate requires zero pending rows inside the scope rather than in the whole CSV.

The review was done with `src/review_plantdoc.py`, a local page that shows one image at a time and writes each decision into the CSV in the existing column order. It is standard library only and needs no dependencies. Run it with `.venv\Scripts\python.exe src\review_plantdoc.py`.

## Data access and references

- Copy used: https://www.kaggle.com/datasets/nirmalsankalana/plantdoc-dataset
- Original repository: https://github.com/pratikkayal/PlantDoc-Dataset
- Repository license file: https://github.com/pratikkayal/PlantDoc-Dataset/blob/master/LICENSE.txt
- Paper: https://doi.org/10.1145/3371158.3371196
- Preprint: https://arxiv.org/abs/1911.10317
