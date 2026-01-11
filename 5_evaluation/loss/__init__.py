"""
Loss functions for AdEx parameter optimization.

This package provides:
- mse: Mean squared error based losses (voltage trace, spike timing)
- guarino: Feature-based loss from Guarino et al. (2025)
"""

from .guarino import (
    GuarinoFeatures,
    GuarinoFeatureExtractor,
    GuarinoLossConfig,
    guarino_loss,
    relative_error,
    extract_experimental_features,
    make_guarino_loss_fn,
)

from .mse import (
    MSELossConfig,
    mse_loss,
    make_mse_loss_fn,
)

__all__ = [
    # MSE losses
    "MSELossConfig",
    "mse_loss",
    "make_mse_loss_fn",

    # Guarino losses
    "GuarinoFeatures",
    "GuarinoFeatureExtractor",
    "GuarinoLossConfig",
    "guarino_loss",
    "relative_error",
    "extract_experimental_features",
    "make_guarino_loss_fn",
]
