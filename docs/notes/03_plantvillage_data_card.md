# Data card - PlantVillage

## Summary

| Field | Description |
|---|---|
| Dataset name | PlantVillage (tomato, potato and pepper subset) |
| Intended use in LeafShift | Controlled-condition reference dataset for tomato and potato leaf-disease classification. |
| Task | Image classification, one crop/disease class per image. |
| Source used by this project | Kaggle dataset `emmarex/plantdisease`, https://www.kaggle.com/datasets/emmarex/plantdisease, downloaded with `kagglehub` into `data/raw/plantvillage`. Provenance marker present: `.complete/datasets/emmarex/plantdisease/1/bundle.complete`. |
| Version / release | Version 1 (the only version on that Kaggle page). Kaggle lists 342.23 MB and 20.6k files. |
| Download date | Container created 2026-11-11. Re-extracted 2026-11-15, which produced a duplicate nested tree that was removed on 2026-11-15. |
| License of exact copy | Kaggle page states "Unknown" and the archive ships no license text. The upstream GitHub repository has no LICENSE file and GitHub reports no license. The official Hugging Face mirror `mohanty/PlantVillage` declares **CC BY-SA 3.0**. See the license section. |
| Citation | Mohanty, Hughes & Salathé (2016), DOI: https://doi.org/10.3389/fpls.2016.01419; Hughes & Salathé (2015), https://arxiv.org/abs/1511.08060 |

## Description

The PlantVillage work is commonly used as a benchmark for recognizing plant species and diseases from leaf images. Mohanty et al. (2016) report 54,306 images, 14 crop species, and 38 crop-disease/healthy classes. Images were collected under controlled conditions, which makes the dataset useful for a clean baseline but creates a gap when a model is applied to less controlled photographs.

The Kaggle copy used here is a 15-folder subset covering tomato, potato and bell pepper, not the full 38-class release.

## Actual counts in this copy

| Measure | Value | Source file |
|---|---:|---|
| Images found | 20,638 | `raw_class_counts.csv` |
| Class folders | 15 | `raw_class_counts.csv` |
| Unreadable images | 0 | `image_quality_report.csv` |
| Exact duplicate pairs (SHA-256) | 14 (28 files) | `plantvillage_exact_duplicate_pairs.csv` |
| Confirmed exclusions recorded | 14 | `plantvillage_exclusions.csv` |
| Images after recorded exclusions | 20,624 | `week7_audit_summary.json` |
| Near-duplicate candidate pairs (pHash, distance <= 4) | 52 (104 files) | `plantvillage_near_duplicate_candidates.csv` |
| pHash failures | 0 | `plantvillage_phash_errors.csv` |
| Images in the 9 selected classes | 13,026 | `week7_class_mapping_counts.csv` |
| Images in the 9 selected classes after exclusions | 13,012 | `week7_class_mapping_counts.csv` |

Duplicate detail: all 14 exact pairs are same-class (6 in `Tomato_healthy`, 8 in `Tomato_Late_blight`). One file from each pair was excluded on 2026-11-15 with reviewer `Emin Hadziabdic`. Of the 52 near-duplicate candidates, 44 are same-class and 8 cross a class boundary, which suggests some are false positives rather than true duplicates. None of the 52 has been reviewed.

The 9 selected classes hold 13,012 of the 20,624 usable images. The rest belong to classes outside the project scope (bell pepper, tomato mosaic virus, tomato yellow leaf curl, tomato target spot) plus Potato - healthy, which was dropped when the shared task moved from 10 classes to 9.

## Known risks and limitations

- **Background and capture bias:** controlled collection makes background, framing and lighting correlate with the class. This is the mechanism behind the lab-to-field gap the project studies.
- **Repeated views:** 14 exact duplicate pairs prove that the same photograph appears twice under different UUID file names. A random split would put both copies on either side and inflate the in-domain score. This is why the exclusions exist.
- **Same leaf, different photo:** the 52 pHash candidates are the visible part of this. The upstream leaf grouping metadata is the reliable answer; see below.
- **Augmented copies:** other redistributed versions of PlantVillage include augmented files. This copy does not appear to, but the file names carry source tags (`GH_HL`, `GHLB2`, `JR_B.Spot`, `GCREC_Bact.Sp`) that identify capture sessions.
- **License uncertainty in the exact copy:** the Kaggle page states "Unknown". The license statement comes from the official mirror, not from the file we downloaded.
- **No Bosnia and Herzegovina images:** the dataset provides no local field images for the target region.

