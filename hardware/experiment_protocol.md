# BACS Physical Hardware Experiment Protocol

This document specifies the physical validation protocol executed at the New Mansoura University test facility, Mansoura, Egypt.

## 1. Physical Platform & Sensors

- **Robots**: Two (2) modified AgileX LIMO differential-drive robot platforms.
- **Sensors**: EAI T-mini Pro 2D LiDAR (front chassis) and Orbbec DaBai RGB-D camera.
- **Compute & OS**: Intel NUC i7 onboard computer per robot, running Ubuntu 22.04 LTS and ROS 2 Humble.
- **Radio Modules**: REYAX RYLR998 (SX1262) LoRa transceivers operating at 868.1 MHz (EU868 g1 sub-band), configured at SF7, 125 kHz bandwidth, coding rate 4/5, 8 preamble symbols, explicit header with CRC, and 14 dBm transmit power (25 mW ERP ceiling).
- **Ground Truth Reference**: Vicon motion capture system operating at $\ge 10\text{ Hz}$ across an indoor laboratory test area (~150 m²).
- **Central Fusion Server**: Workstation running the trust-weighted pose-graph back-end and local mapping feedback hub.

## 2. Experimental Design & Scope

- **Physical Validation Scope ($N = 2$)**: Evaluated across ten (10) matched physical runs per policy on two LIMO robots traversing repeatable, overlapping trajectory schedules.
- **Simulation Scalability Scope ($N = 3 \dots 5$)**: Multi-robot scalability for teams of 3 to 5 robots is evaluated in the 30-seed simulation study (`paper_results/s8_30seed_raw.csv`).
- **Fixed Operating Factors**:
  - Trajectory waypoints and start poses held constant across FIFO, BACS, and BACS+ arms.
  - Radio configuration: 868.1 MHz, SF7/BW125, 1% duty-cycle ceiling ($W = 60\text{ s}$).
  - Session duration: 12 minutes with 60 s duty-cycle scheduling windows.
  - Temporal trust decay rule: `deferral_derived` ($\gamma = \ln 2 / T_{\text{defer}} \approx 0.0045\text{ s}^{-1}$).

## 3. Policy Arms

| Arm | Scheduler Policy | Description |
|---|---|---|
| A | `fifo` | Duty-cycle-compliant FIFO queueing baseline |
| B | `bacs` | Trust-gated, information-density ranking |
| C | `bacs_plus` | BACS with pairwise observability prioritization ($w_o = 0.30, n_{\text{ref}} = 6$) |

## 4. Logged Measurements

- **Vicon Ground Truth Map Alignment**: Relative map-alignment RMSE over ground-truth co-location pairs.
- **Trajectory Error**: Per-robot, per-step position RMSE against Vicon ground-truth poses.
- **Communication Timescales**: Packet generation time, scheduling deferral $T_{\text{defer}}$, channel airtime $T_{\text{air}}$, and end-to-end latency.
- **Scheduler Diagnostics**: Delivered constraint count, airtime utilization, server-side trust yield, and scheduler decision overhead.

## 5. Summary of Physical Results ($N = 2$)

 Across ten matched physical runs per policy:
 - **FIFO**: Map-alignment RMSE = $0.48 \pm 0.15\text{ m}$ (95% CI: $[0.37, 0.59]\text{ m}$).
 - **BACS**: Map-alignment RMSE = $0.28 \pm 0.08\text{ m}$ (95% CI: $[0.22, 0.34]\text{ m}$).
 - **BACS+**: Map-alignment RMSE = $0.27 \pm 0.09\text{ m}$ (95% CI: $[0.20, 0.34]\text{ m}$), a **43.8% reduction** relative to FIFO ($p = 9.77 \times 10^{-4}$, Cliff's $\delta = -0.81$).
 - **Deferral Dominance**: Median packet age under BACS+ is $155\text{ s}$ ($154\text{ s}$ scheduling deferral vs $0.17\text{ s}$ channel delay, a $906\times$ ratio).
