"""Gridfinity for Wiha."""

import cadquery as cq
from cqgridfinity import GR_BASE_HEIGHT, GridfinityBox

from .cq_containers import CqWorkplaneContainer


class Wiha40010(CqWorkplaneContainer):
    """Wiha 400 10 magnetizer."""

    # Gridfinity box size
    LENGTH_U = 2
    WIDTH_U = 2
    HEIGHT_U = 6

    _cq_object: cq.Workplane

    def __init__(self):
        """Initialize Wiha40010."""
        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        """Make Wiha40010 Gridfinity module."""
        # Wiha 400 10 magnetizer dimensions
        tool_length = 49
        tool_width = 52
        tool_height = 29

        solid_ratio = 0.55
        clearance = 1.5  # cutout clearance
        floor_thickness = 5
        finger_hole_radius = 12

        orientation_indicator_height = 2

        positive_aperture_to_edge = 9.5
        positive_aperture_height = 14
        positive_aperture_width = 27

        negative_aperture_to_edge = 2
        negative_aperture_height = 13.5
        negative_aperture_width = 29.5
        negative_aperture_offset = 2
        negative_aperture_step_0_width = 17
        negative_aperture_step = 3

        box = GridfinityBox(
            self.LENGTH_U,
            self.WIDTH_U,
            self.HEIGHT_U,
            solid=True,
            solid_ratio=solid_ratio,
            wall_th=2.5,
        )

        # cutout representing Wiha 400 10
        cutout = cq.Workplane(cq.Vector(0, 0, GR_BASE_HEIGHT + floor_thickness)).box(
            tool_length + clearance,
            tool_width + clearance,
            tool_height,
            centered=(True, True, False),  # lower face located on workplane
        )

        # positive aperture orientation indicator
        positive_orientation_sketch = (
            cq.Sketch()
            .rect(
                positive_aperture_height - clearance,
                positive_aperture_width - clearance,
            )
            .vertices()
            .fillet(1)
        )

        positive_orientation_indicator_loc_x = (
            (tool_length / 2)
            - (positive_aperture_height / 2)
            - positive_aperture_to_edge
        )

        step_1_height = negative_aperture_width - negative_aperture_step_0_width
        step_2_height = step_1_height - negative_aperture_step
        step_3_height = step_2_height - negative_aperture_step

        step_1_loc = (
            ((negative_aperture_height - clearance) / 2) - (negative_aperture_step / 2),
            -((negative_aperture_width - clearance) / 2) + (step_1_height / 2),
        )
        step_2_loc = (
            step_1_loc[0] - negative_aperture_step,
            step_1_loc[1] - negative_aperture_step,
        )
        step_3_loc = (
            step_2_loc[0] - negative_aperture_step,
            step_2_loc[1] - negative_aperture_step,
        )

        # negative aperture orientation indicator
        negative_orientation_sketch = (
            cq.Sketch()
            .rect(  # bounding box of negative aperture
                negative_aperture_height - clearance,
                negative_aperture_width - clearance,
            )
            .push([step_1_loc])  # step 1
            .rect(negative_aperture_step, step_1_height, mode="s")
            .push([step_2_loc])  # step 2
            .rect(negative_aperture_step, step_2_height, mode="s")
            .push([step_3_loc])  # step 3
            .rect(negative_aperture_step, step_3_height, mode="s")
            .clean()
            .reset()
            .vertices()
            .fillet(1)
        )

        negative_orientation_indicator_loc_x = (
            -(tool_length / 2)
            + (negative_aperture_height / 2)
            + negative_aperture_to_edge
        )

        finger_hole_depth = (solid_ratio * box.int_height) + floor_thickness

        finger_cutout = (
            cq.Workplane()
            .cylinder(
                finger_hole_depth,
                finger_hole_radius,
                centered=(True, True, False),  # lower face located on workplane
            )
            .edges("<Z")
            .fillet(finger_hole_radius)
        )

        finger_cutout_section_removed = cq.Workplane("XZ").box(
            24, finger_hole_depth, 12, centered=(True, False, False)
        )

        half_finger_cutout = finger_cutout - finger_cutout_section_removed
        half_finger_cutout = half_finger_cutout.clean()

        cutout = (
            cutout.faces("<Z")
            .workplane()
            .tag("wp_orientation_indicators")
            .center(positive_orientation_indicator_loc_x, 0)
            .placeSketch(positive_orientation_sketch)
            .cutBlind(-orientation_indicator_height)
            .workplaneFromTagged("wp_orientation_indicators")
            .center(negative_orientation_indicator_loc_x, -negative_aperture_offset / 2)
            .placeSketch(negative_orientation_sketch)
            .cutBlind(-orientation_indicator_height)
        )

        # positive Y-axis finger cutout
        cutout = cutout + half_finger_cutout.translate(
            (0, (tool_width + clearance) / 2, GR_BASE_HEIGHT + floor_thickness)
        )
        # negative Y-axis finger cutout
        cutout = cutout + half_finger_cutout.rotate(
            (0, 0, 0), (0, 0, 1), 180
        ).translate(
            (0, -(tool_width + clearance) / 2, GR_BASE_HEIGHT + floor_thickness)
        )
        # positive X-axis finger cutout
        cutout = cutout + half_finger_cutout.rotate(
            (0, 0, 0), (0, 0, 1), -90
        ).translate(((tool_width - clearance) / 2, 0, GR_BASE_HEIGHT + floor_thickness))
        # negative X-axis finger cutout
        cutout = cutout + half_finger_cutout.rotate((0, 0, 0), (0, 0, 1), 90).translate(
            (-(tool_width - clearance) / 2, 0, GR_BASE_HEIGHT + floor_thickness)
        )

        part = box.cq_obj - cutout

        return part
