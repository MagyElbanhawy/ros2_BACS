# Third-party ROS references

This directory keeps external ROS 2 resources used as reference stacks or integration inputs for the current project.

## Included repositories

- `Multi_Robots_ros2` — multi-robot ROS 2 reference stack from MagyElbanhawy.
- `limo_ros2` — AgileX LIMO robot ROS 2 packages for hardware and control integration.

## Purpose

These repositories are kept separate from the main project source tree so the active research code remains reproducible and well-structured while still retaining the upstream hardware and multi-robot references needed for deployment or integration work.

## Usage

- Inspect platform-specific launch files, robot drivers, and Python scripts where the project needs a real-world ROS 2 hardware reference.
- Keep deployment logic in the main workspace (`ros2_ws/`) and use these repos as reference packages when needed.
