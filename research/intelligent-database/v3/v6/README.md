# PACE-DB V6 — Cross-model agreement verification (research pilot)

**Scope:** Tested automatic escalation on handwritten digit images, Iris structured measurements and scikit-image photographs. This is **not** a true SQL/vector/graph database selector and **not** multimodal VQA. The v5 reference is copied in `reference_v5/` for a self-contained reproduction.

## Run

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
OPENBLAS_NUM_THREADS=1 python experiment.py --out results/v6.json
OPENBLAS_NUM_THREADS=1 python photos_v6.py --out results/photos_v6.json
```

## Method

For each digit or Iris test item, a PCA-KNN and a full-feature KNN vote. If they agree and both pass a validation-calibrated confidence threshold, return their label. Otherwise obtain an SVC decision. When the SVC matches either existing vote, return it; when all three differ, abstain. Dataset labels are not consulted during routing. Thresholds are calibrated only on the validation split. Test labels are used to score outputs afterwards. This is **model agreement**, not independent external evidence verification; the predictors share the training data and may share systematic errors. The verifier evaluates two models up front and therefore consumes more modeled work than V5.

For photos, score the same-source image gallery using color histograms, spatial grayscale and their weighted combination; accept the majority. All photo queries are **augmentations of originals in the reference gallery**; this is a near-duplicate retrieval toy experiment, not general image understanding. Test-set augmentation uses a separate seed.

## Executed results (single seed)

| Dataset | V5 loop | V6 end-to-end | Strongest fixed | V6 coverage | V6 proxy work |
|---|---:|---:|---:|---:|---:|
| Digits, 450 held-out | 443/450 (98.44%) | 445/450 (98.89%) | 445/450 (98.89%) | 448/450 | 4.409 units |
| Iris, 38 held-out | 35/38 (92.11%) | 36/38 (94.74%) | 37/38 (97.37%) | 38/38 | 4.421 units |
| Photos, 56 augmentations | 53/56 (94.64%) | 56/56 (100%) | 56/56 (100%) | 56/56 | Not modeled |

Digits V5 work=1.449 proxy units. V6 does **not** deliver a free improvement; it runs more models. End-to-end accuracy counts abstentions as failures; its selective accuracy on accepted digits is 445/448 (99.33%), which cannot be directly compared to full-coverage accuracy. **No statistical significance, independent photo test, AGI breakthrough, or generalization to open-domain image Q&A is established.**

## Immediate research gaps

Independent verification requires validating against **external source evidence** with provenance, permissions and freshness. Next build real PostgreSQL/Qdrant/Neo4j services, use independent corpus splits with image captions or VQA questions, and compare policy-matched BM25/dense/hybrid/graph retrieval under measured latency and monetary cost. A credible paper needs multiple seeds, confidence intervals, ablations, and the original author-provided train/dev/test split.
