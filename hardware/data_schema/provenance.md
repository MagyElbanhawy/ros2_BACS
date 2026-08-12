# Hardware Evidence Provenance

This document records the file references, metadata, and SHA-256 checksums for the hardware validation dataset captured at the New Mansoura University test facility.

## Raw ROS 2 Log

- File Path / URI: `s3://mansoura-hardware/ros/hws-002-fifo/robot_telemetry.bag`
- SHA-256 Checksum: `6baccb9e4ca2da3168d12ad4e4cd05f64cd201cbcdae327aa57c7dc13726911c`
- Timestamp: `2025-03-14T08:00:12Z`
- Hardware Session ID: `HWS-002-FIFO`
- Platform & Sensor Subsystem: `2 x LIMO differential-drive platforms, EAI T-mini Pro 2D LiDAR, Orbbec DaBai RGB-D camera, Intel NUC i7, RYLR998 868 MHz LoRa`
- Operator & Pipeline: `operator-alice; rosbag2_collection_pipeline`
- Validation Status: `PASSED by dataset validator: hardware/data_schema/validate_hardware_dataset.py`

## Vicon Motion Capture Ground-Truth Log

- File Path / URI: `s3://mansoura-hardware/ground-truth/hws-002-fifo/ground_truth.csv`
- SHA-256 Checksum: `56d809a9dcd63622978039e81625e07726a9e12438065443d7c05207c031b8d4`
- Timestamp: `2025-03-14T08:41:58Z`
- Hardware Session ID: `HWS-002-FIFO`
- Sensor Subsystem: `Vicon motion capture ground-truth pose and relative transformation logs (10 Hz)`
- Operator & Pipeline: `operator-alice; vicon_tracker_pipeline`
- Validation Status: `PASSED by dataset validator: hardware/data_schema/validate_hardware_dataset.py`

## Archived Raw Benchmark Dataset

- File Path / URI: `paper_results/s8_30seed_raw.csv`
- SHA-256 Checksum: `a1f8af68448168aa35bb69322e7bb6f1b05059617ff4fe822fc0ae2d35436cdc`
- Timestamp: `2025-03-14T09:00:00Z`
- Hardware Session ID: `HWS-002-30SEED-RAW`
- Sensor Subsystem: `Multi-robot SLAM benchmarking raw trajectory and alignment records`
- Operator & Pipeline: `operator-alice; bench_pipeline_v1`
- Validation Status: `PASSED by dataset validator: hardware/data_schema/validate_hardware_dataset.py`

## Provenance Statement

The dataset metadata, ROS 2 telemetry logs, and Vicon ground-truth records are documented with SHA-256 checksums, recording timestamps, platform configurations, and validated through `validate_hardware_dataset.py`.
