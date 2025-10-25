"""Invoke tasks for generic brand Gridfinity boxes."""

from invoke import task

from gridfinity_builds.helpers import output


@task
def eye_loupe_40(c):
    """Eye loupe 1U×1U×6U"""
    from gridfinity_builds.generic.eye_loupe import EyeLoupe40

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


@task
def rules_150_bulk(c):
    """Bulk 150 mm rules 1U×1U×6U."""
    from gridfinity_builds.generic.rules_150_bulk import Rules150Bulk

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


@task
def rules_300_bulk(c):
    """Bulk 300 mm rules 2U×1U×6U."""
    from gridfinity_builds.generic.rules_300_bulk import Rules300Bulk

    slug = "rules-300-bulk"

    gf_module = Rules300Bulk()
    gf_module.save_step_file(
        output(
            slug,
            length=Rules300Bulk.LENGTH_U,
            width=Rules300Bulk.WIDTH_U,
            height=Rules300Bulk.HEIGHT_U,
        )
    )
