"""
Refiners package for iterative text improvement.

This package provides tools for refining text outputs based on feedback from judges.
The main component is the `Refiner` class, which can be used to iteratively
improve text based on specific feedback.
"""

from .base_refiner import Refiner

__all__ = ['Refiner']
