# Evidence-Aware Selective Routing for AI-Assisted Banking Support: Architecture and a Reproducibility-First Pilot

**IEEE-style preliminary manuscript — research-in-progress; NOT ready for submission**

**Authors:** To be provided by submitting researchers. No institutional affiliation, funding or ethics review is asserted here.

## Abstract
Large language model applications often require retrieval from heterogeneous sources, yet routing incorrect or unsupported answers into transactional workflows may impose high costs. We study an evidence-aware, abstaining query routing layer that selects among lexical and character-based representations under validation-selected confidence rules, while recording auditable decisions. We introduce a reproducible read-only banking-support triage application and a benchmark specification using BANKING77. A preliminary smoke test on 24 manually assembled utterances across three banking intents, with six held-out examples, found 83.3% classification accuracy for each of word-level TF-IDF, character-level TF-IDF, conventional probability fusion, and the proposed validation-gated method; there was no measured improvement. Abstention accepted four of six test predictions, all correct, but the sample is too small for reliability claims. The implementation provides an integrity-conscious foundation for future evaluation of multi-source, policy-aware retrieval. No full-dataset result or originality claim is asserted.

**Index Terms—** query routing, selective prediction, banking support, information retrieval, AI agents, reproducibility.

## I. Introduction
Relational databases provide strong consistency and exact operations. AI support applications must additionally interpret natural-language requests, retrieve policy text and defer risky or insufficiently evidenced actions. An explicit orchestration layer can preserve transactional systems of record while directing questions to appropriate retrieval resources. This design is an engineering hypothesis, not a replacement for database management systems.

## II. Related Work and Novelty Boundaries
Adaptive-RAG [1] dynamically selects retrieval strategies based on question complexity; therefore, adaptive routing alone is not novel. Corrective Retrieval Augmented Generation [2] already assesses retrieval reliability and takes corrective actions. Spider 2.0 [3] highlights the difficulties of real enterprise text-to-SQL tasks. CRAG [4] targets factual questions requiring fresh and heterogeneous knowledge. BANKING77 [5] provides fine-grained intent examples for banking support. Selective prediction and human review have additional mature prior art, which must be reviewed before a novelty claim. A possible research question is whether *jointly* enforcing evidence provenance, temporal freshness, permission constraints and calibrated risk budgets within a cross-store query planner yields reproducible gains under distribution shift. That unified formulation and its uniqueness have **not** been established here.

## III. Proposed Architecture
The desired, not yet fully implemented, architecture comprises: (1) transactional SQL source of truth; (2) document and semantic retrieval; (3) optional relationship graph; (4) planner that estimates risk, retrieval value and cost; (5) policy gate checking permissions and freshness; (6) answer composer with source-level provenance; and (7) abstention and auditable human review. The present implementation includes only a local text triage model and SQLite logging. This distinction is critical for accurate evaluation.

## IV. Experimental Method
BANKING77 [5] has 10,003 training and 3,080 test utterances representing 77 intents. Files are pinned by upstream commit and SHA256. The benchmark reserves 20% of training data for stratified validation, leaves the official test split untouched until evaluation, trains independent word TF-IDF (1–2 grams) and character TF-IDF (2–5 grams) logistic classifiers and compares their predictions with an equal-probability late fusion. A gate uses validation-only confidence cutoffs to choose a classifier prediction; a separate selective threshold maximizes coverage subject to target validation accuracy 90%, when attainable. The planned primary measures are test accuracy and macro-F1; the paired test difference against hybrid fusion is summarized with 1,500 bootstrap resamples. Accuracy is not a measure of transaction correctness or RAG faithfulness. Threshold search on a single validation split may overfit.

## V. Preliminary Results
The offline six-query smoke test used three categories, split into 12 training, six validation and six test cases. Word logistic, character logistic, hybrid fusion and gated routing each achieved 5/6 (83.33%) accuracy; gain of routing over fusion was 0%. The gate deferred two cases and was correct on the other four. This single small trial does not justify statistical inference, state-of-the-art, safety guarantees or conference performance claims. Full BANKING77 results were **not available in the execution environment at manuscript preparation**.

## VI. Threats to Validity
Banking77 is an intent-classification corpus, not a real customer-operation dataset. The demo contains small and lightly edited examples; labels are known. No neural embedding model, LLM, live external system, SQL transaction, graph engine or temporal document versioning is involved. Probabilities are not calibrated. Confidence thresholds may fail under covariate shift and unseen intents. A genuine publication must include strict held-out test evaluations, matched-capability baselines, multiple random seeds, dataset-license checks, ablation analysis and ethical review where needed.

## VII. Conclusion
This work provides an auditable prototype and a cautious specification for evaluating evidence-aware routing. Its pilot did not outperform a conventional hybrid baseline. Future experiments must test whether explicit permissions, freshness and provenance lead to measurable improvements over prior adaptive retrieval and selective prediction systems. Until then, any contribution is a research hypothesis rather than a verified discovery.

## References
[1] S. Jeong et al., “Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity,” 2024, https://arxiv.org/abs/2403.14403.

[2] S.-Q. Yan et al., “Corrective Retrieval Augmented Generation,” 2024, https://arxiv.org/abs/2401.15884.

[3] F. Lei et al., “Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows,” 2024, https://arxiv.org/abs/2411.07763.

[4] X. Yang et al., “CRAG — Comprehensive RAG Benchmark,” 2024, https://arxiv.org/abs/2406.04744.

[5] I. Casanueva et al., “Efficient Intent Detection with Dual Sentence Encoders,” Proceedings of the 2nd Workshop on NLP for Conversational AI, 2020, https://arxiv.org/abs/2003.04807.

## Additional exploratory multi-store experiment (October 2026)

We implemented a second, *synthetic*, end-to-end demonstration (`multistore.py`) containing 12 invented banking-support documents, 12 manually authored test queries, row-level tenant isolation, document freshness thresholds, explicit relationship edges, hybrid sparse-retrieval scoring, and a SQLite evidence log. In the authored tests, a policy-aware lexical/TF-IDF hybrid retrieved 11/12 desired records; adding graph-constrained routing retrieved 12/12. The ablation removing graph constraints also retrieved 11/12. Unrestricted baselines were weaker but inherently unfair comparators because they omitted mandatory authorization. The 1/12 gain is descriptive only, not a statistically established improvement. Experiments were not performed on real bank customer data and the graph is stored in SQLite rather than an independent graph database. These results MUST NOT be used as the central empirical claim of a conference manuscript.

Proposed falsifiable claim for future work: across multiple held-out domains and realistic permission/freshness changes, evidence-aware multi-store routing improves answer support and access-control compliance at a controlled p95 latency and dollar cost relative to **policy-equivalent** hybrid search, a metadata-filtered vector baseline, and independently implemented adaptive-RAG baselines. This is a planned experiment, not a current finding.
