#!/usr/bin/env python3
"""Validate the physical hardware evidence archive."""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUMMARY = ROOT / "reported_hardware_summary.csv"
MANIFEST = ROOT / "session_manifest.csv"
METRICS = ROOT / "session_metrics.csv"
CALIBRATION = ROOT / "calibration_log.csv"
PROVENANCE_CANDIDATES = [ROOT / "provenance.md", ROOT / "raw_evidence_provenance.md"]
EXPECTED_SUMMARY = {
    "record_type",
    "metric_name",
    "team_size",
    "policy",
    "mean_value",
    "std_dev",
    "unit",
    "manuscript_table",
}


def read_csv(path: Path):
    if not path.exists():
        return [], []
    with path.open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def get_provenance_text() -> str:
    for path in PROVENANCE_CANDIDATES:
        if path.exists():
            return path.read_text(encoding='utf-8')
    raise ValueError('provenance.md or raw_evidence_provenance.md is missing')


def ensure_file(path: Path, label: str):
    if not path.exists():
        raise ValueError(f'{label} is missing: {path.name}')


def validate_calibration():
    ensure_file(CALIBRATION, 'calibration log')
    fields, rows = read_csv(CALIBRATION)
    if not rows:
        raise ValueError('calibration_log.csv is empty')
    required = {'calibration_id', 'device_id', 'calibration_time_utc', 'reference', 'validator_status'}
    missing = required - set(fields)
    if missing:
        raise ValueError(f'calibration log missing columns: {sorted(missing)}')
    if any(row.get('validator_status', '').strip().lower() != 'validated' for row in rows):
        raise ValueError('every calibration row must be validated')


def validate_summary():
    ensure_file(SUMMARY, 'summary')
    fields, rows = read_csv(SUMMARY)
    if not rows:
        raise ValueError('reported_hardware_summary.csv is empty')
    missing = EXPECTED_SUMMARY - set(fields)
    if missing:
        raise ValueError('summary missing columns: ' + ', '.join(sorted(missing)))
    if any(row['record_type'] != 'reported_summary' for row in rows):
        raise ValueError('summary records must use record_type=reported_summary')
    for metric in ('map_alignment_rmse', 'pose_rmse'):
        subset = [r for r in rows if r['metric_name'] == metric]
        if {r['team_size'] for r in subset} != {'2', '3', '5'}:
            raise ValueError(f'{metric} must include teams 2, 3, and 5')
        if {r['policy'] for r in subset} != {'FIFO', 'BACS', 'BACS+'}:
            raise ValueError(f'{metric} must include FIFO, BACS, and BACS+')
        for row in subset:
            try:
                mean = float(row['mean_value'])
                std = float(row['std_dev'])
            except (KeyError, TypeError, ValueError):
                raise ValueError(f'invalid numeric value in {metric}: {row}')
            if not (0 < mean < 100 and 0 <= std < 100):
                raise ValueError(f'implausible {metric} values: {row}')
    return rows


def validate_manifest_and_metrics():
    ensure_file(MANIFEST, 'session manifest')
    ensure_file(METRICS, 'session metrics')
    manifest_fields, manifest_rows = read_csv(MANIFEST)
    metric_fields, metric_rows = read_csv(METRICS)
    if not manifest_rows or not metric_rows:
        raise ValueError('raw manifests and metrics must not be empty')
    required_manifest = {'session_id', 'policy', 'team_size', 'hardware_session_id', 'site'}
    required_metrics = {'session_id', 'team_size', 'policy', 'map_alignment_rmse_m', 'pose_rmse_m'}
    if not required_manifest.issubset(manifest_fields):
        raise ValueError('session manifest missing required fields')
    if not required_metrics.issubset(metric_fields):
        raise ValueError('session metrics missing required fields')
    session_ids = {row['session_id'] for row in manifest_rows}
    metric_ids = {row['session_id'] for row in metric_rows}
    if not session_ids or not metric_ids:
        raise ValueError('manifest and metrics must contain session IDs')
    if not metric_ids.issubset(session_ids):
        raise ValueError('metrics contain session IDs not in the manifest')
    for row in metric_rows:
        for key in ('map_alignment_rmse_m', 'pose_rmse_m'):
            try:
                float(row[key])
            except (KeyError, TypeError, ValueError):
                raise ValueError(f'invalid metric value for {row.get("session_id")}: {key}')


def validate_provenance():
    text = get_provenance_text().lower()
    required_core = [
        'original raw log file path or object-storage uri',
        'sha-256 checksum',
        'recording timestamp',
        'hardware session identifier',
        'sensor or subsystem',
        'operator or automated pipeline identity',
        'verification status',
        'independent validator',
        'genuine log-backed',
        'ros',
        'ground-truth',
        'new mansoura university',
    ]
    missing = [item for item in required_core if item not in text]
    if missing:
        raise ValueError('provenance is missing required evidence fields: ' + ', '.join(missing))
    sha_matches = re.findall(r'[0-9a-fA-F]{64}', get_provenance_text())
    if len(sha_matches) < 2:
        raise ValueError('provenance must include SHA-256 checksums for each raw log referenced')
    if 'synthetic' in text or 'simulated' in text or 'reconstructed' in text or 'imputed' in text or 'randomly sampled' in text:
        raise ValueError('provenance identifies non-genuine data')


def validate_raw_aggregation(summary_rows):
    _, manifest_rows = read_csv(MANIFEST)
    _, metric_rows = read_csv(METRICS)
    policy_by_session = {row['session_id']: row['policy'] for row in manifest_rows}
    samples = {}
    for row in metric_rows:
        sid = row['session_id']
        policy = policy_by_session.get(sid)
        if policy is None:
            raise ValueError(f'metric session {sid} is not present in the manifest')
        team = row['team_size']
        samples.setdefault(('map_alignment_rmse', team, policy), []).append(float(row['map_alignment_rmse_m']))
        samples.setdefault(('pose_rmse', team, policy), []).append(float(row['pose_rmse_m']))
    for row in summary_rows:
        key = (row['metric_name'], row['team_size'], row['policy'])
        if key[0] not in {'map_alignment_rmse', 'pose_rmse'}:
            continue
        values = samples.get(key, [])
        if not values:
            raise ValueError(f'raw evidence lacks samples for {key}')
        observed = sum(values) / len(values)
        expected = float(row['mean_value'])
        if abs(observed - expected) > max(0.001, expected * 0.05):
            raise ValueError(f'raw mean disagrees with reported summary for {key}')


def main():
    try:
        validate_calibration()
        summary_rows = validate_summary()
        validate_manifest_and_metrics()
        validate_provenance()
        validate_raw_aggregation(summary_rows)
        print('RAW-VERIFIED:')
        print('Original session manifests and metrics are present.')
        print('Raw records aggregate consistently with reported_hardware_summary.csv.')
        return 0
    except ValueError as exc:
        print(f'INVALID: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
