# Data card - PlantDoc (external test set)

| Field | Value |
|---|---|
| Name | PlantDoc (classification images) |
| Link | https://github.com/pratikkayal/PlantDoc-Dataset, audited at commit `5467f6012d78d1c446145d5f582da6096f852ae8`. Paper: Singh et al. (2020), https://doi.org/10.1145/3371158.3371196 |
| Creator and purpose | Singh, Jain, Jain, Kayal, Kumawat and Batra (IIT Gandhinagar). A dataset of plant disease images taken outside the lab, scraped from Google Images and Ecosia and labelled by the authors |
| Size | Repository: 2,578 images in 28 class folders (train 2,342, test 236); the paper reports 2,598 images and 27 classes. Our 10 classes: 966 images, 85 of them in the official test folder; 893 after cleaning (77 from the test folder) |
| Target | The class given by the folder name, mapped to our 10 PlantVillage classes. `Tomato leaf` is read as healthy tomato and `Tomato leaf yellow virus` as tomato yellow leaf curl virus |
| License | CC BY 4.0 (`LICENSE.txt` of the repository). Course use is allowed with attribution. The images come from the web and some carry their owners' watermarks, so we use them only for evaluation and do not redistribute them |
| Role in LeafShift | External test set only; never used for training or model selection |

## Our 10 classes

| Class | Folder | Images | After cleaning |
|---|---|---:|---:|
| Tomato healthy | `Tomato leaf` | 63 | 63 |
| Tomato bacterial spot | `Tomato leaf bacterial spot` | 110 | 105 |
| Tomato early blight | `Tomato Early blight leaf` | 88 | 76 |
| Tomato late blight | `Tomato leaf late blight` | 111 | 100 |
| Tomato leaf mold | `Tomato mold leaf` | 91 | 90 |
| Tomato Septoria leaf spot | `Tomato Septoria leaf spot` | 151 | 139 |
| Tomato mosaic virus | `Tomato leaf mosaic virus` | 54 | 53 |
| Tomato yellow leaf curl virus | `Tomato leaf yellow virus` | 76 | 72 |
| Potato early blight | `Potato leaf early blight` | 117 | 102 |
| Potato late blight | `Potato leaf late blight` | 105 | 93 |
| **Total** | | **966** | **893** |

The counts pool the train and test folders. The official test folder alone has only 6 to 11 images per class in our classes.

## Cleaning rule

**Duplicates.** Byte-identical files and perceptual-hash pairs were reviewed by eye. If the copies of a photo carry different labels, every copy is excluded. If they carry the same label, the highest-resolution copy is kept, preferring the official test copy on ties. Result: 45 duplicate groups, 73 images excluded.

Every decision, with its reason and reviewer, is in `plantdoc_cleaning_log.csv`. The retained images are listed in `plantdoc_clean_manifest.csv`.

**Next step (not yet applied):** exclude images that are not plant photographs (presentation slides, title cards, covers or thumbnails with title text, labelled figure grids, drawings), while keeping watermarks, captions and photo collages. We have already found 25 retained images that appear to be of this kind; they are listed in `plantdoc_nonphoto_candidates.csv` and still counted above.

## Quality issues

- **Missing or unreadable files:** none; all 966 files open. Widths range from 115 to 6,000 px; 65 images are under 224 px on one side.
- **Imbalance after cleaning:** 53 (tomato mosaic virus) to 139 (tomato Septoria leaf spot) images per class.
- **Label noise:** the authors state that some images may be wrongly labelled, and that tomato bacterial spot and Septoria look alike. Some images show several leaves, a whole plant, or more than one disease, and some may show another crop; 25 appear not to be photographs at all (see Next step). We have not yet reviewed labels independently; this is the label-noise part of `background_vs_label_noise.md`.

## Sensitive content

No personal data in the labels. Some photos show people's hands; some carry copyright watermarks (see License).

## Why it fits

Its uncontrolled photos cover all 10 shared classes and were collected separately from PlantVillage, so we can measure the lab-to-field gap.
