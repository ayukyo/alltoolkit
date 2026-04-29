"""
Probability Distribution Utilities

A comprehensive library for probability distributions with zero external dependencies.
"""

from .probability_distribution_utils import (
    # Distribution classes
    Distribution,
    NormalDistribution,
    UniformDistribution,
    ExponentialDistribution,
    PoissonDistribution,
    BinomialDistribution,
    GeometricDistribution,
    ChiSquareDistribution,
    StudentTDistribution,
    BetaDistribution,
    GammaDistribution,
    FDistribution,
    WeibullDistribution,
    LogNormalDistribution,
    # Convenience functions
    normal_pdf,
    normal_cdf,
    normal_quantile,
    normal_sample,
    confidence_interval,
    z_score,
    p_value_one_tailed,
    p_value_two_tailed,
    # Statistical tests
    z_test,
    t_test,
    # Helper functions
    _factorial,
    _gamma_function,
    _beta_function,
    _erf,
)

__version__ = '1.0.0'
__author__ = 'AllToolkit'

__all__ = [
    'Distribution',
    'NormalDistribution',
    'UniformDistribution',
    'ExponentialDistribution',
    'PoissonDistribution',
    'BinomialDistribution',
    'GeometricDistribution',
    'ChiSquareDistribution',
    'StudentTDistribution',
    'BetaDistribution',
    'GammaDistribution',
    'FDistribution',
    'WeibullDistribution',
    'LogNormalDistribution',
    'normal_pdf',
    'normal_cdf',
    'normal_quantile',
    'normal_sample',
    'confidence_interval',
    'z_score',
    'p_value_one_tailed',
    'p_value_two_tailed',
    'z_test',
    't_test',
    '_factorial',
    '_gamma_function',
    '_beta_function',
    '_erf',
]