"""Eye loupe Gridfinity module."""

import cadquery as cq
from cqgridfinity import GR_BASE_HEIGHT, GRU, GridfinityBox

from .constants import TINY_LENGTH
from .cq_containers import CqWorkplaneContainer


class EyeLoupe40(CqWorkplaneContainer):
    """Eye loupe.

    Brand: Unknown
    Markings: 2½ JAPAN
    """

    # Gridfinity box size
    LENGTH_U = 1
    WIDTH_U = 1
    HEIGHT_U = 6

    def __init__(self):
        """Initialize Eye loupe."""
        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        """Make Eye loupe Gridfinity module."""
        # Eye loupe dimensions
        diameter = 40
        height = 29

        diameter_clearance = 0.5
        height_clearance = 3  # distance between object and stacked bin
        cutout_diameter = 24
        cutout_fillet = 6
        shadow_diameter = 34
        shadow_height = 2

        solid_ratio = 1

        gf_box = GridfinityBox(
            self.LENGTH_U,
            self.WIDTH_U,
            self.HEIGHT_U,
            solid=True,
            solid_ratio=solid_ratio,
        )

        floor_elevation = gf_box.top_ref_height - height - height_clearance
        offset = gf_box.top_ref_height - GR_BASE_HEIGHT - height - height_clearance
        cutout_height = gf_box.height

        finger_cutout = (
            cq.Workplane("XY")
            .workplane(offset=offset)
            .rect(GRU + (cutout_fillet * 2), cutout_diameter)
            .extrude(cutout_height)
            .edges("<Z")
            .fillet(cutout_fillet)
        )

        cutout = (
            cq.Workplane()
            .workplane(offset=offset)
            .circle((diameter + diameter_clearance) / 2)
            .extrude(cutout_height)
            .union(finger_cutout)
            .union(finger_cutout.rotate((0, 0, 0), (0, 0, 1), 90))
        )

        shadow = (
            cq.Workplane()
            .workplane(offset=floor_elevation)
            .circle(shadow_diameter / 2)
            .extrude(shadow_height)
            .faces(">Z")
            .edges("%circle")
            .chamfer(shadow_height - TINY_LENGTH)
        )

        part = gf_box.cq_obj - cutout.translate((0, 0, GR_BASE_HEIGHT)) + shadow

        return part
