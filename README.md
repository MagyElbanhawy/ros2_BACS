# Ros_after_emSLAM — Bandwidth-Aware Constraint Scheduling (BACS)

Simulation, ROS 2 implementation, physical-robot experiments, and reproducibility artifacts for the paper

> **Bandwidth-Aware Constraint Scheduling for Trust-Weighted Multi-Robot Map
> Fusion under Duty-Cycle-Limited Wireless Links**

Collaborative SLAM over low-power wide-area radio (LoRa, EU868) is usually framed
as a *weighting* problem: constraints arrive late or corrupted, and the fusion
back-end decides how much to believe them. Under a 1% duty-cycle ceiling a
transmitter can send only ~6 constraint packets per minute, while the mapping
front-end produces candidates ~180× faster. The binding question therefore
becomes **which candidate to spend the channel on**, not how to weight the
survivors.

**BACS** moves the trust decision from the receiver to the transmitter. Each
robot predicts the trust score its candidate would receive at the fusion server,
gates on an admissibility threshold, and ranks the admissible candidates by an
information-gain surrogate per unit airtime — solved as a knapsack within each
duty-cycle window in `O(n log n)`. **BACS+** adds an observability term `O_ij = exp(-n_ij / n_ref)` that prioritises under-constrained robot pairs.

---

## Physical Hardware Validation

Physical validation was executed on **two modified AgileX LIMO differential-drive robots** under **Vicon motion capture ground truth** at the New Mansoura University test facility:

