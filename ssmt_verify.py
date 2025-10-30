#!/usr/bin/env python3
"""
ssmt_verify.py

Shunyaya Symbolic Mathematical Temperature (SSMT)
Basic self-check / CI harness.

Purpose
-------
This script runs a small set of sanity checks to confirm that:
 - The math is being applied correctly (Kelvin floor, log lens, phase dial).
 - The symbolic outputs behave as promised (monotone contrast, bounded dial).
 - The reference point and pivots line up with expectations.

This is meant for:
 - CI pipelines
 - vendor onboarding
 - procurement review
 - regulator / auditor demos

All formulas are plain ASCII.

Key formulas
------------
T_K := max( T_c + 273.15 , eps_TK )
e_T := ln( T_K / T_ref )
d_m := ( T_K - T_m ) / DeltaT_m
a_phase := tanh( c_m * d_m )

Conventions
-----------
We treat "pass" as boolean True. Any False indicates a spec violation
or a mismatch with the declared constants below.

Note
----
This harness is intentionally simple. It is NOT a substitute for full
compliance testing in Section 5 ("Validation — Tier S1") or governance
checks in Section 8.
"""

from math import log, tanh


# ----------------------------
# Declared constants (must match your manifest)
# ----------------------------

T_ref = 298.15      # Kelvin reference (e.g. ~25 C comfort / nominal range)
T_m = 273.15        # Pivot (e.g. freezing, 0 C in Kelvin)
DeltaT_m = 2.0      # Softness band width (K) around the pivot
c_m = 1.2           # Sharpness for the phase dial
eps_TK = 1e-6       # Kelvin floor to keep math stable


# ----------------------------
# Core helpers (same as quickstart)
# ----------------------------

def to_kelvin_celsius(T_c):
    """
    T_K := max( T_c + 273.15 , eps_TK )
    """
    return max(T_c + 273.15, eps_TK)


def encode_eT(T_K):
    """
    e_T := ln( T_K / T_ref )
    """
    return log(T_K / T_ref)


def encode_a_phase(T_K):
    """
    d_m := ( T_K - T_m ) / DeltaT_m
    a_phase := tanh( c_m * d_m )
    """
    d_m = (T_K - T_m) / DeltaT_m
    return tanh(c_m * d_m)


# ----------------------------
# Verification tests
# ----------------------------

def test_floor_nonzero_kelvin():
    """
    Kelvin should never drop below eps_TK.
    We simulate an extreme -300 C input (physically impossible but good for clamp test).
    """
    T_c_extreme = -300.0
    T_K = to_kelvin_celsius(T_c_extreme)
    return T_K >= eps_TK and T_K > 0.0


def test_reference_zero_contrast():
    """
    At T_ref, e_T should be ~0 by definition of e_T := ln( T_K / T_ref ).
    """
    e_at_ref = encode_eT(T_ref)
    return abs(e_at_ref - 0.0) < 1e-9


def test_contrast_signs():
    """
    Hotter than T_ref should yield e_T > 0.
    Colder than T_ref should yield e_T < 0.
    """
    hot_K = T_ref + 50.0        # e.g. ~75 C
    cold_K = T_ref - 50.0       # e.g. ~ -25 C relative to T_ref (still >0 K)
    e_hot = encode_eT(hot_K)
    e_cold = encode_eT(cold_K)
    return (e_hot > 0.0) and (e_cold < 0.0)


def test_phase_bounds():
    """
    a_phase is a tanh() output, so it must always sit strictly between -1 and +1.
    We'll probe multiple Celsius values (cold, near pivot, warm).
    """
    probe_c = [-20.0, 0.0, 20.0]  # C
    vals = []
    for T_c in probe_c:
        T_K = to_kelvin_celsius(T_c)
        vals.append(encode_a_phase(T_K))

    # all values should be in (-1, +1)
    bounded = all(-1.0 < v < 1.0 for v in vals)

    # also check that sign matches expectation:
    # Below freezing (~-20 C) => negative (cold side)
    # Near freezing (0 C)     => near 0
    # Warm (~20 C)            => positive (warm side)
    logic_ok = (vals[0] < 0.0) and (abs(vals[1]) < 0.6) and (vals[2] > 0.0)

    return bounded and logic_ok


def test_monotonic_eT():
    """
    e_T must be monotone in T_K for a fixed lens.
    That means if T_K1 < T_K2 then e_T1 <= e_T2.
    We'll check a small ascending ladder.
    """
    ladder_c = [0.0, 10.0, 20.0, 30.0]  # Celsius
    ladder_e = []
    for T_c in ladder_c:
        T_K = to_kelvin_celsius(T_c)
        ladder_e.append(encode_eT(T_K))

    # Check non-decreasing order
    monotone = all(ladder_e[i] <= ladder_e[i+1] for i in range(len(ladder_e)-1))
    return monotone


def test_roundtrip_sanity():
    """
    If two rooms at different locations read the same Celsius, they should
    produce the same e_T (assuming same declared manifest).

    Here we just call encode_eT twice with the same input.
    """
    roomA_c = 25.0
    roomB_c = 25.0
    eA = encode_eT(to_kelvin_celsius(roomA_c))
    eB = encode_eT(to_kelvin_celsius(roomB_c))
    return abs(eA - eB) < 1e-12


# ----------------------------
# Harness
# ----------------------------

def run_all():
    tests = [
        ("floor_nonzero_kelvin",   test_floor_nonzero_kelvin),
        ("reference_zero_contrast", test_reference_zero_contrast),
        ("contrast_signs",         test_contrast_signs),
        ("phase_bounds",           test_phase_bounds),
        ("monotonic_eT",           test_monotonic_eT),
        ("roundtrip_sanity",       test_roundtrip_sanity),
    ]

    print("SSMT verification summary:")
    passed = True
    for name, fn in tests:
        ok = fn()
        print(f"  {name}: {ok}")
        if not ok:
            passed = False

    print("")
    if passed:
        print("ALL CHECKS PASSED")
    else:
        print("ONE OR MORE CHECKS FAILED")
        print("Inspect constants (T_ref, T_m, DeltaT_m, etc.) and implementation before deployment.")


if __name__ == "__main__":
    run_all()
