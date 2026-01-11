"""
Core modules for AdEx simulation and evaluation.

This package provides the foundational components:
- simulation: AdEx simulation in Jaxley and Brian2
- data: Experimental data loading and preprocessing
- parameters: Standard parameter sets
"""

from .simulation import (
    SimulationResult,
    SurrogateType,
    geometry_for_capacitance,
    create_adex_cell,
    simulate_jaxley,
    simulate_brian2,
    simulate_with_current_trace,
)

from .data import (
    TraceData,
    detect_spikes,
    find_stim_window,
    load_trace,
    load_multiple_traces,
    crop_to_stim_window,
)

from .parameters import (
    AdExParams,
    ParamBounds,
    NAUD_PARAMETERS,
    DEFAULT_PARAMS,
    PARAM_BOUNDS,
    DATA_PATHS,
    clip_params,
    convert_trainable_to_params,
    params_to_trainable_format,
)

__all__ = [
    # simulation
    "SimulationResult",
    "SurrogateType",
    "geometry_for_capacitance",
    "create_adex_cell",
    "simulate_jaxley",
    "simulate_brian2",
    "simulate_with_current_trace",
    # data
    "TraceData",
    "detect_spikes",
    "find_stim_window",
    "load_trace",
    "load_multiple_traces",
    "crop_to_stim_window",
    # parameters
    "AdExParams",
    "ParamBounds",
    "NAUD_PARAMETERS",
    "DEFAULT_PARAMS",
    "PARAM_BOUNDS",
    "DATA_PATHS",
    "clip_params",
    "convert_trainable_to_params",
    "params_to_trainable_format",
]
