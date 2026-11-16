# LeafShift - Leaf Disease Detection

## Problem Statement
For small vegetable growers in Bosnia and Herzegovina and the advisers who support them, we will use photos of tomato and potato leaves taken in uncontrolled conditions to support early recognition of common leaf diseases by producing one of 10 classes (healthy tomato or one of 9 diseases) with a confidence score and an "uncertain - consult an agronomist" fallback. We will compare the proposed AI approach, an ImageNet-pretrained CNN fine-tuned on lab images (PlantVillage), with a majority-class baseline and a HOG + colour histogram linear SVM, and evaluate it using macro-F1 on uncontrolled photos (PlantDoc) together with the lab-to-field gap, subject to the domain shift between lab and uncontrolled images, label noise in the test data, and the risk that a wrong prediction leads to a wrong treatment.

**Team Members:**
- Emin Hadziabdic - Data and Evaluation lead
- Armin Memisevic - ML and prototyping lead
- Muhammed Pasic - Problem and Project Lead

## Week 7 submission

| Item | File |
|---|---|
| Completed handout (main submission) | [docs/Applied_AI_Week_06_Handout_LeafShift.docx](docs/Applied_AI_Week_06_Handout_LeafShift.docx) |
| Response to the Week 3 feedback | [docs/Week_07_Feedback_Response.md](docs/Week_07_Feedback_Response.md) |
| Literature matrix | [docs/literature_matrix.md](docs/literature_matrix.md) |
| Data cards | [PlantVillage](docs/data_card_plantvillage.md), [PlantDoc](docs/data_card_plantdoc.md), [backup](docs/data_card_backup.md) |
| Class mapping and counts after cleaning (required change) | [docs/class_mapping.md](docs/class_mapping.md) |
| Data-loading notebook | [notebooks/LeafShift_Week7_Data.ipynb](notebooks/LeafShift_Week7_Data.ipynb) |
| Background vs. label-noise idea | [docs/background_vs_label_noise.md](docs/background_vs_label_noise.md) |

After cleaning, the 10 shared classes hold 17,066 PlantVillage images and 893 PlantDoc images. No model has been trained yet.

## Setup

The images are not stored in this repository. Run these commands from the project root.

```bash
python -m pip install -r requirements.txt
git clone --depth 1 --filter=blob:none --sparse https://github.com/spMohanty/PlantVillage-Dataset.git data/PlantVillage-Dataset
git -C data/PlantVillage-Dataset sparse-checkout set raw/color/Tomato___healthy raw/color/Tomato___Bacterial_spot raw/color/Tomato___Early_blight raw/color/Tomato___Late_blight raw/color/Tomato___Leaf_Mold raw/color/Tomato___Septoria_leaf_spot raw/color/Tomato___Tomato_mosaic_virus raw/color/Tomato___Tomato_Yellow_Leaf_Curl_Virus raw/color/Potato___Early_blight raw/color/Potato___Late_blight
```

PlantDoc on **Windows**: some original file names are not valid on Windows. Clone without checking out, then let the script extract the images under the numbered names used in the `windows_path` column of the manifest.

```cmd
git clone --depth 1 --no-checkout https://github.com/pratikkayal/PlantDoc-Dataset.git data/PlantDoc-Dataset-clone
python scripts/fix_plantdoc.py
```

PlantDoc on **Linux or macOS**:

```bash
git clone --depth 1 https://github.com/pratikkayal/PlantDoc-Dataset.git data/PlantDoc-Dataset
```

Then open `notebooks/LeafShift_Week7_Data.ipynb` and choose **Run All**. The scripts in `scripts/` reproduce the duplicate and leaf-map checks; each takes the dataset folder as its first argument.

## Licenses and attribution

- **Code:** MIT, see [LICENSE](LICENSE).
- **PlantVillage:**
  - Sources: Hughes and Salathé (2015), https://arxiv.org/abs/1511.08060, and Mohanty, Hughes and Salathé (2016), https://doi.org/10.3389/fpls.2016.01419. Original release: https://github.com/spMohanty/PlantVillage-Dataset.
  - License: CC BY-SA 3.0, as declared in the repository's `README_HF.md`.
- **PlantDoc:**
  - Source: Singh et al. (2020), https://doi.org/10.1145/3371158.3371196.
  - License: CC BY 4.0 (`LICENSE.txt` of https://github.com/pratikkayal/PlantDoc-Dataset).
- **Backup:** Tomato leaf diseases, Mendeley Data, version 1, https://data.mendeley.com/datasets/93h9p62kg4/1, CC BY 4.0.
- **No image redistribution:** the dataset folders are excluded by `.gitignore`. The files in `docs/` contain paths, counts and decisions, not images.
