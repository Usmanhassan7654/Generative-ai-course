# V5 research log | 2026-10-21

## Benchmarks to integrate after this locally runnable prototype

- ScienceQA: multi-domain multimodal MCQ dataset; image-context questions with explanations. https://scienceqa.github.io/ and https://github.com/lupantech/ScienceQA . Candidate for images + questions; requires full image ingestion and a vision-language model before evaluation.
- Visual Genome: photographs with region text and object relationships; tests multimodal graph routing. https://visualgenome.org/home and https://visualgenome.org/api/v0/api_endpoint_reference . Large download and license review necessary.
- HotpotQA: multi-hop textual evidence. https://github.com/hotpotqa/hotpot . Existing V3 entrypoint not yet run to completion here.
- BIRD: text-to-SQL reasoning. https://bird-bench.github.io/ . Not yet run.

## Falsifiable V5 design

Hypothesis A: iterative low-cost selection approaches the best fixed method's held-out accuracy at lower computational cost.
Hypothesis B: verification prevents confident errors on unseen images.

**Findings:** A partly supported only on digits **under assigned cost proxies**. B contradicted by photos: 3/56 color-only misses were confidently accepted. Iris fails to improve on best fixed. True inference latency and dollars are not benchmarked. A route-selection policy is not equivalent to automatic switching among independent databases, nor does it establish AGI.

## Good next hypothesis

A cross-modal verifier using independent visual feature agreement + calibration + abstention can reduce unsupported confident retrieval decisions at target coverage while respecting source policy. To claim improvement, benchmark against a verification-aware multi-index baseline at equal recall/coverage and equal permitted evidence.
