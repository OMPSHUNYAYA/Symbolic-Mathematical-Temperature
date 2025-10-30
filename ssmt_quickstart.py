#!/usr/bin/env python3
"""
ssmt_quickstart.py

Shunyaya Symbolic Mathematical Temperature (SSMT)
Minimal quickstart encoder (observation-only).

Purpose
-------
Show how to turn a raw temperature reading in Celsius into:
 - T_K      : Kelvin with a safety floor
 - e_T      : unitless contrast against a declared reference
 - a_phase  : bounded phase proximity dial around a critical pivot (e.g. freezing)

This script does NOT change physics or calibration.
It only produces portable symbolic signals for monitoring, analytics, and policy.

All formulas are plain ASCII.

Core formulas
-------------
T_K := max( T_C + 273.15 , eps_TK )
e_T := ln( T_K / T_ref )
d_m := ( T_K - T_m ) / DeltaT_m
a_phase := tanh( c_m * d_m )

Where:
 - T_ref is the declared reference Kelvin (e.g. comfort, nominal process temp)
 - T_m is a pivot (e.g. freezing, gel point, safety boundary)
 - DeltaT_m and c_m shape how sharp the phase dial is
 - eps_TK > 0 is a floor to keep math stable

Interpretation
--------------
e_T:
  0.0  -> at reference
  >0.0 -> hotter than reference
  <0.0 -> colder than reference

a_phase:
  near -1.0 -> meaningfully below pivot (cold side)
  near  0.0 -> near pivot
  near +1.0 -> meaningfully above pivot (hot side)

Usage
-----
Run this file directly:
    python ssmt_quickstart.py

You can integrate the encode_* functions into firmware, gateways, or ETL.
"""

from math import log, tanh

# ----------------------------
# Declared constants (example)
# ----------------------------

# Reference temperature in Kelvin for contrast.
# For indoor comfort / general-purpose benchmarks we use ~25 C:
# 25 C = 298.15 K
T_ref = 298.15

# Phase pivot (e.g. freezing point of water).
# This can be changed per material or safety boundary.
T_m = 273.15        # 0 C in Kelvin

# Width around the pivot that we consider "nearby" (softness band).
DeltaT_m = 2.0      # K

# Sharpness for the phase dial tanh().
c_m = 1.2           # >0

# Kelvin floor so we never take log(0) or divide by zero.
eps_TK = 1e-6       # >0


# ----------------------------
# Core helpers
# ----------------------------

def to_kelvin_celsius(T_c):
    """
    Convert Celsius to Kelvin and apply floor.

    Formula:
        T_K := max( T_c + 273.15 , eps_TK )
    """
    return max(T_c + 273.15, eps_TK)


def encode_eT(T_K):
    """
    Compute unitless contrast e_T.

    Formula:
        e_T := ln( T_K / T_ref )
    Assumes log-lens.
    """
    return log(T_K / T_ref)


def encode_a_phase(T_K):
    """
    Compute bounded phase proximity dial a_phase.

    Formulas:
        d_m := ( T_K - T_m ) / DeltaT_m
        a_phase := tanh( c_m * d_m )

    Output is always in (-1, +1).
    Negative => below pivot (cold side).
    Positive => above pivot (hot side).
    """
    d_m = (T_K - T_m) / DeltaT_m
    return tanh(c_m * d_m)


def format_record(timestamp_utc, T_c):
    """
    Produce a minimal SSMT-like record for a single reading.

    Fields shown:
      timestamp_utc : ISO-8601 UTC string (caller-provided)
      T_c           : raw Celsius (for human display only)
      T_K           : Kelvin (floored)
      e_T           : unitless contrast from T_ref
      a_phase       : bounded dial around T_m

    In production SSMT, the emitted payload would also include:
      manifest_id, health, and (optionally) Q_phase, a_T, etc.
    """
    T_K = to_kelvin_celsius(T_c)
    e_T = encode_eT(T_K)
    a_p = encode_a_phase(T_K)

    return {
        "timestamp_utc": timestamp_utc,
        "T_c_human": round(T_c, 2),
        "T_K": round(T_K, 6),
        "e_T": round(e_T, 6),
        "a_phase": round(a_p, 6),
    }


# ----------------------------
# Demo / quick start
# ----------------------------

def main():
    # Example reading:
    # Suppose we sampled 25.0 C at "2025-10-30T09:30:00Z"
    sample_timestamp = "2025-10-30T09:30:00Z"
    sample_T_c = 25.0

    record = format_record(sample_timestamp, sample_T_c)

    print("SSMT quickstart demo record:")
    for k, v in record.items():
        print(f"  {k}: {v}")

    # You can replicate this for any channel:
    #  - indoor sensors
    #  - outdoor weather station
    #  - cold-chain probe
    #  - equipment cabinet sensor
    #
    # Only the constants (T_ref, T_m, DeltaT_m, etc.) need to be
    # declared once in a manifest so everyone knows how to interpret
    # e_T and a_phase.


if __name__ == "__main__":
    main()
