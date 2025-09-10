"""Bulk 150 mm rules Gridfinity module."""

import cadquery as cq
from cqgridfinity import GR_BASE_HEIGHT, GRU, GridfinityBox

from .constants import CUTOUT_FILLET_RADIUS, MAX_WALL_THICKNESS
from .cq_containers import CqWorkplaneContainer


class Rules150Bulk(CqWorkplaneContainer):
    """Bulk 150 mm rules Gridfinity module."""

    # Gridfinity box size
    LENGTH_U = 5
    WIDTH_U = 1
    HEIGHT_U = 6

    def __init__(self):
        """Initialize 150 mm rules Gridfinity module."""
        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        """Make 150 mm rules Gridfinity module."""
        finger_cutout_wall_height = 5

        gf_box = GridfinityBox(
            self.LENGTH_U,
            self.WIDTH_U,
            self.HEIGHT_U,
            wall_th=MAX_WALL_THICKNESS,
            width_div=3,
        )

        finger_cutout_length = (self.LENGTH_U - 2) * GRU
        finger_cutout_elevation = GR_BASE_HEIGHT + finger_cutout_wall_height
        finger_cutout_height = gf_box.height - finger_cutout_elevation
        finger_cutout = (
            cq.Workplane(origin=(0, 0, finger_cutout_elevation))
            .box(
                finger_cutout_length,
                gf_box.width,
                finger_cutout_height,
                centered=(True, True, False),
            )
            .edges("(>X and <Z) or (<X and <Z)")
            .fillet(CUTOUT_FILLET_RADIUS)
        )

        part = gf_box.cq_obj - finger_cutout

        return part
