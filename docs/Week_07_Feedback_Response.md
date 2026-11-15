# Week 7 response to the Week 3 feedback

| Field | Value |
|---|---|
| Project | LeafShift: lab-to-field gap in tomato and potato leaf disease recognition |
| Team | Muhammed Pašić, Emin Hadžiabdić, Armin Memišević |
| Date | 2026-11-15 |

This document responds to the Week 3 feedback and reports the Week 7 deliverables. Every attention item is addressed, the final class mapping is committed, and both datasets are cleaned, reviewed and counted. The experiments the feedback sets up, starting with Grad-CAM, form the next phase.

## What works well

The accepted parts of the proposal are unchanged: the research question, the two baselines, macro-F1 on uncontrolled photos with bootstrap intervals, the scope and its stated limitations, the "uncertain - consult an agronomist" fallback, and the repository structure. One deliberate change was made to the label space, from ten classes to nine, and it is justified below.

## Response to the five attention items

### 1. Background bias in PlantVillage

The concern is that uniform backgrounds and capture conditions let a model learn the background instead of the symptoms.

We defined a two-stage test. First, Grad-CAM on the PlantVillage-trained model, applied to images from both domains, to show where the model looks. Second, a controlled intervention that compares each image with a leaf-masked or neutral-background version; a large change under a background-only edit indicates background sensitivity. The design treats a heatmap as evidence of attention, not as proof of causation.

Grad-CAM and the intervention are the first experiments of the next phase.

### 2. Leakage inside PlantVillage

The concern is that the same leaf may appear several times, and that some redistributions carry augmented duplicates, so a random split would inflate the in-domain score.

We checked every image in the copy at byte level, then ran a perceptual-hash pass to catch visually similar images. The check found 14 byte-identical pairs, all within the same class. One copy of each pair was excluded, with a recorded reviewer and date, leaving 20,624 usable images. The perceptual pass produced 52 near-duplicate candidates; because a candidate is not a confirmed duplicate, they were listed for review rather than removed. We also confirmed that this copy does not contain the augmented duplicates found in some redistributions, and that its file names carry capture-session tags that support grouping.

The split will be built on the official leaf grouping published with the dataset, which matched 72% of the images to a physical leaf identifier, with perceptual hashing and capture tags covering the remainder. Building that split is the next step.

### 3. PlantDoc label noise

The concern is that PlantDoc images were collected from the web, some show several leaves or several diseases, and the cleaning rule and each decision maker must be documented.

We defined three decisions. An image is kept when it is readable, the crop is identifiable and one target class is clear. It is marked uncertain when several diseases are plausible or the evidence is insufficient. It is removed when it is broken, irrelevant, the wrong crop, or clearly mismatched with its folder. Several leaves alone are not a reason to remove an image. Every uncertain or removed image requires a written reason.

Every image in the nine mapped classes was reviewed: 990 decisions, 986 kept, 4 removed, none uncertain. Each decision is signed by the data and evaluation lead with the date. The four removals are presentation slides with a leaf photo and text overlay, not usable leaf images. Images outside the mapped classes are never scored and are recorded separately.

### 4. License

The concern is that the license of the Kaggle copy had to be recorded, or the source switched to the original release.

Three sources were checked. The Kaggle copy states "Unknown" and ships no license text. The upstream repository has no license file. The official Hugging Face mirror, published under the dataset authors' account and carrying the same dataset card as their repository, declares CC BY-SA 3.0. We cite that license, record the Kaggle copy's status alongside it, and note the consequences: attribution is required, and ShareAlike applies to any publicly redistributed derived image set, though not to reported results.

PlantDoc is recorded as CC BY 4.0, with one field on its Kaggle page showing a CC0 label, quoted as seen.

### 5. README typo

The title is corrected and the problem statement now states nine classes.

## Final class mapping

The shared task moved from ten classes to nine. PlantDoc has no healthy potato class under any spelling, so a ten-class model could be scored on only nine classes there, and macro-F1 would average over different label sets on the two sides. Healthy potato remains on disk and is out of scope.

Each canonical class corresponds to one folder in each dataset; the exact folder names and the alias resolution are recorded in the repository. All nine classes resolve on both sides.

| Canonical class | PlantVillage images | PlantDoc before review | PlantDoc after review |
|---|---:|---:|---:|
| Potato - early blight | 1,000 | 171 | 171 |
| Potato - late blight | 1,000 | 208 | 208 |
| Tomato - bacterial spot | 2,127 | 110 | 107 |
| Tomato - early blight | 1,000 | 88 | 88 |
| Tomato - late blight | 1,901 | 111 | 111 |
| Tomato - leaf mold | 952 | 91 | 90 |
| Tomato - septoria leaf spot | 1,771 | 157 | 157 |
| Tomato - spider mites | 1,676 | 2 | 2 |
| Tomato - healthy | 1,585 | 52 | 52 |
| **Total** | **13,012** | **990** | **986** |

After cleaning, the nine PlantVillage classes hold 13,012 images and the nine PlantDoc classes hold 986. Spider mites has two PlantDoc images and none in the test split, so it is declared unevaluable there. The PlantDoc metric therefore covers eight classes and 984 images, 910 in training and 74 in test.

The duplicate check is summarised below.

| Check | Pairs | Files | Same class | Cross class | Action |
|---|---:|---:|---:|---:|---|
| Exact duplicates | 14 | 28 | 14 | 0 | one file per pair excluded |
| Near-duplicate candidates | 52 | 104 | 44 | 8 | listed for review before the split |

Both passes covered all 20,638 images with no failures.

## Summary

The literature matrix covers four sources: the PlantVillage release, the study that reported its steep drop on outside images, the PlantDoc paper, and the Grad-CAM method. Each entry records the problem, method, data, evaluation and what we adopt.

Both data cards are complete. They record source, version, download date, measured counts, license status and limitations, and the PlantDoc card adds the review outcome.

The data-loading notebook loads both datasets, resolves the nine-class mapping and counts every class. It opened 23,560 images with no failures. The data-quality observation is that integrity is clean and duplication is the real risk: nothing failed to open, but the byte-level pass still found 14 identical pairs under different file names.

The first design for separating a background-caused drop from a label-noise-caused drop gives each hypothesis its own test. For background, heatmaps are compared across domains and the same images are re-scored with the leaf masked or the background neutralised. For label noise, two team members independently review a fixed sample, disagreements are resolved, and performance on the clear subset is compared with the full set. The two effects are reported separately.

## Next phase

The next phase starts with Grad-CAM on lab and field images and the background intervention. It continues with the grouped split, the confidence threshold, and the baseline and CNN runs, evaluated on both datasets with bootstrap intervals. These are the experiments the feedback anticipates, and they are already designed.

All counts, decisions and review records are kept in the project repository.
