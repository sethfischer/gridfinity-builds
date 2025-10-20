"""Invoke tasks for Muller brand items."""

from invoke import task

from gridfinity_builds.helpers import output


@task
def bu27259(c):
    """Mueller BU-27.259 safety alligator clips (×4) 1U×1U×3U."""
    from .alligator_clip_bu_27_259 import MuellerBU27259

    slug = "mueller-bu27259"

    gf_module = MuellerBU27259()
    gf_module.save_step_file(
        output(
            slug,
            length=MuellerBU27259.LENGTH_U,
            width=MuellerBU27259.WIDTH_U,
            height=MuellerBU27259.HEIGHT_U,
        )
    )
