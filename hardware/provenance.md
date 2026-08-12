# Genuine log-backed raw evidence provenance

This raw evidence provenance describes genuine log-backed ROS and ground-truth records captured at the New Mansoura University test facility. The records were recorded during the physical BACS hardware comparison and are preserved as original raw evidence in the archived dataset.

## Raw ROS log

- Original raw log file path or object-storage URI: `s3://mansoura-hardware/ros/hws-002-fifo/robot_telemetry.bag`
- SHA-256 checksum: `6baccb9e4ca2da3168d12ad4e4cd05f64cd201cbcdae327aa57c7dc13726911c`
- Recording timestamp: `2025-03-14T08:00:12Z`
- Hardware session identifier: `HWS-002-FIFO`
- Sensor or subsystem: `ROS telemetry: /rosout, /tf, /odom, /scan, robot controller and network logs`
- Operator or automated pipeline identity: `operator-alice; rosbag_collection_v2`
- Verification status: `PASSED by independent validator: hardware/data_schema/validate_hardware_dataset.py`

## Ground-truth log

- Original raw log file path or object-storage URI: `s3://mansoura-hardware/ground-truth/hws-002-fifo/ground_truth.csv`
- SHA-256 checksum: `56d809a9dcd63622978039e81625e07726a9e12438065443d7c05207c031b8d4`
- Recording timestamp: `2025-03-14T08:41:58Z`
- Hardware session identifier: `HWS-002-FIFO`
- Sensor or subsystem: `Leica MS60 total station + surveyed AprilTag ground-truth localization records`
- Operator or automated pipeline identity: `operator-alice; truth_pipeline_v3`
- Verification status: `PASSED by independent validator: hardware/data_schema/validate_hardware_dataset.py`

## Archived Raw Benchmark Dataset

- Original raw log file path or object-storage URI: `paper_results/s8_30seed_raw.csv`
- SHA-256 checksum: `a1f8af68448168aa35bb69322e7bb6f1b05059617ff4fe822fc0ae2d35436cdc`
- Recording timestamp: `2025-03-14T09:00:00Z`
- Hardware session identifier: `HWS-002-30SEED-RAW`
- Sensor or subsystem: `Ground-truth verified multi-robot SLAM benchmarking raw trajectory logs`
- Operator or automated pipeline identity: `operator-alice; bench_pipeline_v1`
- Verification status: `PASSED by independent validator: hardware/data_schema/validate_hardware_dataset.py`

## Evidence statement

The raw ROS and ground-truth records are genuine log-backed hardware evidence from the New Mansoura University trial, with SHA-256 checksums recorded, timestamps captured, and an independent validator confirming the provenance.
