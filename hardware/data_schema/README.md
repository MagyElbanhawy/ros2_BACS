# Hardware evidence and verification

This directory contains the archived evidence for the physical hardware comparison
run at New Mansoura University, Mansoura, Egypt. The authoritative summary is
`reported_hardware_summary.csv`, and the underlying evidence is the raw ROS 2 logs,
Vicon motion capture ground-truth records, calibration log, session manifests, and
provenance metadata.

Run:
- `python hardware/data_schema/validate_hardware_dataset.py`
- `python hardware/data_schema/validate_hardware_dataset.py --validate-synthetic`
  only for synthetic fixture validation.

## Required files

- `calibration_log.csv`
- `session_manifest.csv`
- `session_metrics.csv`
- `reported_hardware_summary.csv`
- `provenance.md`
- `raw_evidence_provenance.md`
- `validator_output.txt`

## Verification levels

- **RAW-VERIFIED** requires genuine, log-backed session manifests and metrics,
  together with provenance identifying the original ROS and ground-truth logs,
  a SHA-256 checksum for each raw log, the recording timestamps, hardware
  session identifiers, sensor/subsystem names, operator identity, and an
  independent validator status.
- **SUMMARY-VERIFIED** means the archived hardware summary is internally
  consistent without claiming raw reproducibility.
- **SYNTHETIC-TEST-DATA-ONLY** is allowed only in separately named synthetic_*
  fixtures and is never accepted as physical evidence.
