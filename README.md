# LeafShift - Leaf Disease Detection

## Problem Statement
For small vegetable growers in Bosnia and Herzegovina and the advisers who support them, we will use photos of tomato and potato leaves taken in uncontrolled conditions to support early recognition of common leaf diseases by producing one of 9 disease classes with a confidence score and an "uncertain - consult an agronomist" fallback. We will compare the proposed AI approach, an ImageNet-pretrained CNN fine-tuned on lab images (PlantVillage), with a majority-class baseline and a HOG + colour histogram linear SVM, and evaluate it using macro-F1 on uncontrolled photos (PlantDoc) together with the lab-to-field gap, subject to the domain shift between lab and uncontrolled images, label noise in the test data, and the risk that a wrong prediction leads to a wrong treatment.

**Team Members:**
- Emin Hadziabdic - Data and Evaluation lead
- Armin Memisevic -  ML and prototyping lead
- Muhammed Pasic - Problem and Project Lead

## Licenses and attribution

- **Code:** MIT, see [LICENSE](LICENSE).
- **PlantVillage:** images from the PlantVillage dataset by Mohanty, Hughes and Salathé (2016). The Kaggle copy used here (`emmarex/plantdisease`) carries no license statement ("Unknown"); the official mirror `mohanty/PlantVillage` declares **CC BY-SA 3.0**, which is the license recorded in `docs/notes/03_plantvillage_data_card.md`. Attribution and ShareAlike apply to the images, not to this code.
- **PlantDoc:** images from PlantDoc by Singh et al. (2020), **CC BY 4.0**, as stated on the Kaggle copy (`nirmalsankalana/plantdoc-dataset`) and in the original repository.
- **No image redistribution:** `data/raw/` is excluded from version control, so this repository does not redistribute either dataset. The tables in `data/processed/` contain file paths, hashes and counts, not image content.
- **Citation:** Mohanty, Hughes and Salathé (2016), https://doi.org/10.3389/fpls.2016.01419; Singh et al. (2020), https://doi.org/10.1145/3371158.3371196.