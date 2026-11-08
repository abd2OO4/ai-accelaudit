"""Cohen's kappa for the dual-rater gap-currency audit (Section 3.2.1).

Usage:
    python kappa.py ratings.csv

ratings.csv must have a header row with these columns:
    claim_id,rater1,rater2

Allowed codes (case-insensitive):
    closed, partly, open

Each row holds the two raters' independent, pre-discussion codes.
The script prints the agreement matrix (Table 11), p_o, p_e, kappa,
a 95% bootstrap confidence interval, and the list of disagreements
to copy into the resolution log (Table 12).
"""

import csv
import random
import sys

CATEGORIES = ["closed", "partly", "open"]
LABELS = {
    "closed": "Closed",
    "partly": "Partly Addressed",
    "open": "Open",
}


def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            a = r["rater1"].strip().lower()
            b = r["rater2"].strip().lower()
            for code in (a, b):
                if code not in CATEGORIES:
                    sys.exit(f"Unknown code '{code}' for claim {r['claim_id']}")
            rows.append((r["claim_id"].strip(), a, b))
    return rows


def kappa(pairs):
    n = len(pairs)
    p_o = sum(a == b for a, b in pairs) / n
    p_e = 0.0
    for k in CATEGORIES:
        r1 = sum(a == k for a, _ in pairs) / n
        r2 = sum(b == k for _, b in pairs) / n
        p_e += r1 * r2
    if p_e == 1.0:
        return p_o, p_e, float("nan")
    return p_o, p_e, (p_o - p_e) / (1 - p_e)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    rows = load(sys.argv[1])
    pairs = [(a, b) for _, a, b in rows]
    n = len(pairs)

    # Agreement matrix
    print(f"N = {n}\n")
    short = {"closed": "Clo", "partly": "Par", "open": "Ope"}
    print("R1 \\ R2".ljust(26) + "".join(short[c].rjust(6) for c in CATEGORIES) + "  Total")
    for i in CATEGORIES:
        counts = [sum(a == i and b == j for a, b in pairs) for j in CATEGORIES]
        print(LABELS[i].ljust(26) + "".join(str(c).rjust(6) for c in counts) + str(sum(counts)).rjust(7))
    col = [sum(b == j for _, b in pairs) for j in CATEGORIES]
    print("Total".ljust(26) + "".join(str(c).rjust(6) for c in col) + str(n).rjust(7))

    p_o, p_e, k = kappa(pairs)
    print(f"\np_o   = {p_o:.4f}  ({sum(a == b for a, b in pairs)}/{n} agreements)")
    print(f"p_e   = {p_e:.4f}")
    print(f"kappa = {k:.4f}")

    # Bootstrap CI over claims
    rng = random.Random(20261107)
    boots = []
    for _ in range(10000):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        _, _, kb = kappa(sample)
        if kb == kb:  # skip NaN (all codes identical in resample)
            boots.append(kb)
    boots.sort()
    lo = boots[int(0.025 * len(boots))]
    hi = boots[int(0.975 * len(boots)) - 1]
    print(f"95% bootstrap CI = [{lo:.3f}, {hi:.3f}]  ({len(boots)} valid resamples)")

    # Disagreements for Table 6
    dis = [(cid, a, b) for cid, a, b in rows if a != b]
    print(f"\nDisagreements ({len(dis)}):")
    for cid, a, b in dis:
        print(f"  {cid}: R1 = {LABELS[a]} | R2 = {LABELS[b]}")


if __name__ == "__main__":
    main()
