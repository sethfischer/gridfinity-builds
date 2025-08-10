"""Record of Gridfinity builds."""

import os
from pathlib import Path

from invoke import task

BUILD_DIR = "_build"


def output(slug: str, length: float, width: float, height: float = None) -> Path:
    """Generate output pathname."""
    filename = f"{slug}_{length}x{width}"

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
def box_1_3_9(c):
    """Basic box 1U×3U×9U."""
    length = 1
    width = 3
    height = 9
    wall = 2.5

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--wall={wall} "
        f"--output {output('box', length=length, width=width, height=height)}"
    )


@task(pre=[mkdir_build])
def box_2_4_9(c):
    """Basic box 2U×4U×9U."""
    length = 2
    width = 4
    height = 9
    wall = 2.5

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--wall={wall} "
        f"--output {output('box', length=length, width=width, height=height)}"
    )


@task(pre=[mkdir_build])
def box_2_3_9(c):
    """Basic box 2U×3U×9U."""
    length = 2
    width = 3
    height = 9
    wall = 2.5

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--wall={wall} "
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
