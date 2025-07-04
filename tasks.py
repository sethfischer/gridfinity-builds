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
def baseplate_7_5(c):
    """Simple baseplate 7U×5U."""
    length = 7
    width = 5

    c.run(
        f"gridfinitybase {length} {width} "
        f"--format STEP "
        f"--output {output('baseplate', length=length, width=width)}"
    )
