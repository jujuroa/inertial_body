"""
inertial_body_py

High-performance inertial easing core (C++/pybind11)
"""

# low-level extension (private)
from .inertial_body_py import (
    InertialBody as _InertialBody,
    State as _State,
)

# public API aliases
InertialBody = _InertialBody
State = _State

__all__ = [
    "InertialBody",
    "State",
]
