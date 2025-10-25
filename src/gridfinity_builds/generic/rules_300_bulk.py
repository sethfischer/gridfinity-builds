"""Generic bulk 300 mm rules Gridfinity module."""

import math

import cadquery as cq
from cqgridfinity import GR_BASE_HEIGHT, GR_TOL, GRU, GridfinityBox

from gridfinity_builds.constants import COLOR_ITEM, MAX_WALL_THICKNESS
from gridfinity_builds.cq_containers import CqWorkplaneContainer


class Rules300Bulk(CqWorkplaneContainer):
    """Bulk 300 mm rules Gridfinity module."""

    # Gridfinity size
    LENGTH_U = 2
    WIDTH_U = 1
    HEIGHT_U = 6

    def __init__(self):
        """Initialize 300 mm rules Gridfinity module."""
        self._cq_objects = {}
        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        """Make 300 mm rules Gridfinity module."""
        rule_dimensions = {
            "toledo": {"length": 335, "width": 1.2, "height": 25},
            "taurus": {"length": 318, "width": 2.3, "height": 40},
            "nvidia": {"length": 308, "width": 2.3, "height": 38.2},
        }

        width_clearance = 1
        length_clearance = 3
        floor_thickness = 3
        cutout_floor_elevation = GR_BASE_HEIGHT + floor_thickness

        number_of_rules = len(rule_dimensions)
        longest_rule_length = max(int(d["length"]) for d in rule_dimensions.values())
        highest_rule_height = max(int(d["height"]) for d in rule_dimensions.values())

        gf_box = GridfinityBox(
            self.LENGTH_U,
            self.WIDTH_U,
            self.HEIGHT_U,
            solid=True,
        )

        # the minimum length required for the longest rule
        minimum_storage_length = (
            longest_rule_length + length_clearance + MAX_WALL_THICKNESS
        )
        # storage length in Gridfinity units to fit the longest rule
        storage_length_gru = math.ceil(minimum_storage_length / GRU)
        # storage length in mm excluding spacing between Gridfinity modules
        storage_length = (storage_length_gru * GRU) - (GR_TOL * 2)

        self.mirror_basepoint_x = (storage_length_gru / 2) * GRU

        rule_y_spacing = GRU / (number_of_rules + 1)
        initial_y_offset = ((number_of_rules - 1) * rule_y_spacing) / 2

        rule_x_offset = (storage_length / 2) + GR_TOL

        self._cq_objects["cutout"] = cq.Workplane()
        self._cq_objects["rules"] = cq.Workplane()

        rule_y_offset = initial_y_offset

        for name, dimensions in rule_dimensions.items():
            origin = (
                rule_x_offset,
                rule_y_offset,
                cutout_floor_elevation + (highest_rule_height - dimensions["height"]),
            )

            self._cq_objects["cutout"] = self._cq_objects["cutout"] + cq.Workplane(
                origin=origin
            ).box(
                dimensions["length"] + length_clearance,
                dimensions["width"] + width_clearance,
                dimensions["height"],
                centered=(True, True, False),
            )

            self._cq_objects["rules"] = self._cq_objects["rules"] + cq.Workplane(
                origin=origin
            ).box(
                dimensions["length"],
                dimensions["width"],
                dimensions["height"],
                centered=(True, True, False),
            )

            rule_y_offset = rule_y_offset - rule_y_spacing

        part = gf_box.cq_obj.translate((GRU, 0, 0))
        part = part - self._cq_objects["cutout"]

        part_mirrored = part.mirror(
            "ZY", basePointVector=(self.mirror_basepoint_x, 0, 0)
        )

        return part + part_mirrored


if "show_object" in locals():
    from cqgridfinity import GridfinityBaseplate

    result = Rules300Bulk()
    show_object(result.cq_object)  # noqa: F821

    show_object(  # noqa: F821
        result.cq_objects["rules"],
        options={"alpha": 0.5, "color": COLOR_ITEM},
    )
    show_object(  # noqa: F821
        result.cq_objects["cutout"],
        options={"alpha": 0, "color": COLOR_ITEM},
    )

    baseplate = GridfinityBaseplate(11, 3)
    baseplate_translated = baseplate.cq_obj.translate((4.5 * GRU, 0, 0))
    show_object(  # noqa: F821
        baseplate_translated,
        options={"alpha": 0.5, "color": COLOR_ITEM},
    )


if __name__ == "__main__":
    from cadquery.vis import show

    result = Rules300Bulk()
    show(result.cq_object)
