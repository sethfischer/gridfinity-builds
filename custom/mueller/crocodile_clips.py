"""Mueller Crocodile Clips."""

import cadquery as cq
from cqgridfinity import GridfinityBox

from custom.cq_containers import CqWorkplaneContainer


class MuellerBU27259(CqWorkplaneContainer):
    """Mueller BU-27.259.@ Safety Alligator Clip

    Brand: Mueller
    """

    # Gridfinity box size
    LENGTH_U = 1
    WIDTH_U = 1
    HEIGHT_U = 3

    def __init__(self):
        """Mueller BU-27.259.@ Safety Alligator Clip."""
        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        """Make Mueller BU-27.259.@ Gridfinity module."""
        # dimensions
        diameter = 9.85
        distance_to_push_button = 18

        clearance = 0.5
        solid_ratio = 1

        gf_box = GridfinityBox(
            self.LENGTH_U,
            self.WIDTH_U,
            self.HEIGHT_U,
            solid=True,
            solid_ratio=solid_ratio,
        )

        aperture_diameter = diameter + clearance
        aperture_radius = aperture_diameter / 2

        aperture_spacing = 8.5

        aperture_locations = [
            (aperture_spacing, aperture_spacing),
            (-aperture_spacing, aperture_spacing),
            (aperture_spacing, -aperture_spacing),
            (-aperture_spacing, -aperture_spacing),
        ]

        cutout = (
            cq.Workplane(origin=(0, 0, gf_box.top_ref_height))
            .pushPoints(aperture_locations)
            .circle(aperture_radius)
            .extrude(-distance_to_push_button + 3)
        )

        part = gf_box.cq_obj - cutout

        return part
