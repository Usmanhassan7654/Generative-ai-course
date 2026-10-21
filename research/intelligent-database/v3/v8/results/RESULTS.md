# V8 Five-Seed Results (Synthetic Data)

600 examples per seed, five seeds (40-44), 3,000 case executions per method. Recreate full raw JSON locally with `python v8.py --out results/v8.json`.

| Method | Eligible-query success | Answered accuracy | Coverage | Modeled units/query |
|---|---:|---:|---:|---:|
| SQL-only | 83.70% | 83.70% | 87.50% | 1.000 |
| V7 strict consensus | 53.87% | 99.01% | 47.60% | 3.363 |
| V8 reconciliation | 90.44% | 98.38% | 80.43% | 4.947 |

All values averaged over five seeds. Full per-seed results are in the downloadable archive and reproducible with the script. This was **synthetic** and used SQLite as a logical multi-store emulator; no real external database services, neural models or independently collected data. Source corruption rates were chosen by the experiment author, favoring the more accurate carrier-event channel. V8 was more costly than baselines and had lower selective accuracy than V7. No established novelty, real-world superiority, or AGI contribution.
