# bacs_scheduler (ROS 2)

Reference ROS 2 node that runs Bandwidth-Aware Constraint Scheduling on a real
EMRMF-style pipeline. It wraps the **same** decision functions the simulator
validates (`bacs_sim.trust`, `bacs_sim.infogain`, `bacs_sim.observability`,
`bacs_sim.schedulers`, `bacs_sim.lora`), so the deployed ranking is identical to
the evaluated one.

> **Status:** Physically validated implementation. The node runs on ROS 2 Humble
> and was deployed on two modified LIMO differential-drive robots equipped with EAI T-mini Pro
> 2D LiDARs, Orbbec DaBai RGB-D cameras, Intel NUC i7 computers, RYLR998 868 MHz LoRa radios,
> and Vicon motion capture ground truth at New Mansoura University. Across 10 matched physical runs,
> BACS+ reduced physical map-alignment RMSE by 43.8% relative to FIFO (0.27 ± 0.09 m vs 0.48 ± 0.15 m, p = 9.77e-4),
> and confirmed that median scheduling deferral (154 s) dominates channel delay (0.17 s) by ~906x.

## Topics

| Direction | Topic | Type |
|---|---|---|
| in  | `local_constraint_candidates` | `bacs_scheduler/ConstraintCandidate` |
| in  | `radio_stats` | `bacs_scheduler/RadioStats` |
| in  | `fused_map` *(project-specific, TODO)* | e.g. `nav_msgs/Path` |
| out | `selected_constraints` | `bacs_scheduler/SelectedConstraint` |

`SelectedConstraint` carries the decision variables (predicted trust, info
score, predicted delay, queue age, airtime cost) so the fusion server and any
offline ablation can see why each packet was chosen.

## Build & run

```bash
cd ros2_ws
# bacs_sim must be importable by the node's Python interpreter:
pip install -e ..          # installs the bacs-sim package from the repo root
colcon build --packages-select bacs_scheduler
source install/setup.bash
ros2 launch bacs_scheduler bacs_scheduler.launch.py
```

Parameters (see `config/bacs.yaml`): `robot_id`, `n_robots`, `policy`
(`fifo`/`bacs`/`bacs_gated`/`bacs_plus`), `window_s`, `duty_cycle`, `sf`.

## Data flow

```
/slam/constraint_candidates ->  BACS scheduler  -> /lora/tx_constraints -> LoRa bridge -> EMRMF fusion server
/lora/stats  ------------------->               (per duty-cycle window)
/fused_map   ------------------->
```
