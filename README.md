# AI Accelerator Literature & MLPerf Audit

Artifact repository for the Parallel and Distributed Computing (PDC) course project paper:  
**"How Long Do Survey Claims Last? Auditing Provenance, Currency, and Configuration-Dependence in AI Accelerator Literature"**

**Authors:** Muhammad Musab, Muhammad Abdullah, Abdul Rehman Amir   


---

## Files in this Repository

* `ratings.csv` — Independent dual-rater provenance codes for the 24 audited survey claims.
* `gap_ratings.csv` — Independent dual-rater currency codes for the 12 open research gaps.
* `mlperf_closed_llm_results.csv` — Extracted MLCommons Inference datacenter results (v3.1, v4.0, v4.1) for 8× H100 and A100 systems.
* `kappa.py` — Python script to compute Cohen's kappa and agreement matrix for the 24 claims.
* `kappa_gaps.py` — Python script to compute Cohen's kappa and agreement matrix for the 12 gaps.

---

## How to Run

No special libraries are needed—just standard Python 3:

### 1. Compute Cohen's Kappa for Claims (RQ1)
python kappa.py ratings.csv

### 2. Compute Cohen's Kappa for Gaps (RQ2)
python kappa_gaps.py gap_ratings.csv

###Data Summary
Claims Audit: 24 claims across 15 surveys (2024–2026), evaluated for silicon, simulated, vendor, and normalized provenance.
Gaps Audit: 12 open research gaps tracked from baseline publication dates to November 2026 (3 Closed, 5 Partly Addressed, 4 Open).
MLPerf Group: 8× NVIDIA H100-SXM servers on identical host hardware, evaluating throughput spread and cross-round progression.
