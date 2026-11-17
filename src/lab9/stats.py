"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    if len(human) != len(judge) or not human:
        raise ValueError("labels must be nonempty and paired")
    if any(x not in {"PASS", "FAIL"} for x in [*human, *judge]):
        raise ValueError("labels must be PASS or FAIL")
    return {"tp": sum(h == POS and j == POS for h, j in zip(human, judge)),
            "fp": sum(h != POS and j == POS for h, j in zip(human, judge)),
            "fn": sum(h == POS and j != POS for h, j in zip(human, judge)),
            "tn": sum(h != POS and j != POS for h, j in zip(human, judge))}


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    cm = confusion(human, judge)
    tp = cm["tp"]
    return (tp / (tp + cm["fp"]) if tp + cm["fp"] else 0.0,
            tp / (tp + cm["fn"]) if tp + cm["fn"] else 0.0)


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    cm = confusion(human, judge)
    n = len(human)
    po = (cm["tp"] + cm["tn"]) / n
    hp = (cm["tp"] + cm["fn"]) / n
    jp = (cm["tp"] + cm["fp"]) / n
    pe = hp * jp + (1 - hp) * (1 - jp)
    if pe == 1:
        raise ValueError("kappa undefined")
    return (po - pe) / (1 - pe)


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    import math
    if any(not math.isfinite(x) or not 0 <= x <= 1 for x in (observed_rate, sensitivity, specificity)):
        raise ValueError("rates must lie in [0, 1]")
    denominator = sensitivity + specificity - 1
    if denominator <= 0:
        raise ValueError("judge has no positive discrimination")
    return max(0.0, min(1.0, (observed_rate + specificity - 1) / denominator))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    import numpy as np
    from scipy.stats import bootstrap
    x, y = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or len(x) != len(y) or len(x) == 0:
        raise ValueError("bootstrap requires nonempty paired vectors")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("nonfinite observation")
    if n_resamples < 1 or not 0 < confidence < 1:
        raise ValueError("invalid bootstrap configuration")
    delta = float(np.mean(x - y))
    if len(x) == 1 or np.all(x - y == x[0] - y[0]):
        return delta, delta, delta
    result = bootstrap((x, y), lambda a, b, axis: np.mean(a - b, axis=axis),
                       paired=True, method="percentile", n_resamples=n_resamples,
                       rng=np.random.default_rng(rng), confidence_level=confidence)
    return delta, float(result.confidence_interval.low), float(result.confidence_interval.high)


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    from math import comb
    _validate_pass_k(n, c, k)
    return 1 - comb(n - c, k) / comb(n, k)


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    from math import comb
    _validate_pass_k(n, c, k)
    return comb(c, k) / comb(n, k)


def _validate_pass_k(n: int, c: int, k: int) -> None:
    if any(type(x) is not int for x in (n, c, k)) or not (n > 0 and 0 <= c <= n and 1 <= k <= n):
        raise ValueError("require integer n>0, 0<=c<=n, 1<=k<=n")
