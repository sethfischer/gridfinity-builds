"""Invoke tasks for basic Gridfinity boxes and baseplates."""

from invoke import task

from gridfinity_builds.constants import MAX_WALL_THICKNESS
from gridfinity_builds.helpers import output


@task
def box_1_1_1(c):
    """Basic box 1U×1U×1U."""
    length = 1
    width = 1
    height = 1

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--output {output('basic-box', length=length, width=width, height=height)}"
    )


@task
def box_1_1_6(c):
    """Basic box 1U×1U×6U."""
    length = 1
    width = 1
    height = 6

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--output {output('basic-box', length=length, width=width, height=height)}"
    )


@task
def box_3_1_9(c):
    """Basic box 3U×1U×9U."""
    length = 3
    width = 1
    height = 9

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--wall={MAX_WALL_THICKNESS} "
        f"--output {output('basic-box', length=length, width=width, height=height)}"
    )


@task
def box_3_2_9(c):
    """Basic box 3U×2U×9U."""
    length = 3
    width = 2
    height = 9

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--wall={MAX_WALL_THICKNESS} "
        f"--output {output('basic-box', length=length, width=width, height=height)}"
    )


@task
def box_4_2_9(c):
    """Basic box 4U×2U×9U."""
    length = 4
    width = 2
    height = 9

    c.run(
        f"gridfinitybox {length} {width} {height} "
        f"--wall={MAX_WALL_THICKNESS} "
        f"--output {output('basic-box', length=length, width=width, height=height)}"
    )


@task
def baseplate_7_5(c):
    """Simple baseplate 7U×5U."""
    length = 7
    width = 5

    c.run(
        f"gridfinitybase {length} {width} "
        f"--format STEP "
        f"--output {output('baseplate', length=length, width=width)}"
    )
