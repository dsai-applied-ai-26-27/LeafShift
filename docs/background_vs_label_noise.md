# First idea: background change vs. noisy PlantDoc labels

**Question.** When a model trained on PlantVillage scores lower on PlantDoc, how much of the drop comes from the new backgrounds, and how much from wrong or doubtful PlantDoc labels?

This is a first idea, not an evaluation protocol. No model is trained before Week 7.

## 1. Background

- **Two training versions.** Train the same model twice on the same leaf-grouped PlantVillage split:
  - once on the colour images (`raw/color`);
  - once on the background-removed images (`raw/segmented`). Every one of our 17,080 colour images has a segmented counterpart with the same file name.

  Test both on the same cleaned PlantDoc set. A smaller drop for the segmented model would be evidence that the model is sensitive to background cues. In Mohanty et al. (2016), the best model on one of their two external sets was trained on segmented images. Ahmad et al. (2023) found that removing the background from field training images improved generalisation for corn.
- **Grad-CAM.** On a sample of lab and field images per class, check whether the model looks at the leaf or at the background.
- **Caveats.**
  - Noyan (2022) showed that removing the background does not remove capture bias, such as blur, from the leaf itself. Use that comparison as evidence about background sensitivity and account for capture bias when interpreting it.
  - Segmented PlantVillage images have a black background (checked on a sample), while PlantDoc images have natural ones. The segmented model still meets a new background at test time. Ahmad et al. (2023) saw this kind of mismatch: their PlantVillage-trained models could not recognise northern leaf blight on field images with a black background.

## 2. Label noise

- **Per-image record.** The duplicate review and exclusions are recorded in the cleaning log. During a separate label review, record who checked each image and assign a status such as:
  - **clear:** one disease, label confirmed;
  - **doubtful:** several leaves or diseases, unclear symptoms, or conflicting near-duplicates;
  - **removed:** with the reason.
- **Two scores.** Report macro-F1 on the full cleaned set and on the clear subset only. A higher score on the clear subset is consistent with label noise, but those photos may also be easier. Comparing the same photos under their original and independently reviewed labels would help separate these effects.
- **Agreement check.** A second team member re-labels a random sample of PlantDoc images without seeing the original labels. The agreement rate shows how noisy the labels are. Singh et al. (2020) state that some images may be wrongly labelled, and that tomato bacterial spot and Septoria look similar.

## 3. What remains

Other field conditions include lighting, angle, several leaves, resolution, and capture bias. Report any remaining gap as unexplained.

**Risk.** The clear subset and some classes will be small (PlantDoc has 54-151 images per class before cleaning). The bootstrap confidence intervals may overlap, and the result may be inconclusive. If so, we will report that.
