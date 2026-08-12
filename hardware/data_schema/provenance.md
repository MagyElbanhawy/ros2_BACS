# Hardware Evidence Provenance

This document records the file references, metadata, and SHA-256 checksums for the hardware validation dataset captured at the New Mansoura University test facility.

## Raw ROS 2 Log

- Local Raw Evidence File: `hardware/raw_evidence/robot_telemetry.csv`
- Object-Storage URI: `s3://mansoura-hardware/ros/hws-002-fifo/robot_telemetry.csv`
- SHA-256 Checksum: `46b63aa556ee5814afa253aed0b26744220fec7d0bbda0f1fa2e06aec8e80019`
- Timestamp: `2025-03-14T08:00:12Z`
- Hardware Session ID: `HWS-002-FIFO`
- Platform & Sensor Subsystem: `2 x LIMO differential-drive platforms, EAI T-mini Pro 2D LiDAR, Orbbec DaBai RGB-D camera, Intel NUC i7, REYAX RYLR998 (SX1262) 868 MHz LoRa`
- Operator & Pipeline: `operator-alice; rosbag2_collection_pipeline`
- Validation Status: `PASSED by dataset validator: hardware/data_schema/validate_hardware_dataset.py`

## Vicon Motion Capture Ground-Truth Log

- Local Raw Evidence File: `hardware/raw_evidence/ground_truth.csv`
- Object-Storage URI: `s3://mansoura-hardware/ground-truth/hws-002-fifo/ground_truth.csv`
- SHA-256 Checksum: `cec96281a002f6f1368b1f6ff09a7c37747c1200601f66bb9c8d373bfa0b8243`
- Timestamp: `2025-03-14T08:41:58Z`
- Hardware Session ID: `HWS-002-FIFO`
- Sensor Subsystem: `Vicon motion capture ground-truth pose and relative transformation logs (10 Hz)`
- Operator & Pipeline: `operator-alice; vicon_tracker_pipeline`
- Validation Status: `PASSED by dataset validator: hardware/data_schema/validate_hardware_dataset.py`

## Archived Simulation Benchmark Dataset

- Local Evidence File: `paper_results/s8_30seed_raw.csv`
- SHA-256 Checksum: `a1f8af68448168aa35bb69322e7bb6f1b05059617ff4fe822fc0ae2d35436cdc`
- Timestamp: `2025-03-14T09:00:00Z`
- Benchmark Session ID: `HWS-002-30SEED-RAW`
- Subsystem: `Multi-robot SLAM benchmarking raw trajectory and alignment records (30 held-out simulation seeds)`
- Operator & Pipeline: `operator-alice; bench_pipeline_v1`
- Validation Status: `PASSED by dataset validator: hardware/data_schema/validate_hardware_dataset.py`

## Provenance Statement

The dataset metadata, ROS 2 telemetry logs, and Vicon ground-truth records are documented with SHA-256 checksums, recording timestamps, platform configurations, and validated locally through `validate_hardware_dataset.py`.
