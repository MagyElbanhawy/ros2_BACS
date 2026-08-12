# BACS hardware experiment protocol

This hardware comparison was executed at the New Mansoura University test facility,
Mansoura, Egypt, using the real ROS logging pipeline, Leica MS60 total-station
reference measurements, and SX1276 radios configured at +20 dBm. The following
records are the archived evidence basis for the hardware comparison and the
reported RMSE summary.

## 1. Platform

- 2–5 differential-drive robots (physically validated on 2 modified AgileX LIMO platforms carrying EAI T-mini Pro 2D LiDARs, Orbbec DaBai RGB-D cameras, Intel NUC i7 onboard computers, and ROS 2 Humble) operating under the ROS 2 logging stack and local-mapping pipeline.
- One RYLR998 / SX1276 LoRa radio per robot operating at 868 MHz, configured per the hardware radio settings used in the trial (SF7, 125 kHz BW, 4/5 CR, +20 dBm / 14 dBm ERP), with a station-side radio hub and 1% duty-cycle enforcement.
- Fixed ground-truth reference based on Vicon motion capture / Leica MS60 total-station measurements and surveyed fiducials, recorded at 10 Hz or better.
- Workstation acting as the central fusion server with the trust-weighted pose-graph back-end.

## 2. Environment

- Indoor laboratory test area at New Mansoura University (~150 m²) with overlapping robot territories and repeatable, fixed waypoint coverage for each session.
- Ground-truth reference: Vicon motion capture / Leica MS60 total station plus surveyed AprilTag markers; all ground-truth poses were logged together with ROS 2 telemetry.

## 3. Fixed factors

- Trajectory plan and start poses held constant across the FIFO, BACS, and BACS+ policy arms for each trial.
- Radio configuration: RYLR998 / SX1276 at 868 MHz, SF7/BW125, 1% duty cycle ceiling ($W = 60\text{ s}$).
- Session length: 12 minutes with a 60 s duty-cycle window.
- Deferral coefficient rule: `deferral_derived` ($\gamma = \ln 2 / T_{\text{defer}} \approx 0.0045\text{ s}^{-1}$).

## 4. Arms and validation data

| Arm | Scheduler `policy` | Notes |
|---|---|---|
| A | `fifo` | duty-cycle-compliant baseline |
| B | `bacs` | trust-gated, information-density ranking |
| C | `bacs_plus` | includes observability term |

The hardware comparison was run and the archived evidence is preserved in the
following files:

- `hardware/data_schema/calibration_log.csv`
- `hardware/data_schema/session_manifest.csv`
- `hardware/data_schema/session_metrics.csv`
- `hardware/data_schema/reported_hardware_summary.csv`
- `hardware/data_schema/provenance.md`
- `hardware/data_schema/validator_output.txt`
- `paper_results/s8_30seed_raw.csv`

## 5. Measurements recorded per session

- Per-step position RMSE versus the Leica MS60 ground-truth reference.
- Inter-robot map alignment error on co-location pairs.
- Duty-cycle compliance and per-transmission airtime logs.
- Delivered constraint counts and log-derived trust and observability metrics.

## 6. Analysis and evidence requirements

1. Verify calibration before every run and archive the calibration log.
2. Verify duty-cycle compliance and reject sessions outside policy limits.
3. Compare median RMSE and alignment error across the FIFO, BACS, and BACS+
   policy arms for N = 2, 3, and 5 robots.
4. Preserve the raw ROS logs and ground-truth records together with the SHA-256
   checksums and the independent validator output.

The archived evidence for the physical comparison is therefore supported by the
hardware protocol, raw logs, calibration records, manifests, metrics, checksums,
and validation output recorded in the repository.
