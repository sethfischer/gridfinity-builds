"""Empire EMSSRS Stainless Steel Ruler Stop Gridfinity module."""

import cadquery as cq
from cqgridfinity import GridfinityBox

from gridfinity_builds.constants import FINGER_CUTOUT_DIAMETER, MAX_WALL_THICKNESS
from gridfinity_builds.cq_containers import CqWorkplaneContainer


class EmpireRuleStopEmssrs(CqWorkplaneContainer):
    """Empire EMSSRS Stainless Steel Ruler Stop.

    Brand: Empire
    Model: EMSSRS
    Markings: Empire
    Product page: https://www.empiretools.co.nz/products/rulers/stainless-steel-ruler-stop
    """

    # Gridfinity size
    LENGTH_U = 2
    WIDTH_U = 1
    HEIGHT_U = 6

    def __init__(self):
        """Initialize Empire Stainless Steel Ruler Stop."""
        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        """Make Empire Stainless Steel Ruler Stop Gridfinity module."""

        body_length = 50
        body_width = 20.5
        body_depth = 10.5
        thumb_screw_diameter = 6

        thumb_screw_radius = thumb_screw_diameter / 2
        clearance = 0.5
        solid_ratio = 0.9

        gf_box = GridfinityBox(
            self.LENGTH_U,
            self.WIDTH_U,
            self.HEIGHT_U,
            solid=True,
            solid_ratio=solid_ratio,
            wall_th=MAX_WALL_THICKNESS,
        )

        body_cutout = cq.Workplane().box(
            body_length + clearance,
            body_depth + clearance,
            body_width,
        )

        cutout_total_length = gf_box.inner_l - 1
        adjuster_cutout_length = cutout_total_length - (body_length + clearance)
        adjuster_cutout_height = (body_width / 2) + thumb_screw_radius + clearance

        adjuster_cutout = (
            cq.Workplane()
            .box(
                adjuster_cutout_length,
                body_depth + clearance,
                adjuster_cutout_height,
                centered=(False, True, False),
            )
            .edges("<Z and |X")
            .fillet(thumb_screw_radius + (clearance / 2))
        )

        finger_cutout = (
            cq.Workplane()
            .cylinder(
                body_width,
                FINGER_CUTOUT_DIAMETER / 2,
                centered=(True, True, True),
            )
            .edges("<Z")
            .fillet(FINGER_CUTOUT_DIAMETER / 2)
        )

        # positive Y-axis finger cutout
        finger_cutout_pos = finger_cutout.translate(
            (0, (body_depth + clearance) / 2, 0)
        )
        # negative Y-axis finger cutout
        finger_cutout_neg = finger_cutout.rotate((0, 0, 0), (0, 0, 1), 180).translate(
            (0, -(body_depth + clearance) / 2, 0)
        )

        cutout = (
            body_cutout
            + adjuster_cutout.translate(
                (body_length / 2, 0, -(thumb_screw_radius + clearance))
            )
            + finger_cutout_pos
            + finger_cutout_neg
        )

        bounding_box = cutout.val().BoundingBox()
        bounding_box_center = bounding_box.center

        part = gf_box.cq_obj - cutout.translate(
            (
                -bounding_box_center.x,
                -bounding_box_center.y,
                gf_box.top_ref_height - (body_width / 2),
            )
        )

        return part
