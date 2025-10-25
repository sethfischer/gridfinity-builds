"""Abstract base classes for CadQuery object containers."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict

import cadquery as cq
from cqkit import export_step_file


class CqSketchContainer(ABC):
    """Abstract base class for CadQuery Sketch containers."""

    _cq_object: cq.Sketch

    @property
    def cq_object(self) -> cq.Sketch:
        """Get CadQuery object."""
        return self._cq_object

    @abstractmethod
    def _make(self) -> cq.Sketch:
        """Create CadQuery object."""
        ...


class CqWorkplaneContainer(ABC):
    """Abstract base class for CadQuery Workplane containers."""

    _cq_object: cq.Workplane
    _cq_objects: Dict[str, cq.Workplane]

    @property
    def cq_object(self) -> cq.Workplane:
        """Get CadQuery object."""
        return self._cq_object

    @property
    def cq_objects(self) -> Dict[str, cq.Workplane]:
        """Get CadQuery object."""
        return self._cq_objects

    def save_step_file(self, filename: Path):
        """Save STEP file."""
        export_step_file(self.cq_object, filename.as_posix())

    @abstractmethod
    def _make(self) -> cq.Workplane:
        """Create CadQuery object."""
        ...
