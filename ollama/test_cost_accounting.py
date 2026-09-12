#!/usr/bin/env python3
"""Self-test for cost accounting in run_cloud_benchmark.py.

Makes NO network calls and NO Anthropic API calls — imports only PRICES and
cost_usd from run_cloud_benchmark.py (the `import anthropic` in that module
lives inside run_claude()'s function body, so importing the module here
triggers no SDK/network dependency).

Usage:
    python3 ollama/test_cost_accounting.py

Prints PASS/FAIL per check and exits non-zero if any check fails.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run_cloud_benchmark import PRICES, cost_usd  # noqa: E402

FAILURES = []


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))
    if not condition:
        FAILURES.append(name)


def main():
    model = "claude-sonnet-4-6"
    prices = PRICES[model]

    # 1. input and output tokens must be priced DIFFERENTLY — the core bug
    # this guards against is treating usage as a flat token count.
    cost_1000_output = cost_usd({"output_tokens": 1000}, model)
    cost_1000_input = cost_usd({"input_tokens": 1000}, model)
    check(
        "1000 output tokens cost more than 1000 input tokens (priced differently)",
        cost_1000_output != cost_1000_input and cost_1000_output > cost_1000_input,
        f"output_cost={cost_1000_output}, input_cost={cost_1000_input}",
    )

    # 2. cache_read cheaper than cache_write, and cheaper than fresh input,
    # for the same token count.
    n = 1_000_000
    cost_fresh_input = cost_usd({"input_tokens": n}, model)
    cost_cache_write = cost_usd({"cache_creation_input_tokens": n}, model)
    cost_cache_read = cost_usd({"cache_read_input_tokens": n}, model)
    check(
        "cache_read cheaper than cache_write for the same token count",
        cost_cache_read < cost_cache_write,
        f"cache_read={cost_cache_read}, cache_write={cost_cache_write}",
    )
    check(
        "cache_read cheaper than fresh input for the same token count",
        cost_cache_read < cost_fresh_input,
        f"cache_read={cost_cache_read}, fresh_input={cost_fresh_input}",
    )

    # 3. A known usage dict yields the exact expected dollar figure, hand-
    # computed from the PRICES table.
    usage = {
        "input_tokens": 10_000,
        "output_tokens": 2_000,
        "cache_creation_input_tokens": 5_000,
        "cache_read_input_tokens": 50_000,
    }
    expected = (
        10_000 / 1_000_000 * prices["input"]
        + 2_000 / 1_000_000 * prices["output"]
        + 5_000 / 1_000_000 * prices["cache_write"]
        + 50_000 / 1_000_000 * prices["cache_read"]
    )
    actual = cost_usd(usage, model)
    check(
        "known usage dict yields the exact hand-computed dollar figure",
        abs(actual - expected) < 1e-9,
        f"expected={expected!r}, actual={actual!r}",
    )

    # 4. Missing cache keys default to 0 — no KeyError.
    try:
        result = cost_usd({"input_tokens": 100, "output_tokens": 50}, model)
        check(
            "missing cache_creation/cache_read keys default to 0 (no KeyError)",
            isinstance(result, float),
            f"result={result!r}",
        )
    except KeyError as e:
        check("missing cache_creation/cache_read keys default to 0 (no KeyError)", False, f"KeyError: {e}")

    # 5. Unknown model falls back to _DEFAULT without error.
    try:
        fallback_cost = cost_usd({"input_tokens": 1000, "output_tokens": 1000}, "totally-unknown-model-xyz")
        expected_fallback = (
            1000 / 1_000_000 * PRICES["_DEFAULT"]["input"]
            + 1000 / 1_000_000 * PRICES["_DEFAULT"]["output"]
        )
        check(
            "unknown model id falls back to PRICES['_DEFAULT'] without error",
            abs(fallback_cost - expected_fallback) < 1e-9,
            f"fallback_cost={fallback_cost!r}, expected={expected_fallback!r}",
        )
    except Exception as e:
        check(
            "unknown model id falls back to PRICES['_DEFAULT'] without error",
            False,
            f"{type(e).__name__}: {e}",
        )

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED: {', '.join(FAILURES)}")
        sys.exit(1)

    print(f"All {5} checks PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
