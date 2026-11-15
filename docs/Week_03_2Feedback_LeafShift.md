# **Week 3 Feedback \- LeafShift**

**Members:** Muhammed Pašić, Emin Hadžiabdić, Armin Memišević

**Direction:** Lab-to-field gap in tomato and potato leaf disease recognition

**Provisional label:** promising

## **What works well**

* The research question is excellent. Instead of repeating plant disease classification on PlantVillage, you measure how much performance is lost on uncontrolled photos. That gives the project real value.

* B0 (majority class, with actual counts) and B1 (HOG \+ HSV histogram \+ linear SVM) are exactly the kind of baselines this course expects.

* Macro-F1 on PlantDoc is well justified by class imbalance and unequal error costs, and the bootstrap confidence intervals and your reasoning about the small official PlantDoc test split show that you have looked at the data.

* Clear MUST/SHOULD/COULD/NOT NOW scope, an honest limitation (no images from Bosnia and Herzegovina), an "uncertain" fallback, and no treatment recommendations.

* The repository has the required structure.

## **What needs attention**

1. **Background bias in PlantVillage.** Images have uniform backgrounds and capture conditions per class, so a model can learn the background instead of the symptoms. This is part of your story: plan to show it, for example with Grad-CAM on lab and field images.

2. **Leakage inside PlantVillage.** The same leaf may appear several times, and some copies of the dataset contain augmented duplicates. A random split will inflate the in-domain score and therefore the lab-to-field gap. Check for near-duplicates (for example with perceptual hashing) before splitting.

3. **PlantDoc label noise.** Images were collected from the web, some show several leaves or several diseases. Document your cleaning rule and who made each decision.

4. **License.** Record the license of the Kaggle copy you use, or switch to the original PlantVillage source.

5. **README typo.** The title currently reads "LeafShitf". Please fix it.

## **Required change, due with the Week 7 submission**

Commit the final class-mapping table between PlantVillage and PlantDoc for your 10 classes, with the number of images per class after cleaning, and report the result of a duplicate check on PlantVillage.

## **Also due in Week 7**

The literature and data assignment is explained in the Week 5 session. Include the following in that submission.

* Literature matrix (3-5 sources) and data cards for PlantVillage and PlantDoc in docs/.

* A data-loading notebook with class counts for both datasets and one data-quality observation.

* A first idea of how you will distinguish a drop caused by background change from a drop caused by noisy PlantDoc labels.