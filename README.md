# SSMT — portable symbolic temperature lanes (stable, comparable, auditable). Observation-only.

![GitHub Stars](https://img.shields.io/github/stars/OMPSHUNYAYA/Symbolic-Mathematical-Temperature?style=flat&logo=github) ![License](https://img.shields.io/badge/license-Open%20Standard%20%2F%20Open%20Source-brightgreen?style=flat&logo=open-source-initiative)

SSMT
License: Open standard, open source. (See "License" below for full terms.)

SSMT — Public Demo Bundle (v2.3)

**[Preview document (PDF)](https://github.com/OMPSHUNYAYA/Symbolic-Mathematical-Temperature/blob/main/docs/SSMT_ver2.3.pdf)**

## Intro

Shunyaya Symbolic Mathematical Temperature (SSMT) turns raw degC/degF readings into portable, auditable signals that can be compared across rooms, vendors, buildings, cities, or even planets — without changing physics or local safety rules.

Instead of only saying "it's 25 degC", SSMT emits stable symbolic lanes:

- `e_T` — unitless contrast from a declared reference `T_ref`
  `e_T := ln( T_K / T_ref )`

- `a_phase` — bounded dial in (-1,+1) that tells you which side of a critical threshold (for example freezing, gel point, burn limit) you are on and by how much
  `a_phase := tanh( c_m * ( (T_K - T_m) / DeltaT_m ) )`

- `(optional) a_phase_fused` — multi-pivot survival dial when more than one boundary matters
  `a_phase_fused := tanh( sum_i( c_m_i * ( (T_K - T_m_i) / DeltaT_m_i ) ) )`

- `(optional) Q_phase` — adaptive hysteresis memory that smooths flicker near danger zones

These symbolic lanes are designed for insurance, compliance, ESG, uptime guarantees, warranty enforcement, and long-horizon risk dashboards. Human displays can keep showing degC/degF, but machine logic should consume the symbolic lanes.

SSMT is an open standard, open source, observation-only layer; it does not replace calibration, safety SOPs, or engineering judgment.

## Why it matters

- Comparable anywhere  
  Two facilities (or two vendors) can prove they are holding the same condition using the same symbolic numbers, not just "we're both around 25 degC". The lane `e_T` is a unitless contrast against a declared `T_ref`, so it is portable.

- Alert stability instead of noise  
  `Q_phase` adds adaptive hysteresis so alarms do not flap every time you bounce around a limit. This supports real SLAs and audit trails instead of endless "false alert" emails.

- Executive / regulator clarity  
  "Show me where we're near freezing risk, across every site, with one number." Bounded dials like `a_phase` and `a_phase_fused` directly encode "how close to trouble" and "which side of the line."

- Audit and warranty  
  A fixed manifest (the published constants such as `T_ref`, `T_m`, `DeltaT_m`, `c_m`, `eps_TK`, plus hysteresis knobs) lets any third party replay exactly what you claimed later. If you say "safe", they can verify it numerically.

- Zero lock-in  
  There is no central service, no paywall, no proprietary API. You publish your manifest, you emit the numbers, anyone can verify. SSMT is an open standard and open source. You keep control.

## Documents (Preview)

**Full Specification (PDF):**  
[Preview](https://github.com/OMPSHUNYAYA/Symbolic-Mathematical-Temperature/blob/main/docs/SSMT_ver2.3.pdf) • [Download](https://github.com/OMPSHUNYAYA/Symbolic-Mathematical-Temperature/raw/main/docs/SSMT_ver2.3.pdf)

**GETTING_STARTED_SSMT.txt:**  
[Preview](https://github.com/OMPSHUNYAYA/Symbolic-Mathematical-Temperature/blob/main/GETTING_STARTED_SSMT.txt) • [Download](https://github.com/OMPSHUNYAYA/Symbolic-Mathematical-Temperature/raw/main/GETTING_STARTED_SSMT.txt)

**CALIBRATION_SSMT.txt:**  
[Preview](https://github.com/OMPSHUNYAYA/Symbolic-Mathematical-Temperature/blob/main/CALIBRATION_SSMT.txt) • [Download](https://github.com/OMPSHUNYAYA/Symbolic-Mathematical-Temperature/raw/main/CALIBRATION_SSMT.txt)

**Quickstart demo (PY):**  
[Preview](https://github.com/OMPSHUNYAYA/Symbolic-Mathematical-Temperature/blob/main/ssmt_quickstart.py) • [Download](https://github.com/OMPSHUNYAYA/Symbolic-Mathematical-Temperature/raw/main/ssmt_quickstart.py)

**Verification tests (PY):**  
[Preview](https://github.com/OMPSHUNYAYA/Symbolic-Mathematical-Temperature/blob/main/ssmt_verify.py) • [Download](https://github.com/OMPSHUNYAYA/Symbolic-Mathematical-Temperature/raw/main/ssmt_verify.py)

(Optional) You can keep a `logs/` folder in this repo to attach sample output records for auditing and replay (timestamp, raw reading, `T_K`, `e_T`, `a_phase`, etc.).

## Quick Start

Windows:
python ssmt_quickstart.py

macOS / Linux:
python3 ssmt_quickstart.py

You will get a compact record like:

timestamp_utc: 2025-10-30T09:30:00Z
T_c_human: 25.0
T_K: 298.15
e_T: 0.0
a_phase: 1.0

How to read this:
- `e_T = 0.0` means the sensor reading sits exactly at the declared reference `T_ref` (for example `T_ref = 298.15 K`, about 25 degC comfort baseline).
- `a_phase = 1.0` means "well above the cold-risk threshold," i.e. safely on the warm side of freezing.

This already demonstrates two things:
1) shared reference, not just raw degC/degF, and
2) phase awareness (which side of the safety line, and by how much).


## Verification / CI-style check

Run:
python ssmt_verify.py      (Windows)
python3 ssmt_verify.py     (macOS / Linux)

Expected output ends with:
ALL CHECKS PASSED

This confirms:
- Kelvin floor is always enforced:
  `T_K := max( to_kelvin(T_raw, unit_flag) , eps_TK )`

- Contrast baseline is consistent and monotone:
  `e_T := ln( T_K / T_ref )`
  `e_T` is exactly `0.0` at `T_ref`, positive above, negative below.

- Phase dial stays bounded and signed:
  `a_phase := tanh( c_m * ( (T_K - T_m) / DeltaT_m ) )`
  Values stay in (-1,+1), and negative means "cold side", positive means "warm side".

- Round-trip reproducibility:
  Two sensors that both read the same degC under the same manifest will generate the same `e_T`. That prevents vendors or sites from "gaming" the language.

## License

SSMT is open source and released as an open standard.  
Any organization — public, industrial, municipal, national, academic, commercial, or off-world habitat — may implement it with no registration or fees, provided the formulas are implemented exactly as declared in a published manifest.

Minimum citation requirement:  
When implementing or adapting, cite the concept name "Shunyaya Symbolic Mathematical Temperature (SSMT)" as the origin of the symbolic mathematical temperature approach.

Non-exclusivity:  
No implementer may claim exclusive ownership, stewardship, endorsement, or representation of the standard. There is no central registry or approval flow.

Integrity requirement:  
`e_T`, `a_phase`, `a_phase_fused`, and any pooled or memory-stabilized derivatives (for example `Q_phase`) must preserve their defined meaning.  
If you change formulas (for example, use a different lens than `e_T := ln( T_K / T_ref )`, or redefine how `a_phase` is computed), you must clearly declare that change in your manifest and downstream documentation.

Optional extensions:  
Organizations may add optional layers (for example gating, privacy offsets, or signatures) so long as the core symbolic definitions and baseline formulas remain intact and auditable.

Datasets:  
Any datasets used in examples or demonstrations retain their original licenses and usage terms.

Warranty disclaimer:  
Provided strictly "as-is," observation-only, with no warranty, safety guarantee, or endorsement.  
This does not replace instrument calibration, local safety procedures, engineering judgment, or mandated thresholds.


## Topics

Shunyaya Symbolic Mathematical Temperature (SSMT), symbolic temperature standard, `e_T`, `a_phase`, `a_phase_fused`, `Q_phase`, manifest discipline, auditability, ESG reporting, compliance, safety analytics, open standard, open source.
