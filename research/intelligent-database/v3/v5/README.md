# PACE-DB V5: Closed-loop multimodal store-selection pilot

**Research status:** implemented and locally evaluated; **not** a deployed multimodal DB and **not** a demonstration of AGI. This is a test of cheap-first routing and confidence-based verification across feature indices and models.

## Run

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python experiment.py --out results/results.json
python photos.py --out results/photos.json
python repeat.py
```

The datasets are bundled in scikit-learn (`load_digits`, `load_iris`) and scikit-image (`skimage.data`). No live API, download, or private datasets required. Python 3.11+ recommended. Run inside the V5 folder.

## Three independent evaluations

1. **Digits (image classification):** 1797 real handwritten 8x8 grayscale digit images, stratified train/validation/test split, 450 final test images. Cheap 8D PCA+7-NN -> full-pixel 5-NN -> RBF SVC. Predicted class confidence triggers automatic escalation. Thresholds picked *only* using validation labels and cost objective. The independent test labels are **never passed to the inference loop**. This is classification as a **proxy** for selecting visual retrieval stores, not image-text multimodal reasoning.
2. **Iris (structured data):** 150 labeled botanical measurement records, 38 final test rows. The same algorithm evaluated out of domain; **no pictures in Iris**. Negative transfer is reported.
3. **Photographs:** 14 real images shipped with scikit-image, including astronaut, coffee, cat, rocket and scenery, four augmentations per image, 56 seed-separated test perturbations. Color-histogram image lookup followed by confidence-margin verification and full combined lookup. This **is near-duplicate image identification**; the same original photos are in the reference collection. It is **not held-out-image semantic retrieval**. The initial verifier may fail confidently.

## Results (local run, seed 20261021)

| Test | Fast-only | Full-only | Strong/combined | Closed-loop |
|---|---:|---:|---:|---:|
| Digits, n=450 | 95.33% | 98.67% | 98.89% | **98.44%** |
| Iris, n=38 | 92.11% | **97.37%** | 94.74% | 92.11% |
| Photos, n=56 | 94.64% | 100.00% spatial | 100.00% combined | 94.64% |

Digits cost **proxy units**: fast=1, full=3, strong=8; the conditional loop's cumulative attempts cost 1,4,12. The loop averages **1.449 modeled units**, versus full-only 3 and strong-only 8. These are **not measured wall times, cloud prices, or energy**. Photo loop does not escalate on this test, demonstrating confident verification failure.

Three-seed results in `results/repeated.json` are more robust than a single split but still limited by the dataset, model choice, and model-based thresholds.

## What the verifier does / does not verify

1. First route cheap PCA or color-feature store.
2. Inspect model posterior confidence (digits/Iris) or top1-top2 score gap (photos), compare against validation-selected threshold.
3. If below threshold, escalate to stronger independent features/model; log route and scores.
4. Return prediction with trace, and evaluate correctness **afterward** using held-out gold labels.

The verifier checks **uncertainty**, not truth or evidence entailment. It can accept confident false results. It does not check external authorization, freshness, calibration under shift, or information provenance in production. Existing PACE V3 policy gates are separate and have not been integrated into a live multiservice V5 pipeline.

## What needs to happen next

- ScienceQA image-based VQA, Visual Genome image/relationship queries, HotpotQA text and BIRD SQL (separate tracks and publisher licenses).
- Strong baselines: CLIP/SigLIP dual-encoder, dense text embeddings, BM25, true graph traversal, image-caption alignment, neural cross-encoder/reasoner.
- Verify actual *evidence correctness*: cross-index consensus, source integrity, policy scope, entailment against trusted observations, and calibrated abstention.
- Measure real p50/p95 latency, infrastructure cost, memory, energy, token use, selective risk / coverage and confidence intervals on independent corpus-level splits.
- End-to-end connect PostgreSQL, Qdrant and Neo4j. Docker declaration alone is not proof of deployment.

### Academic integrity

Adaptive routing and verifier-based RAG are established research topics. This code is not proof of a new method or publication-ready originality. Do **not** report 98.44% as multimodal question-answering accuracy. Report each track separately and include negative results.
