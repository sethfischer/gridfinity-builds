"""Gridfinity for Wiha."""

import cadquery as cq
from cqgridfinity import GR_BASE_HEIGHT, GridfinityBox

from .cq_containers import CqWorkplaneContainer


class Wiha40010Horizontal(CqWorkplaneContainer):
    """Wiha 400 10 magnetizer."""

    # Gridfinity box size
    LENGTH_U = 2
    WIDTH_U = 2
    HEIGHT_U = 6

    def __init__(self):
        """Initialize Wiha40010."""
        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        """Make Wiha40010 Gridfinity module."""
        # Wiha 400 10 magnetizer dimensions
        tool_length = 49
        tool_width = 52
        tool_height = 29

        pos_aperture_to_edge = 9.5
        pos_aperture_height = 14
        pos_aperture_width = 27

        neg_aperture_to_edge = 2
        neg_aperture_height = 13.5
        neg_aperture_width = 29.5
        neg_aperture_offset = 2
        neg_aperture_step_0_width = 17
        neg_aperture_step = 3

        clearance = 1.5  # cutout clearance
        tool_cutout_length = tool_length + clearance
        tool_cutout_width = tool_width + clearance
        finger_cutout_radius = 12

        solid_ratio = 0.55
        floor_thickness = 5

        floor_elevation = GR_BASE_HEIGHT + floor_thickness
        aperture_indicator_elevation = 2

        gf_box = GridfinityBox(
            self.LENGTH_U,
            self.WIDTH_U,
            self.HEIGHT_U,
            solid=True,
            solid_ratio=solid_ratio,
            wall_th=2.5,
        )

        # cutout representing Wiha 400 10
        cutout = cq.Workplane(cq.Vector(0, 0, floor_elevation)).box(
            tool_cutout_length,
            tool_cutout_width,
            tool_height,
            centered=(True, True, False),  # lower face located on workplane
        )

        # positive aperture orientation indicator
        pos_aperture_sketch = (
            cq.Sketch()
            .rect(
                pos_aperture_height - clearance,
                pos_aperture_width - clearance,
            )
            .vertices()
            .fillet(1)
        )

        positive_orientation_indicator_loc_x = (
            (tool_length / 2) - (pos_aperture_height / 2) - pos_aperture_to_edge
        )

        # negative aperture orientation indicator
        step_1_height = neg_aperture_width - neg_aperture_step_0_width
        step_2_height = step_1_height - neg_aperture_step
        step_3_height = step_2_height - neg_aperture_step

        step_1_loc = (
            ((neg_aperture_height - clearance) / 2) - (neg_aperture_step / 2),
            -((neg_aperture_width - clearance) / 2) + (step_1_height / 2),
        )
        step_2_loc = (
            step_1_loc[0] - neg_aperture_step,
            step_1_loc[1] - neg_aperture_step,
        )
        step_3_loc = (
            step_2_loc[0] - neg_aperture_step,
            step_2_loc[1] - neg_aperture_step,
        )

        neg_aperture_sketch = (
            cq.Sketch()
            .rect(  # bounding box of negative aperture
                neg_aperture_height - clearance,
                neg_aperture_width - clearance,
            )
            .push([step_1_loc])  # step 1
            .rect(neg_aperture_step, step_1_height, mode="s")
            .push([step_2_loc])  # step 2
            .rect(neg_aperture_step, step_2_height, mode="s")
            .push([step_3_loc])  # step 3
            .rect(neg_aperture_step, step_3_height, mode="s")
            .clean()
            .reset()
            .vertices()
            .fillet(1)
        )

        neg_aperture_loc_x = (
            -(tool_length / 2) + (neg_aperture_height / 2) + neg_aperture_to_edge
        )

        # finger cutout
        finger_cutout_depth = gf_box.top_ref_height
        finger_cutout_minuend = (
            cq.Workplane()
            .cylinder(
                finger_cutout_depth,
                finger_cutout_radius,
                centered=(True, True, False),  # lower face located on workplane
            )
            .edges("<Z")
            .fillet(finger_cutout_radius)
        )
        # finger cutout is a half cylinder
        finger_cutout_subtrahend = cq.Workplane("XZ").box(
            24, finger_cutout_depth, 12, centered=(True, False, False)
        )
        finger_cutout = finger_cutout_minuend - finger_cutout_subtrahend
        finger_cutout = finger_cutout.clean()

        cutout = (
            cutout.faces("<Z")
            .workplane()
            .tag("workplane_orientation_indicators")
            .center(positive_orientation_indicator_loc_x, 0)
            .placeSketch(pos_aperture_sketch)
            .cutBlind(-aperture_indicator_elevation)
            .workplaneFromTagged("workplane_orientation_indicators")
            .center(neg_aperture_loc_x, -neg_aperture_offset / 2)
            .placeSketch(neg_aperture_sketch)
            .cutBlind(-aperture_indicator_elevation)
        )

        # positive Y-axis finger cutout
        cutout = cutout + finger_cutout.translate(
            (0, tool_cutout_width / 2, floor_elevation)
        )
        # negative Y-axis finger cutout
        cutout = cutout + finger_cutout.rotate((0, 0, 0), (0, 0, 1), 180).translate(
            (0, -tool_cutout_width / 2, floor_elevation)
        )
        # positive X-axis finger cutout
        cutout = cutout + finger_cutout.rotate((0, 0, 0), (0, 0, 1), -90).translate(
            ((tool_width - clearance) / 2, 0, floor_elevation)
        )
        # negative X-axis finger cutout
        cutout = cutout + finger_cutout.rotate((0, 0, 0), (0, 0, 1), 90).translate(
            (-(tool_width - clearance) / 2, 0, floor_elevation)
        )

        part = gf_box.cq_obj - cutout

        return part