## License status

The Kaggle copy carries no license statement:

> License: Unknown

That is not a grant of rights. Three sources were checked on 2026-11-15:

| Source | License stated |
|---|---|
| Kaggle page `emmarex/plantdisease` | "Unknown" |
| GitHub `spMohanty/PlantVillage-Dataset` | No LICENSE file; the GitHub API returns `"license": null` |
| Hugging Face `mohanty/PlantVillage` (official mirror, card also present as `README_HF.md` upstream) | **CC BY-SA 3.0**, declared in the dataset card metadata |

The report should cite **CC BY-SA 3.0** from the official mirror and state plainly that the Kaggle copy itself carries no license. Two consequences must be written down rather than assumed away:

1. **Attribution** is required: credit the PlantVillage authors and the paper.
2. **ShareAlike** is required: a derived dataset redistributed publicly must carry the same license. If the team only reports results and does not publish derived images, this does not restrict the report, but it does restrict publishing a cleaned image set.

If the instructor wants the license to match the exact downloaded copy rather than the upstream mirror, the fix is to download from the official mirror instead of Kaggle and note the switch.

## Preprocessing and cleaning done by LeafShift

1. Raw files are preserved unchanged in `data/raw/`, which is gitignored.
2. Every image is opened and its dimensions recorded (`image_quality_report.csv`): 0 failures.
3. SHA-256 computed for all 20,638 files (`plantvillage_sha256.csv`).
4. pHash computed for all 20,638 files, 0 failures; candidates stored for inspection.
5. 14 exact duplicate files excluded with reviewer and date (`plantvillage_exclusions.csv`).
6. The duplicate nested extraction tree (`PlantVillage/PlantVillage`) was removed on 2026-11-15, and the notebook now refuses to walk into a folder that repeats its parent's name.

## Grouping metadata available upstream

The upstream repository publishes `leaf_grouping/leaf-map.json`, which maps a normalized source image name to an official leaf identifier and class. The Hugging Face mirror also publishes `splits/color_train.txt` and `splits/color_test.txt`, an 80/20 split that respects that grouping.

A direct test against this copy matched **14,935 of the 20,638 images (72.4%)** to an official leaf ID. The method is implemented in `src/compute_leaf_map_coverage.py`: it lowercases the file-name suffix after `___`, looks it up directly, then retries without the word `Leaf` and with `.` and `_` variants, because the map mixes both. The per-image result is `data/processed/plantvillage_leaf_map_coverage.csv` (20,638 rows; `matched` yes or no, the resolved `leaf_key`, and every `leaf_records` entry for that key, since 400 keys carry more than one record). The map itself is downloaded from the mirror and kept outside version control at `data/raw/leaf_grouping/leaf-map.json`. This is the strongest available defence against the same physical leaf appearing on both sides of a split, and it is better than pHash because it does not depend on the images looking alike.

The remaining 28% would fall back to pHash and the capture-session tags in the file names. This is the recommended split strategy and is not yet implemented.

## Open items

- Review the 52 near-duplicate candidates, or state that they were left unreviewed.
- Build the split using the official leaf IDs where available.
- License is cited as CC BY-SA 3.0 from the official mirror, with the Kaggle copy's "Unknown" status stated alongside it. Closed unless the instructor rejects that approach.

## Data access and references

- Copy used: https://www.kaggle.com/datasets/emmarex/plantdisease
- Official mirror used for the license and grouping metadata: https://huggingface.co/datasets/mohanty/PlantVillage
- Upstream repository: https://github.com/spMohanty/PlantVillage-Dataset
- Paper: https://doi.org/10.3389/fpls.2016.01419
- Dataset description/preprint: https://arxiv.org/abs/1511.08060
