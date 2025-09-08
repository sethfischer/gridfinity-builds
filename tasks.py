"""Record of Gridfinity builds."""

import os
from pathlib import Path

from invoke import task

from custom.constants import MAX_WALL_THICKNESS

BUILD_DIR = "_build"


def output(slug: str, length: float, width: float, height: float = None) -> Path:
    """Generate output pathname."""
    filename = f"gf_{slug}_{length}x{width}"

    if height:
        filename += f"x{height}"

    filename += ".step"

    client_id = os.environ.get("BOXES_CLIENT_ID", None)

    if client_id:
        filename = f"{client_id}_{filename}"

    return Path(BUILD_DIR, filename)


@task
def mkdir_build(c):
    """Create build directory."""
    c.run(f"mkdir -p {BUILD_DIR}")


@task(pre=[mkdir_build])
def clean(c):
    """Clean build directory."""
    c.run(f"rm -rf {BUILD_DIR}/*.step")


@task(pre=[mkdir_build])
def box_1_1_1(c):
    """Basic box 1U×1U×1U."""
    length = 1
    width = 1
    height = 1

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--output {output('box', length=length, width=width, height=height)}"
    )


@task(pre=[mkdir_build])
def box_1_1_6(c):
    """Basic box 1U×1U×6U."""
    length = 1
    width = 1
    height = 6

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--output {output('box', length=length, width=width, height=height)}"
    )


@task(pre=[mkdir_build])
def box_3_1_9(c):
    """Basic box 3U×1U×9U."""
    length = 3
    width = 1
    height = 9

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--wall={MAX_WALL_THICKNESS} "
        f"--output {output('box', length=length, width=width, height=height)}"
    )


@task(pre=[mkdir_build])
def box_3_2_9(c):
    """Basic box 3U×2U×9U."""
    length = 3
    width = 2
    height = 9

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--wall={MAX_WALL_THICKNESS} "
        f"--output {output('box', length=length, width=width, height=height)}"
    )


@task(pre=[mkdir_build])
def box_4_2_9(c):
    """Basic box 4U×2U×9U."""
    length = 4
    width = 2
    height = 9

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--wall={MAX_WALL_THICKNESS} "
        f"--output {output('box', length=length, width=width, height=height)}"
    )


@task(pre=[mkdir_build])
def baseplate_7_5(c):
    """Simple baseplate 7U×5U."""
    length = 7
    width = 5

    c.run(
        f"gridfinitybase {length} {width} "
        f"--format STEP "
        f"--output {output('baseplate', length=length, width=width)}"
    )


@task(pre=[mkdir_build])
def wiha_400_10(c):
    """Wiha 400 10 magnetizer.

    Manufacturer: Wiha
    Model: 40010
    Product page: https://www.wihatools.com/products/magnetizer-and-demagnetizer
    """
    from custom.wiha import Wiha40010Horizontal

    slug = "wiha-400-10"

    gf_module = Wiha40010Horizontal()
    gf_module.save_step_file(
        output(
            slug,
            length=Wiha40010Horizontal.LENGTH_U,
            width=Wiha40010Horizontal.WIDTH_U,
            height=Wiha40010Horizontal.HEIGHT_U,
        )
    )


@task(pre=[mkdir_build])
def eye_loupe_40(c):
    """Eye loupe."""
    from custom.eye_loupe import EyeLoupe40

    slug = "eye-loupe-40"

    gf_module = EyeLoupe40()
    gf_module.save_step_file(
        output(
            slug,
            length=EyeLoupe40.LENGTH_U,
            width=EyeLoupe40.WIDTH_U,
            height=EyeLoupe40.HEIGHT_U,
        )
    )


@task(pre=[mkdir_build])
def rules_150_bulk(c):
    """Bulk 150 mm rules."""
    from custom.rules_150_bulk import Rules150Bulk

    slug = "rules-150-bulk"

    gf_module = Rules150Bulk()
    gf_module.save_step_file(
        output(
            slug,
            length=Rules150Bulk.LENGTH_U,
            width=Rules150Bulk.WIDTH_U,
            height=Rules150Bulk.HEIGHT_U,
        )
    )


@task(pre=[mkdir_build])
def drawer_spacer_tab(c):
    """Drawer spacer for Europlan TAB Pedestal Drawers."""
    slug = "drawer-spacer-tab"

    dr_width = 326.5
    dr_depth = 449.5
    chamf_rad = 1.0
    tolerance = 0.25

    from cqgridfinity import GridfinityDrawerSpacer

    spacers = GridfinityDrawerSpacer(
        dr_width,
        dr_depth,
        verbose=True,
        show_arrows=False,
        chamf_rad=chamf_rad,
        tolerance=tolerance,
    )
    spacers.render_half_set()
    spacers.save_step_file(output(slug, length=dr_width, width=dr_depth).as_posix())