- **Platform & Compute**: 2 × LIMO differential-drive platforms, each carrying an EAI T-mini Pro 2D LiDAR, an Orbbec DaBai RGB-D camera, and an Intel NUC i7 onboard computer running Ubuntu 22.04 and ROS 2 Humble.
- **Radio System**: REYAX RYLR998 LoRa transceivers operating at 868 MHz (EU868 g1, SF7, 125 kHz bandwidth, coding rate 4/5, 1% duty-cycle ceiling, $W = 60\text{ s}$).
- **Ground Truth**: Vicon motion capture system (~150 m² indoor laboratory test area).
- **Physical Repetitions**: 10 matched physical runs per policy ($N = 2$).
- **Primary Metric & Headline Result**: BACS+ reduces physical map-alignment RMSE from $0.48 \pm 0.15\text{ m}$ under FIFO to $0.27 \pm 0.09\text{ m}$, a **43.8% improvement** (one-sided paired Wilcoxon $p = 9.77 \times 10^{-4}$, Cliff's $\delta = -0.81$).
- **Queueing Deferral Dominance**: Median scheduling deferral is $154\text{ s}$ versus $0.17\text{ s}$ channel delay (a **906× separation**), confirming that packet staleness under duty-cycle compliance is governed by airtime queueing rather than sub-second radio propagation.

*Note on experimental scope*: Physical experiments evaluate two LIMO robots ($N = 2$). Scalability across larger teams ($N = 3, 4, 5$) is evaluated in the 30-seed simulation study.

---

## Simulation Study ($N = 2 \dots 5$)

The simulation evaluation uses 30 held-out seeds (seeds 10–39) across teams of two to five robots:

- **Primary Metric (Map-Alignment RMSE)**: BACS+ reduces map-alignment error by 21.3% to 48.1% relative to FIFO across two to four robots, and retains a **28.7% reduction** at five robots ($0.183\text{ m}$ vs $0.257\text{ m}$, $p = 7.3 \times 10^{-4}$, Cliff's $\delta = -0.53$).
- **Secondary Metric (Pose RMSE)**: Per-step trajectory pose RMSE is dominated by local odometry drift and shows no statistically significant policy effect across any team size (all paired Wilcoxon $p > 0.11$).
- **Incremental Surrogate Validation (S7-C)**: Validated against exact Jacobian-based incremental information evaluated at scheduling time, the observability-aware surrogate improves rank correlation across all 40 paired runs (median gains of $+0.10$ to $+0.23$, one-sided Wilcoxon $p = 9.8 \times 10^{-4}$).

---

## Repository layout

```
bacs_sim/            simulation package (module layout mirrors the manuscript)
scripts/             reproduce.py (S1-S6) + generate_paper_results.py (BACS+ additions)
tests/               smoke + reproducibility tests
paper_results/       frozen CSVs backing the manuscript tables and hardware metrics
ros2_ws/             ROS 2 scheduler package (bacs_scheduler) deployed on LIMO robots
third_party/          external ROS 2 dependencies (Multi_Robots_ros2, limo_ros2)
hardware/            LoRa radio parameters, hardware logs, and physical test protocol
paper_figures/       generated manuscript figures (scripts/make_figures.py)
```

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# or, to install the package itself (with test extras):
pip install -e ".[test]"
```

Requires Python ≥ 3.9 with NumPy, pandas and SciPy.

## Quick start

```python
from bacs_sim import SimConfig, run, precompute

cfg = SimConfig()
cfg.trust.gamma = 0.003           # calibrated empirical optimum
cfg.scheduler.policy = "bacs_gated"
pre = precompute(cfg)             # share world data across policies
result = run(cfg, precomputed=pre)
print(result.pose_rmse, result.trust_yield)
```

Available policies: `send_all`, `fifo`, `random`, `greedy_trust`, `greedy_info`,
`bacs`, `bacs_gated`, `bacs_plus`.

### BACS+ (Observability-Aware BACS)

`bacs_plus` adds the pairwise observability term `O_ij = exp(-n_ij / n_ref)` to steer airtime toward under-constrained robot pairs, paired with the deferral-derived decay rule ($\gamma = \ln 2 / T_{\text{defer}} \approx 0.0045\text{ s}^{-1}$):

```python
cfg = SimConfig()
cfg.scheduler.policy = "bacs_plus"       # enables the observability term
cfg.trust.gamma_rule = "deferral_derived" # gamma = ln2 / T_defer ~ 0.0045
result = run(cfg, precomputed=precompute(cfg))
```

## Reproducing paper results

```bash
python scripts/reproduce.py                 # baseline scenarios S1-S6
python scripts/generate_paper_results.py   # progression, S7-C, S8 (30-seed), S9
```

| Scenario | What it measures |
|---|---|
| `progression` | EMRMF-original → compliant FIFO → BACS → BACS+ |
| `s7c` | **incremental** Spearman correlation ρ(surrogate, true info) across N = 2..5 |
| `s8` | 30-seed held-out evaluation of map-alignment RMSE and pose RMSE for N = 2..5 |
| `s9` | decay-coefficient rules: drift (Eq. 19) vs deferral-derived (Eq. 20) |

## ROS 2 Scheduler Package

[`ros2_ws/src/bacs_scheduler`](ros2_ws/src/bacs_scheduler) is the ROS 2 node executing BACS scheduling decisions on physical platforms. It was deployed and validated on two modified LIMO differential-drive robots running ROS 2 Humble. See [`hardware/experiment_protocol.md`](hardware/experiment_protocol.md) for full physical configuration parameters.

## Key findings

1. **Physical Validation Confirmations**: BACS+ reduces physical map-alignment RMSE by **43.8%** relative to FIFO ($0.27 \pm 0.09\text{ m}$ vs $0.48 \pm 0.15\text{ m}$, $p = 9.77 \times 10^{-4}$, Cliff's $\delta = -0.81$) and confirms a 906× ratio between scheduling deferral ($154\text{ s}$) and channel delay ($0.17\text{ s}$).
2. **Queueing Deferral Governs Staleness**: Under 1% duty cycle compliance, airtime deferral dominates packet age (~155 s). Radio propagation delays (0.05–0.2 s) are three orders of magnitude smaller and do not govern temporal decay.
3. **Deferral-Derived Decay Correction**: The drift-derived decay rule ($\gamma \approx 0.0333\text{ s}^{-1}$) is falsified. The corrected rule ($\gamma_{\text{defer}} = \ln 2 / T_{\text{defer}} \approx 0.0045\text{ s}^{-1}$) anchors decay to airtime queueing and matches tuned performance without offline sweeps.
4. **Gated Information Ranking**: Trust should act as an admissibility **gate** rather than a multiplicative weight, with admissible candidates ranked by information density.
5. **Observability-Aware Surrogate Fidelity**: Validated against scheduling-time incremental information (S7-C), the local surrogate positively correlates with exact information ($0.45\text{--}0.62$), and `bacs_plus` improves correlation across all evaluated runs ($\Delta \rho = +0.10\text{--}+0.23$).
6. **Metric Separation**: Pose RMSE is dominated by local odometry drift and is policy-insensitive ($p > 0.11$). Map-alignment RMSE measures relative graph consistency and demonstrates significant policy gains ($21\text{--}49\%$ reductions across $N=2..5$).

## Tests

```bash
pytest
```

## Citation

See [`CITATION.cff`](CITATION.cff). Author and venue details are withheld pending double-anonymous review.

## License

MIT — see [`LICENSE`](LICENSE).
