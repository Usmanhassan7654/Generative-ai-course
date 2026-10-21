# V6 executed benchmark summary (October 21, 2026)

Run `python experiment.py --out results/v6.json` and `python photos_v6.py --out results/photos_v6.json` from the V6 directory; full JSON output also ships in the ZIP.

| Dataset | V5 | V6 | Strong fixed | Coverage V6 |
|---|---|---|---|---|
| Handwritten digits (450 test images) | 443/450 (98.44%) | 445/450 (98.89%) | 445/450 (98.89%) | 448/450 |
| Iris structured data (38 test) | 35/38 (92.11%) | 36/38 (94.74%) | 37/38 (97.37%) | 38/38 |
| Scikit-image photograph augmentations (56) | 53/56 (94.64%) | 56/56 (100%) | 56/56 (100%) | 56/56 |

V6 digit proxy cost 4.409 vs V5 1.449 assigned units. Only four functional tests; all passed.

**Scientific limits:** predictive agreement is NOT independent evidence verification; photo augmentations reuse original source images; no production SQL/Qdrant/Neo4j services tested; no VQA; no real monetary cost or latency benchmark; no proven originality or AGI contribution. For digits V6 abstained on 2 cases: 445/448 accepted correct, and 445/450 end-to-end correct with abstentions penalized. Strongest fixed matches 445/450, so V6 does not exceed it. All figures arise from a single split and seed.
