SSMT
License: Open standard, open source. (See "Full License / Usage" below.)

SSMT — Public Demo Bundle (v2.3)

Intro (brief)

This bundle provides a minimal, observation-only temperature standardization tool.
It converts any raw Celsius/Fahrenheit input into symbolic, comparable, and audit-ready values:

e_T — unitless contrast from a reference temperature T_ref
e_T := ln( T_K / T_ref )

a_phase — bounded dial showing side and distance from a key pivot
a_phase := tanh( c_m * ( (T_K - T_m) / DeltaT_m ) )

(optional) a_phase_fused — multi-pivot survival dial when more than one safety boundary matters
a_phase_fused := tanh( sum_i( c_m_i * ( (T_K - T_m_i) / DeltaT_m_i ) ) )

(optional) Q_phase — adaptive hysteresis memory to stabilize alerts near freezing / gel / burn thresholds

All logic operates on these symbolic lanes (e_T, a_phase / a_phase_fused, Q_phase).
Physics and human °C/°F displays remain untouched. Human comfort displays can still show °C or °F.
Machine logic should consume only the symbolic lanes.

Included Files

Python Demos

• ssmt_quickstart.py
Full working demo (Celsius → Kelvin floor → e_T, a_phase).
Produces a minimal record with timestamp, human-readable °C, Kelvin, and symbolic lanes.
Uses the default log lens:
e_T := ln( T_K / T_ref )

• ssmt_verify.py
Mathematical self-check (Kelvin floor, monotonicity of e_T, boundedness of a_phase, round-trip reproducibility).
Intended as a mini CI gate for procurement, regulators, and QA.

Guides

• GETTING_STARTED.txt
Setup, usage, interpretation, pooling guidance, and how to read each field.

• CALIBRATION.txt
Canonical constants (T_ref, T_m, DeltaT_m, c_m, eps_TK, hysteresis knobs).
This is the manifest you publish so others can replay your stream.

Documents

• docs/SSMT_ver2.3.pdf
Full specification (formulas, semantics, safety rules).

Optional Runtime

• logs/ folder
You may drop CSV or JSON-style samples here (timestamp, raw reading, T_K, e_T, a_phase, etc.) to prove traceability.

Quick Start

Windows
cd "C:\Users\<you>\Desktop\SSMT"
python ssmt_quickstart.py

macOS / Linux
python3 ssmt_quickstart.py

Expected output

timestamp_utc: 2025-10-30T09:30:00Z
T_c_human: 25.0
T_K: 298.15
e_T: 0.0
a_phase: 1.0

How to read this:

• e_T = 0.0 means the sensor reading sits exactly at the declared reference T_ref (for example T_ref = 298.15 K, ~25 C comfort baseline).
• a_phase = 1.0 means “well above the cold-risk threshold,” i.e. safely on the warm side of freezing.

Verification / CI-style check

Run:
python ssmt_verify.py (Windows)
python3 ssmt_verify.py (macOS / Linux)

You should see:
ALL CHECKS PASSED

This confirms:

• Kelvin floor is applied:
T_K := max( to_kelvin(T_raw, unit_flag) , eps_TK )

• Contrast baseline is consistent and monotone:
e_T := ln( T_K / T_ref )

• Phase dial stays bounded and signed by side of pivot:
a_phase := tanh( c_m * ( (T_K - T_m) / DeltaT_m ) )

• Identical Celsius under the same manifest gives identical e_T (round-trip reproducibility across vendors / rooms / buildings / planets).

Manifest Lock (before deployment)

Declare once, then freeze:

T_ref=298.15
T_m=273.15
DeltaT_m=2.0
c_m=1.2
eps_TK=1e-6
rho_min=0.50
rho_max=0.95
sigma0=0.1
k_side=0.5
W=30

This set of constants is your manifest.
Every downstream consumer can recreate e_T, a_phase (or a_phase_fused), and Q_phase from raw Kelvin using only this manifest.
Do not silently change these knobs mid-run; changing them without disclosure breaks auditability and invalidates comparisons.

Pooling / fleets

When combining multiple sensors into one dashboard / site score / regulator report, you must pool bounded dials safely so one rogue sensor cannot dominate. Use rapidity-style pooling:

Clamp each dial away from ±1:
a_clamped := clamp( a_in , -1+eps_a , +1-eps_a )

Convert to rapidity:
u_i := atanh( a_clamped_i )

Weighted accumulate:
U := sum_i( w_i * u_i )
W := max( sum_i( w_i ) , eps_w )

Map back, bounded:
a_pooled := tanh( U / W )

This is mandatory for cross-sensor / cross-vendor comparability at scale.

Full License / Usage

SSMT is open source and released as an open standard.
It may be implemented by any organization — public, industrial, municipal, national, academic, commercial, or off-world habitat — 
with no registration or fees, provided formulas are implemented exactly as declared in a published manifest.

Minimum citation requirement:
When implementing or adapting, cite the concept name "Shunyaya Symbolic Mathematical Temperature (SSMT)" as the origin of the symbolic mathematical temperature approach.

Non-exclusivity:
Implementations are independent. No central registry, hosted service, or maintainer approval is required. 
No implementer may claim exclusive ownership, stewardship, endorsement, or representation of the standard.

Integrity requirement:
e_T, a_phase, a_phase_fused, and any pooled or memory-stabilized derivatives (for example Q_phase) must preserve their defined meaning. 
If you alter any formula (for example, choosing a different lens than e_T := ln( T_K / T_ref ), or redefining the pivot logic in a_phase), 
you must clearly declare that change in your manifest and downstream documentation.

Warranty disclaimer:
The bundle is provided strictly "as-is," with no warranty and no safety guarantee.
This is an observation-only symbolic layer.
It does not replace physical calibration, local procedures, engineering judgment, or mandated safety thresholds.